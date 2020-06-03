# COVID-MCS

### Introduction

COVID-MCS is an R package that allows users to apply the model confidence set (MCS) hypothesis testing framework developed in Hansen et. al (2011) to public health data in an effort to test hypotheses surrounding questions about temporal trends in the data. See Ganz (2020) for more details on the implementation of the test.

### Why COVID-MCS?

Policymakers and public health researchers have had difficulty determining whether benchmarks surrounding trends in the intensity of the COVID-19 pandemic. One reason for the confusion is that commonly-used hypothesis testing methods, e.g., t-tests for mean comparisons or linear regression models, are poorly suited for questions about shapes of trends in data, e.g., “consistent decline”.

One hypothesis testing framework that is suitable to ask questions like “has a region experienced a specified number of days of declining COVID-19 cases?” applies the MCS framework to shape-constrained regression. Based on the output of the test, the analyst can determine whether the hypothesized shape is a good fit for the data -- in the model confidence set -- and whether alternative shapes inconsistent with the data are a bad fit -- i.e., not in the model confidence set.

These results can then be used to inform policy decisions about whether necessary public health criteria are satisfied to justify the phased reopening of the local economy.

### Basic Usage

#### “main.R”

“main.R” is a  script that implements the test using three primary functions. The first (“mcs_shapes”) estimates a series of shape-constrained regressions and calculates the extent to which the estimated models depart from the data via the Kullback-Liebler Information Criterion (KLIC). The second (“mcs_shapes_boot”) uses a parametric bootstrap to re-estimate the models on simulated data, which is used to calculate (1) the effective degrees of freedom in each model and (2) the null distribution of the “range statistic” for KLIC under the hypothesis that the hypothesized models fit the data equally well. The third (“mcs_shapes_test”) then executes the hypothesis tests and returns the models in the MCS.

#### “mcs_shapes”

Data: The data passed to “mcs_shapes” should be in the following form. “t” is a vector of integers that index dates. “n” a vector of integers that indicate the total number of observations on a date. “y1” is a vector of integers that indicate the number of positive observations. So, if there are 100 positive tests out of 2000 total tests, “n” is 2000 and “y1” is 100.
Shapes: The “shapes” argument includes a list of the models to be analyzed. Currently, the following shapes are permitted:
"cei": A ceiling shape constraint. All proportions of positive observations are constrained to be less than or equal to a specified level.
“con”: A constant shape constraint. The proportion of positive observations is the same every day.
“con_cei”: A constant shape constraint in which the level is also constrained to be less than or equal to a ceiling.
“dec”: A monotonically decreasing shape constraint. The model requires that the proportion of positive observations is shrinking across every pair of days.
“dec_cei”: A monotonically decreasing shape constraint in which the level is also constrained to be less than or equal to a ceiling.
"inc": A monotonically increasing shape constraint. The model requires that the proportion of positive observations is increasing across every pair of days.
“inc_cei”: A monotonically increasing shape constraint in which the level is also constrained to be less than or equal to a ceiling.
"ius": An inverted u-shaped shape constraint. The model requires that the proportion of positive observations increase monotonically to a peak day and decrease monotonically thereafter.
"ius_cei": An inverted u-shaped shape constraint in which the level is also constrained to be less than a ceiling.
"unc": Unconstrained. The proportion of positive observation can take any value.
Other parameters:
“lag”: This permits comparisons across proportions more than one day apart. (The default lag is 1.) Increasing the lag can be especially useful in contexts where a monotonic decline is rejected due to day-to-day randomness in sampling.
“ceiling”: This sets the ceiling for the relevant shape constraints. The default is 1.

#### “mcs_shapes_boot”

“z”: The object that is output from “mcs_shapes”.
“nsim”: The number of bootstrap replications to be generated.
“seed”: Sets a seed for the purposes of replication.
“verbose”: Controls a series of comments that are generated during the bootstrap.

##### “mcs_shapes_test”

“z”: The object that is output from “mcs_shapes”.
“zb”: The object that is output from “mcs_shapes_boot”.
“alpha”: The significance value for the test.
“nested”: This controls whether to execute the hypothesis test of nested or non-nested models. If TRUE, then the arguments passed to “shapes” must be in order of decreasing restrictiveness. If FALSE, then the arguments to “shapes” can be passed in any order. If the user is unsure whether models are nested or not, it is safer to assume they are not. However, the nested hypothesis test is more powerful (if the models are indeed nested).
“verbose”: Controls a series of comments that are generated during the MCS testing framework.

“mcs_shapes_test” produces an “mcs” object with the following output:
“B”: The number of bootstrap samples.
“alpha”: The significance value for the test.
“nmodels”: The number of models tested.
“M0”: The names of the models tested.
“Mstar”: The model confidence set.
“Mstar.ix”: The indices (relative to M0) for the models in the model confidence set.
“summary”: Key output from the MCS procedure. Each row represents one cycle of testing the null hypothesis that all the models have equally good fit.
“iter”: Number of tests of equality completed.
“N”: Number of bootstrap samples for which the simulated range statistic exceeds the range statistic in the observed data.
“P.H0”: P-value for the null hypothesis for the current set of models.
“P.MCS”: MCS p-values for the current set of models. See Hansen (2011).
“MCS”: Models evaluated in this iteration.
“Model.Drop”: Model rejected from the MCS if the p-value of H0 is less than alpha.
“p.mcs”: MCS p-values.
“p.ho”: P-values for the null hypothesis for the models in the MCS.

##### Summary object
There is also a “summary” function that can be applied to the “mcs” object that is returned from “mcs_shapes_test” and returns a text summary of the information in the “mcs” object.
