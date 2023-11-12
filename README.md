# US-economy
The main goal of this project is estimate and analyse a simple model of the US economy. 

The necessary data is in three csv files, as follows:
1. The file ‘2021-12.csv’. The file containing 127 monthly US economic time series
statistics from Mathew McCraken’s FRED-MD project
(https://research.stlouisfed.org/econ/mccracken/fred-databases/).
2. The file ‘fred_md_desc.csv’ – a file containing a variety of summary data for the
FRED-MD data, including the formula for each variable which should be transformed.
3. ‘NBER_DATES.csv’ – a table containing the dates of US economic recessions
and expansions as identified by the US National Bureau of Economic Research
(https://www.nber.org).

The output of my model is then used to build a AR(1) model for five economic time
series, also extracted from the database.


In order to fit the model, the data needs to be mathematically transformed in
several ways. The transformation required for each series and the corresponding
code to compute these are set out below. The appropriate transformation for each
variable is supplied in the ‘tfcode’ field in the description table.
