"""Set up logging formats for EmaCalc package"""

import logging
from pathlib import Path


def setup(log_file=None, save_path='.'):
    """create logging handlers
    :param log_file: (optional) string file name for logger FileHandler
    :param save_path: directory where log_file, if any, is stored
    :return: None
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    # root_logger.setLevel(logging.DEBUG)

    # *** create handlers explicitly, to specify encoding:
    if log_file is not None:
        save_path = Path(save_path)
        save_path.mkdir(parents=True, exist_ok=True)  # *** allow over-write ***
        fh = logging.FileHandler(save_path / log_file, mode='w', encoding='utf-8')
        fh.setFormatter(logging.Formatter('{asctime} {name} {levelname}: {message}',
                                          style='{',
                                          datefmt='%Y-%m-%d %H:%M:%S')
                        )
        root_logger.addHandler(fh)

    console = logging.StreamHandler()
    console.setFormatter(logging.Formatter('{asctime} {name}: {message}',
                                           style='{',
                                           datefmt='%H:%M:%S'))
    root_logger.addHandler(console)