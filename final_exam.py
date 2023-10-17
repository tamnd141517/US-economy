import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import statsmodels.api as sma

#the pca function is written for you, call this from your code to calculate the 1st PC
def pca_function(stdata):
    """Returns the sign identified 1st principal component of a data set.
    input: stdata - a n x t pandas data frame
    output: 1st principal component, standardised to s.d = 1 and
    signed to have the same sign as the cross sectional mean of the variables"""
    factor1_us = sma.PCA(stdata, 1).factors
    factor1 = (factor1_us - factor1_us.mean()) / factor1_us.std()
    sgn = np.sign(pd.concat([stdata.mean(1), factor1], axis=1).corr().iloc[1, 0])
    return factor1 * sgn

#produce your analysis for the following five variables, which was chosen from the question paper
my_srs = ['INDPRO', 'S&P 500', 'PAYEMS', 'CPIAUCSL', 'BUSINVx']

#enter your code below, save this file as ‘final_exam.py’, Zip and upload as instructed

data = pd.read_csv("2021-12.csv",index_col=0)
df = data.drop(["Transform:"], axis = 0)
df.dropna(how ="all",inplace = True) #drop lines from the file where all entries are NaN
df.index = pd.to_datetime(df.index,format='%m/%d/%Y').to_period('M')

my_df = df[df.index <'2020-01']

data_1 = pd.read_csv("fred_md_desc.csv",index_col = 0)
data_1.dropna(how ="all", inplace = True) #drop lines from the file where all entries are NaN
df_1 = data_1.drop(['fred'],axis = 1)

desc = pd.DataFrame(df_1.values,index = data_1['fred'],columns = df_1.columns)
desc.rename(index = {"VXOCLSx":"VIXCLSx"},inplace = True)
for i in desc.index:
    if i in my_df.columns:
        continue
    desc=desc.drop([i],axis = 0)

new_df = pd.DataFrame(index = my_df.index,columns = my_df.columns)

for i in desc.index:
    if desc.loc[i,'tcode'] == 1:
        new_df[i] = my_df[i]
    elif desc.loc[i,'tcode'] == 2:
        new_df[i] = my_df[i].diff()
    elif desc.loc[i,'tcode'] == 3:
        new_df[i] = my_df[i].diff().diff()
    elif desc.loc[i,'tcode'] == 4:
        new_df[i] = np.log(my_df[i])
    elif desc.loc[i,'tcode'] == 5:
        new_df[i] = np.log(my_df[i]).diff()
    elif desc.loc[i,'tcode'] == 6:
        new_df[i] = np.log(my_df[i]).diff().diff()
    else:
        new_df[i] = (my_df[i]/my_df[i].shift(1)-1)

st_new_df = (new_df-new_df.mean())/new_df.std()
st_new_df.fillna(0, inplace = True)
st_new_df.to_csv('transformed_data.csv')

pca_function(st_new_df)
factor = pca_function(st_new_df)

sns.set_theme()
fig, axes = plt.subplots(1,2, figsize=(14, 4))
factor['comp_0'].plot(ax=axes[0])
factor['comp_0'].plot.hist(ax=axes[1],bins =10)
fig.figure.suptitle('Primary Factor (1st Principal Component)')
plt.tight_layout()
fig.savefig('factor.pdf')

lagdt = new_df.shift(1)
lagfactor = factor.shift(1)

srs_df = pd.DataFrame(index = new_df.index, columns = my_srs)
for s in my_srs:
        reg_data = pd.concat([new_df[s],lagdt[s],lagfactor],axis =1).set_axis(['srs','lagsrs','lagfactor'],axis =1).dropna()
        yt = reg_data['srs']
        yt_1 = reg_data['lagsrs']
        ft_1 = reg_data['lagfactor']
        model = sma.OLS.from_formula('yt~1+yt_1+ft_1',data =reg_data).fit()
        srs_df[s] = model.fittedvalues
        print(s,model.summary())
srs_df.dropna(how = 'all', inplace =True)
srs_df.to_csv('fitted_values.csv')

nber = pd.read_csv('NBER_DATES.csv',index_col=0)
nber1 = nber['1959-03':'2019-12']
nber1.index = pd.to_datetime(nber1.index,format='%Y/%m').to_period('M')

for s in my_srs:
    srs_data = pd.concat([srs_df[s],new_df.loc["1959-03":,s],nber1],axis = 1).set_axis(['Fitted','Transformed','nber'],axis = 1)
    fig = sns.lmplot(data=srs_data, x='Fitted', y='Transformed', col='nber')
    fig.figure.suptitle(desc.loc[s,'description'] + ': '+ desc.loc[s,'ttype'])
    fig.figure.tight_layout()
    fig.figure.savefig(s+'.pdf')