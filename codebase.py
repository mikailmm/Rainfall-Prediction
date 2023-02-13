import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from category_encoders.binary import BinaryEncoder


def metrics(y_true, y_pred):
    print("MSE  :", mean_squared_error(y_true, y_pred))
    print("RMSE :", mean_squared_error(y_true, y_pred)**(0.5))

def preprocessing_basic(data):
    le = LabelEncoder()
    data = data.copy()
    
    data.time = pd.to_datetime(data.time).astype(int)
    data['sunrise (iso8601)'] = pd.to_datetime(data['sunrise (iso8601)']).astype(int)
    data['sunset (iso8601)'] = pd.to_datetime(data['sunset (iso8601)']).astype(int)
    
    data['city'] = le.fit_transform(data['city'])
    
    return data

def preprocessing_alpha1(data):
    le = LabelEncoder()
    data = data.copy()
    
    # data.time = pd.to_datetime(data.time).astype(int)
    data = data.set_index('time')
    # data = data.drop('time', axis=1)
    # data['daylight_amount'] = (pd.to_datetime(data['sunset (iso8601)']) - pd.to_datetime(data['sunrise (iso8601)'])).apply(_get_minutes)
    data = data.drop({'sunrise (iso8601)', 'sunset (iso8601)'}, axis=1)
    # data['sunrise (iso8601)'] = pd.to_datetime(data['sunrise (iso8601)']).astype(int)
    # data['sunset (iso8601)'] = pd.to_datetime(data['sunset (iso8601)']).astype(int)
    
    data['city'] = le.fit_transform(data['city'])    
    
    return data

def preprocessing_alpha5(data):
    le = LabelEncoder()
    ohe = OneHotEncoder()
    be = BinaryEncoder()
    data = data.copy()
    
    elevations = ohe.fit_transform(data.loc[:, ['elevation']])
    elevations = pd.DataFrame(elevations.todense())
    elevations.columns = elevations.columns.astype(str)
    # eleva = be.fit_transform(data['elevation'].astype(str))
    # elevations = eleva
    data = data.merge(elevations.add_prefix('elevation_'), left_index=True, right_index=True)
    data = data.drop('elevation', axis=1)

    cities = ohe.fit_transform(data.loc[:, ['city']])
    cities = pd.DataFrame(cities.todense())
    data = data.merge(cities.add_prefix('city_'), left_index=True, right_index=True)
    data = data.drop('city', axis=1)
    # cities = be.fit_transform(data['city'])
    # data = data.merge(cities, left_index=True, right_index=True)
    # data = data.drop('city', axis=1)
    # data['city'] = le.fit_transform(data['city'])
    
    data['time'] = pd.to_datetime(data['time'])
    data = data.set_index('time')
    # data = data.drop('time', axis=1)
    # data['daylight_amount'] = (pd.to_datetime(data['sunset (iso8601)']) - pd.to_datetime(data['sunrise (iso8601)'])).apply(_get_minutes)
    data = data.drop({'sunrise (iso8601)', 'sunset (iso8601)'}, axis=1)

    # data = data.drop('winddirection_10m_dominant (°)', axis=1)

    return data

def missing_data_basic(data):
    return data.dropna().reset_index().drop('index', axis=1)

def missing_data_alpha3(data):
    # return data.ffill()
    return data.interpolate()

def crossval(data):
    # '2019-01-22'
    # '2020-07-04'
    # '2019-04-03' & '2020-05-17'
    pass

def _get_minutes(timediff: pd.Timedelta):
    try:
        return timediff.seconds/60
    except Exception:
        return 'n/a'