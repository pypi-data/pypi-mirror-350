Package **EmaCalc** implements probabilistic Bayesian analysis
of *Ecological Momentary Assessment (EMA)* data. 
The EMA methodology can be used to evaluate 
the effect of any kind of psycho-socio-medical intervention,
for example, the subjective performance of hearing aids,
in the everyday life of the user or client, 

## EMA Experiments
In an EMA study, each participant is requested to respond to a questionnaire
during normal everyday life, typically several times per day. 
Some questions may address the current real-life *Situation*,
i.e., the physical environment and the user's activity and intentions.
The participant may also be asked to rate any 
perceptual *Attribute* of interest in the study,
for example, 
the ease of speech understanding in the current situation.

Thus, EMA data usually include both *nominal* and *ordinal* results.
Typically, many records are collected from each participant, 
but the number of records may vary a lot among respondents.

This causes some interesting challenges for the statistical
analysis (Oleson et al., 2021).
The present analysis model estimates *Attribute* values 
numerically on an objective *interval scale*,
given the Situation,
although the raw input data are *subjective*
and indicate only *ordinal* judgments for each Attribute,
and *nominal* categories for the Situations. 

This package does *not* include functions to handle the data collection;
it can only use existing files with data recorded earlier.
The package can analyze data from simple or rather complex experimental designs,
including the following features:


1. The complete EMA study may include one or more test **Phases**,
for example, *before* and *after* some kind of intervention.

2. Each EMA record may characterize the current situation
in one or more pre-defined **Situation Dimensions**. 
For example, one dimension may be specified
by the *Common Sound Scenarios (CoSS)* (Wolters et al., 2016),
which is a list of broad categories of situational intentions and tasks. 
Other dimensions may specify the *Importance* of the situation,
and/or the *Hearing-Aid Program* currently used.
    
3. Each EMA record may also include discrete *ratings* for 
one or more perceptual **Attributes**. 
For example, one Attribute may be *Speech Understanding*, 
with ordinal grades *Bad*, *Fair*, *Good*, *Perfect*. 
Another attribute may be *Comfort*, with grades *Bad*, *Good*.

4. For each *Situation Dimension*, a list of allowed **Situation Categories** must be pre-defined. 
An assessment event is defined by a combination 
of exactly one selected Category from each Dimension.

5. For each perceptual *Attribute*, a list of discrete ordinal **Attribute Grades**
must be pre-defined. 
Ordinal scales may be unique for each attribute, 
or shared by more than one attribute. 
         
6. An EMA study may involve one or more distinct **Populations**,
from which separate groups of participants have been recruited.

7. Populations are distinguished by a combination of 
categories from one or more **Group Dimensions**.
For example, one dimension may be *Age*,
with categories *Young*, *Middle*, or *Old*.
Another dimension may be, e.g.,*Gender*, 
with categories *Female*, *Male*, or *Unknown*.

8. The analysis model *does not require* anything about 
the number of participants from each population,
or the number of assessments by each participant.
Of course, the reliability is improved
if there are many participants from each population, 
each reporting a large number of EMA records.

## EMA Data Analysis
The analysis uses the recorded data to
learn a probabilistic model,
representing the statistically most relevant aspects of the data.
The analysis includes a regression model to show how the Attribute values 
vary across Situations. 

1. The analysis results will show predictive **Situation Probabilities** 
    for each population, credible differences between situation probabilities within each 
    population, and credible differences between populations.

2. The analysis results will also show perceptual **Attribute Values** 
for each population, credible differences between Attribute Values
in separate situations, 
and credible Attribute Differences between populations.
3. **Differences between populations** can be shown as main effects 
in only one or a few of the pre-defined Group Dimensions,
or as complete interaction effects of categories in all Group Dimensions.


The Bayesian analysis automatically estimates the *statistical credibility*
of all analysis results, given the amount of collected data.
The Bayesian model is hierarchical. 
The package can estimate results for

1. an unseen *random individual*  in the population from which the participants were recruited,
2. the *population mean*,
3. each individual *participant*.

The first of these probability measures may be most important 
in a study designed, e.g., by a hearing-aid manufacturer 
to predict the future marketing success of some new hearing aid feature. 
The second probability measure is most closely related 
to the statistical significance as estimated by conventional hypothesis tests. 
The third measure might be most important 
in a clinical study to quantify the benefit of an intervention for individual clients.

The package can also quantify 
individual rating differences by the 
*Non-overlap of All Pairs (NAP)* effect measure
(Parker & Vannest, 2009), 
including approximate confidence intervals calculated by
the *"MW-N" method* recommended by Feng et al. (2017).

