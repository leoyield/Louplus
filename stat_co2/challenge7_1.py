import pandas as pd

def co2():
    df_climate = pd.read_excel('ClimateChange.xlsx', sheetname=None)
    df = clean(df_climate)
    sumem = df.groupby('Income group').sum()
    Hig = df.sort_values('co2', ascending=False).groupby('Income group').first()
    Low = df.sort_values('co2', ascending=True).groupby('Income group').first()
    results = pd.concat([sumem, Hig, Low], axis=1)
    results.columns = [
            'Sum emissions',
            'Highest emission country',
            'Highest emissions',
            'Lowest emission country',
            'Lowest emissions'
            ]
    return results

def clean(work_book):
    data = work_book['Data']
    series = work_book['Country']

    data = data[data['Series code']=='EN.ATM.CO2E.KT']
    data_country = data['Country name']
    co2 = data.iloc[:, 6:]
    #print('***co2:***',co2.head())
    co2.index = data_country
    co2 = co2.replace('..', pd.np.nan).ffill(axis=1).bfill(axis=1).dropna().drop_duplicates().sum(axis=1)
    
    group_country = series['Country name']
    group = series['Income group']
    group.index = group_country
    
    df = pd.concat([co2, group], axis=1).reset_index()
    df.columns = ['Country name', 'co2', 'Income group']
    
    return df

if __name__ == '__main__':
    print(co2())
    
