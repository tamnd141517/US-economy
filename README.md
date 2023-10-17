# US-economy
Estimate and analyse a simple model of the US economy
The necessary data is in three csv files, as follows:
1. The file ‘2021-12.csv’. The file containing 127 monthly US economic time series
statistics from Mathew McCraken’s FRED-MD project
(https://research.stlouisfed.org/econ/mccracken/fred-databases/).
2. The file ‘fred_md_desc.csv’ – a file containing a variety of summary data for the
FRED-MD data.
3. ‘NBER_DATES.csv’ – a table containing the dates of US economic recessions
and expansions as identified by the US National Bureau of Economic Research
(https://www.nber.org).
The output of my model is then used to build a regression model for five economic time
series, also extracted from the database.


In order to fit the model, the data needs to be mathematically transformed in
several ways. The transformation required for each series and the corresponding
code to compute these are set out below. The appropriate transformation for each
variable is supplied in the ‘tfcode’ field in the description table. The table below
gives the code required to transform the data for any given Pandas Series stored in
the variable ‘srs’:
Tfcode Description          Pandas Code
1      1st differences      srs.diff()
2      2nd differences      srs.diff().diff()
3      Log np.log(srs)
4      Log 1st differences  np.log(srs).diff()
5      Log 2nd differences  np.log(srs).diff().diff()
6      Percent Change       (srs/srs.shift(1) – 1)
