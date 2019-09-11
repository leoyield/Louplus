import pandas as pd
import matplotlib.pyplot as plt

def co2_gdp_plot():
    df_climate = pd.read_excel('ClimateChange.xlsx', sheetname=None)
    df = clean(df_climate)
    re_index = df.reset_index()
    
    order = []
    f_country = ['CHN', 'FRA', 'GBR', 'RUS', 'USA']
    for c in f_country:
        o = re_index[re_index['Country code']==c].index[0]
        order.append(o)

    fig = plt.subplot()
    plt.title('GDP-CO2')
    plt.xlabel('Countries')
    plt.ylabel('Values')
    plt.plot(list(df['CO2-SUM']), label='CO2-SUM')
    plt.plot(list(df['GDP-SUM']), label='GDP-SUM')
    plt.xticks(order, f_country)
    plt.legend()
    #plt.show()

    china = df.loc['CHN', :]
    china = [round(float(china['CO2-SUM']), 3), round(float(china['GDP-SUM']), 3)]

    return fig, china

def clean(work_bk):
    data = work_bk['Data']
    country = work_bk['Country']

    gdp_code = 'NY.GDP.MKTP.CD'
    co2_code = 'EN.ATM.CO2E.KT'

    gdp_data = data[data['Series code']==gdp_code]
    co2_data = data[data['Series code']==co2_code]

    gdp_index = gdp_data['Country code']
    co2_index = co2_data['Country code']
    gdp = gdp_data.iloc[:, 6:]
    co2 = co2_data.iloc[:, 6:]
    gdp.index = gdp_index
    co2.index = co2_index
    gdp = gdp.replace('..', pd.np.nan).ffill(axis=1).bfill(axis=1)
    co2 = co2.replace('..', pd.np.nan).ffill(axis=1).bfill(axis=1)
    gdp = gdp.replace(pd.np.nan, 0).sum(axis=1)
    co2 = co2.replace(pd.np.nan, 0).sum(axis=1)

    #min-max
    gdp = (gdp - gdp.min()) / (gdp.max() - gdp.min())
    co2 = (co2 - co2.min()) / (co2.max() - co2.min())
    
    df = pd.concat([co2, gdp], axis=1)
    df.columns = ['CO2-SUM', 'GDP-SUM']
    return df

if __name__ == '__main__':
    print(co2_gdp_plot())
