"""This module implements common pretty-printing repr(), str() methods
for EmaCalc classes declared as subclasses of EmaObject

Defines classes
EmaRepr --- subclass of reprlib.Repr
EmaObject --- superclass for all Ema classes using EmaRepr pretty printing

*** Version history:
* Version 1.1.3:
2025-03-27, tested with Python 3.12 and 3.13, requires >= 3.12
2025-03-21, first implementation, tested with python 3.10,
            but works as really intended only in python v >= 3.12
"""
from reprlib import Repr


# ------------------------------ special pretty-printing repr()
class EmaRepr(Repr):
    """Special for EmaCalc classes
    """
    def line_indent_sep(self, level):
        """Line indent based on self.indent, for given level
        :param level: integer, current repr depth
        :return: string
        """
        # based on super()._join
        indent = self.indent
        if indent is None:
            return ' '
        if isinstance(indent, int):
            if indent < 0:
                raise ValueError(
                    f'Repr.indent cannot be negative int (was {indent!r})'
                )
            indent *= ' '
        if isinstance(indent, str):
            return '\n' + (self.maxlevel - level) * indent
        raise TypeError(
            f'Repr.indent must be a str, int or None, not {type(indent)}'
        )

    def repr_tuple(self, x, level):
        if len(x) > self.maxtuple:
            return super().repr_tuple(x, level)
        s = repr(x)
        if len(s) > self.maxother:
            return super().repr_tuple(x, level)
        return s

    def repr_ndarray(self, x, level):
        s = repr(x)  # as defined by Numpy.printoptions
        # includes shape = (...) if printoptions.threshold exceeded
        lsep = self.line_indent_sep(level)
        return s.replace('\n', lsep)

    def repr_dict(self, x, level):
        add_len = f'({len(x)} items)' if len(x) > self.maxdict else ''
        return super().repr_dict(x, level) + add_len

    def repr_DataFrame(self, x, level):
        s = repr(x)  # as defined by pandas options 'display.xxx'
        lsep = self.line_indent_sep(level - 1)
        return lsep + s.replace('\n', lsep)

    def repr_type(self, x, level):
        return '<class ' + x.__module__ +'.' + x.__name__ + '>'

    def repr_instance(self, x, level):
        """Special version for object not already handled by standard superclass
        :param x: instance to be represented
        :param level: integer, current top level
        :return: string = pretty repr(x)
        """
        if level <= 0:
            return x.__class__.__name__ + '(' + self.fillvalue + ')'
        try:
            # instead of self.repr_TYPE(x, level), EmaObject-s have a rrepr method:
            return x.rrepr(self, level)
        except AttributeError:  # x has no rrepr() method
            return super().repr_instance(x, level)


class EmaObject:
    """Superclass for all EmaCalc classes
    defining special __repr__ and __str__ methods
    using an EmaRepr(reprlib.Repr) instance
    """
    def __repr__(self):  # ************ -> use EmaRepr version less compact?
        return  (self.__class__.__name__ + '(\n\t'
                 + ',\n\t'.join(f'{k}= {repr(v)}' for (k, v) in vars(self).items())
                 + '\n\t)')

    def __str__(self):  # using reprlib subclass
        r = EmaRepr(maxlevel=10, indent=2,
                    fillvalue='...',
                    maxdict=4,
                    maxother=80)
        return r.repr(self)

    def rrepr(self, r, level):
        """Recursive repr variant called by r.repr_instance(...)
        :param r: an EmaRepr(reprlib.Repr) instance
            calling this method for objects not handled
            by any predefined r.repr_TYPE(x, level) method
        :param level: current level
        :return: string = pretty repr(self)
        """
        newlevel = level - 1
        line_sep = r.line_indent_sep(newlevel)
        sep = ',' +line_sep
        return (self.__class__.__name__ + '(' + line_sep
                + sep.join(f'{k}= {r.repr1(v, newlevel)}'
                                for (k, v) in vars(self).items())
                +  r.line_indent_sep(level) + ')'
                )


# --------------------------------- TEST:
if __name__ == '__main__':
    import numpy as np

    REPR = EmaRepr(maxlevel=10, indent='--->')  # FOR TEST

    class TestA(EmaObject):
        """A class containing data and a dict with TestB objects
        """

        def __init__(self, a, b):
            """
            :param a: a number
            :param b: a dict
            """
            self.a = a
            self.b = b
            self._c = 'hidden'

    class TestB(EmaObject):
        """Another class with a list of sub-objects
        """

        def __init__(self, a, b_list):
            """
            :param a: a builtin object
            :param b_list: a list of objects
            """
            self.a = a
            self.b_list = b_list

    # --------------------------------

    test_d = {'arne': TestB('arnes', [1, 2, 'text']),
              'leijon': TestB('leijons', ['a', 'b', 'c'])
              }
    # print(REPR.repr([1, 2, 'text']))
    # print(REPR.repr({'a': 1, 'b': 2}))

    test_1 = TestA(100, ['a', 'b', 'c'])
    print('test_1=', test_1)
    print('repr(test_1)= ', repr(test_1))

    test_a = TestA(100, [test_d, test_d])
    test_d['rec'] = test_a  # recursion
    print('test_a=', test_a)
    print('repr(test_a)=', repr(test_a))

    print('\n*** Testing Numpy arrays')
    a = np.ones((2, 2, 7))
    a_dict = {'test': a}
    with np.printoptions(threshold=10, edgeitems=2):
        print('str(a)=\n', str(a))
        print('repr(a)=\n', repr(a))
        print('REPR.repr(a)=\n', REPR.repr(a))
        print('REPR.repr(a_dict)=\n', REPR.repr(a_dict))

# print()
    # print(REPR.repr(test_a))
