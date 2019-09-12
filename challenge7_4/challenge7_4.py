import pandas as pd
from matplotlib import pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import make_pipeline
import warnings

warnings.filterwarnings('ignore')

def Temperature():
    X_train, X_test, y_train_m, y_train_u, y_train_l, y_test_m, y_test_u, y_test_l, test = clean()


    UpperPredict = []
    MedianPredict = []
    LowerPredict = []

    for i in [2,]:
        model_m = make_pipeline(PolynomialFeatures(i, include_bias=False),
                LinearRegression())
        model_m.fit(X_train, y_train_m)
        pred_m = model_m.predict(X_test)
        #print("{}'s error is :".format(i), mean_absolute_error(pred_m, y_test_m))

    for i in [2,]:
        model_u = make_pipeline(PolynomialFeatures(i, include_bias=False),
                LinearRegression())
        model_u.fit(X_train, y_train_u)
        pred_u = model_u.predict(X_test)
        #print("{}'s error is :".format(i), mean_absolute_error(pred_u, y_test_u))
    
    for i in [2,]:
        model_l = make_pipeline(PolynomialFeatures(i, include_bias=False),
                LinearRegression())
        model_l.fit(X_train, y_train_l)
        pred_l = model_l.predict(X_test)
        #print("{}'s error is :".format(i), mean_absolute_error(pred_l, y_test_l))
    MedianPredict = list(map(rd, model_m.predict(test.reshape(-1, 1)).reshape(-1,).tolist()))
    UpperPredict = list(map(rd, model_u.predict(test.reshape(-1, 1)).reshape(-1,).tolist()))
    LowerPredict = list(map(rd, model_l.predict(test.reshape(-1, 1)).reshape(-1,).tolist()))

    return UpperPredict, MedianPredict, LowerPredict

def clean():
    df = pd.read_csv('GlobalSurfaceTemperature.csv')
    train = df.iloc[:161, :]
    test = df.iloc[161:, 0]
    X_train, X_test, y_train, y_test = train_test_split(train.iloc[:, 0],
            train.iloc[:, 1:], test_size=0.3, random_state=10)

    y_train_m = y_train[['Median']]
    y_train_u = y_train[['Upper']]
    y_train_l = y_train[['Lower']]

    y_test_m = y_test[['Median']]
    y_test_u = y_test[['Upper']]
    y_test_l = y_test[['Lower']]

    X_train = X_train.reshape(-1, 1)
    X_test = X_test.reshape(-1, 1)
    return X_train, X_test, y_train_m, y_train_u, y_train_l, y_test_m, y_test_u, y_test_l, test

def rd(x):
    x = round(x, 3)
    return x

if __name__ == '__main__':
    print(Temperature())