## Package Documentation
General information and version history is given in the package doc-string that may be accessed by commands
`import EmaCalc`, `help(EmaCalc)` 
in an interactive Python environment.

Input EMA data can be accessed from files in several 
of the formats that package Pandas can handle, e.g., .csv, .xlsx.
Specific information about the organization of input data files
is presented in the doc-string of module ema_data, 
accessible by commands
`import EmaCalc.ema_data`, `help(EmaCalc.ema_data)`.

After running an analysis, the logging output briefly explains
the analysis results presented in figures and tables.
Figures can be saved in any file format 
allowed by Matplotlib.
Result tables can be saved in many of the 
file formats that Pandas can handle,
e.g., .csv, .txt, .tex, as defined in module `ema_file`.
Thus, the results can easily be imported to a word-processing document 
or to other statistical packages.

## Usage

1. Install the most recent package version:
    `python3 -m pip install --upgrade EmaCalc`

2. For an introduction to the analysis results and the input data format, 
you may want to study and run the included simulation script: `python3 run_sim.py`.

3. Copy the template script `run_ema.py`, rename it, and
edit the copy as suggested in the template, to specify
    - your experimental layout,
    - the top input data directory,
    - a directory where all output result files will be stored.

4. Run your edited script: `python3 run_my_ema.py`

5. In the planning phase, complete analysis results 
may also be calculated for synthetic data 
generated from simulated experiments. 
Simulated experiments allow the same design variants as real experiments.
Copy the template script `run_sim.py`, rename it,
edit the copy, and run your own EMA simulation.

## Requirements
This package requires Python 3.12 or newer,
with recent versions of Numpy, Scipy, and Matplotlib,
as well as a support package samppy. 
Package Pandas is used to handle input data and result tables 
and requires openpyxl to access Excel (.xlsx) files.
The pip installer will check and install these packages if needed.

Pandas can also read input files and write result tables in some other formats, 
but may then need other support packages that must be installed manually.

## New in version 1.1
Flexible user control of result display styles.

Population differences can be shown in one and/or several of the predefined 
Group Dimensions, as selected by the user.

## New in version 1.1.1-5
Minor bugfix. User-friendly checks
for minor typos in function arguments.
Clarified names and headings of table files with situation differences.


## References

A. Leijon, P. von Gablenz, I. Holube, J. Taghia, and K. Smeds (2023).
Bayesian analysis of ecological momentary assessment (EMA) data
collected in adults before and after hearing rehabilitation. 
*Frontiers in Digital Health*, 5(1100705).
[download](https://www.frontiersin.org/articles/10.3389/fdgth.2023.1100705/full)

A. Leijon (2025).
Bayesian Analysis of Ecological Momentary Assessment (EMA) Data. 
*Documentation: Theory, Code usage, Validation, and Computational Details.* 
Contact the author for a copy.

D. Feng, G. Cortese, and R. Baumgartner (2017).
A comparison of confidence/credible interval methods for the area under the ROC curve
for continuous diagnostic tests with small sample size.
*Statistical Methods in Medical Research*, 26(6):2603–2621.
[download](https://journals.sagepub.com/doi/10.1177/0962280215602040)

J. J. Oleson, M. A. Jones, E. J. Jorgensen, and Y.-H. Wu (2021).
Statistical considerations for analyzing ecological momentary assessment data. 
*J Sp Lang Hear Res*, ePub:1–17. 
[download](https://pubs.asha.org/doi/10.1044/2021_JSLHR-21-00081)

R. I. Parker and K. Vannest (2009).
An improved effect size for single-case research: Nonoverlap of all pairs.
*Behavior Therapy*, 40(4):357–367. 
[download](https://www.sciencedirect.com/science/article/pii/S0005789408000816?via%3Dihub)

K. Smeds, F. Wolters, J. Larsson, P. Herrlin, and M. Dahlquist (2018).
Ecological momentary assessments for evaluation of hearing-aid preference.
*J Acoust Soc Amer* 143(3):1742–1742.
[download](https://asa.scitation.org/doi/10.1121/1.5035685)

F. Wolters, K. Smeds, E. Schmidt, and C. Norup (2016).
Common sound scenarios: A context-driven categorization of everyday sound environments
for application in hearing-device research.
*J Amer Acad Audiol*, 27(7):527–540. 
[download](https://www.thieme-connect.de/products/ejournals/abstract/10.3766/jaaa.15105)
