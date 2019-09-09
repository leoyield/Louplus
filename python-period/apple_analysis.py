import pandas as pd

def quarter_volume():
    df = pd.read_csv('apple.csv')

    index = pd.to_datetime(df['Date'].values)
    s = df.iloc[:,-1]
    s.index = index
    s.index = s.index.to_period(freq='D')
    new_s = s.resample('Q').sum().sort_values(ascending=False)
    second_volume = new_s[1]
    return second_volume

if __name__ == '__main__':
    print(quarter_volume())

