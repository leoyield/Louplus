import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def climate_plot():
    df_temperature = pd.read_excel('GlobalTemperature.xlsx')
    df_climate = pd.read_excel('ClimateChange.xlsx', sheetname=None)
    df_gas = clean(df_climate)
    df_gas.name = 'Total GHC'
    df_temp = clean_t(df_temperature)
    land = df_temp.iloc[:, 0]
    land_max = df_temp.iloc[:, 1]
    land_min = df_temp.iloc[:, 2]
    land_ocean = df_temp.iloc[:, 3]
    
    fig, ax = plt.subplots(2, 2)
    ax[0][0].plot(list(df_gas['1990':'2010'].index.year), list(m_m(df_gas['1990':'2010']).values), label='Total GHC')
    ax[0][0].plot(list(land['1990':'2010'].resample('A').mean().index.year),
            list(m_m(land['1990':'2010'].resample('A').mean()).values),
            label='Land Average Temperature')
    ax[0][0].plot(
            list(land_ocean['1990':'2010'].resample('A').mean().index.year),
            list(m_m(land_ocean['1990':'2010'].resample('A').mean()).values),
            label='Land And Ocean Average Temperature')
    ax[0][0].set_xlabel('Years')
    ax[0][0].set_ylabel('Values')
    ax[0][0].legend()

    second = pd.concat([
        m_m(df_gas['1990':'2010']),
        m_m(land['1990':'2010'].resample('A').mean()),
        m_m(land_ocean['1990':'2010'].resample('A').mean())
        ], axis=1)
    second.plot(kind='bar', ax=ax[0][1])
    ax[0][1].set_xlabel('Years')
    ax[0][1].set_ylabel('Values')
    ax[0][1].legend()

    three = pd.concat([land, land_ocean], axis=1).replace(pd.np.nan, 0)
    three = three.resample('Q')
    three.plot(kind='area', ax=ax[1][0])
    ax[1][0].set_xlabel('Quarters')
    ax[1][0].set_ylabel('Temperature')
    ax[1][0].legend()

    four = pd.concat([land, land_ocean], axis=1).dropna()
    four = four.resample('Q')
    four.plot(kind='kde', ax=ax[1][1])
    ax[1][1].set_xlabel('Values')
    ax[1][1].set_ylabel('Values')
    ax[1][1].legend()
    
    plt.show()

    return fig

def m_m(series):
    series = (series - series.min()) / (series.max() - series.min())
    return series

def clean_t(data):
    data = data.set_index('Date')
    data.index = pd.to_datetime(data.index).to_period(freq="D")
    return data

def clean(work_bk):
    data = work_bk['Data']
    code = ['EN.ATM.CO2E.KT', 'EN.ATM.METH.KT.CE', 'EN.ATM.NOXE.KT.CE', 'EN.ATM.GHGO.KT.CE', 'EN.CLC.GHGR.MT.CE']

    df1 = data.iloc[:, 6:].replace('..', pd.np.nan).ffill(axis=1).bfill(axis=1)
    df2 = data.iloc[:, 2]
    df = pd.concat([df2, df1], axis=1)
    df = df.groupby('Series code').sum()
    n_df = pd.DataFrame(columns=df.columns)
    for c in code:
        n_df = pd.concat([n_df, df[df.index==c]])
    df_sum = n_df.sum(axis=0)
    df_sum.index = pd.to_datetime(df_sum.index, format='%Y').to_period(freq='A')
    return df_sum

if __name__ == '__main__':
    print(climate_plot())
