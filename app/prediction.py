import numpy as np
import pandas as pd
import pygal
from pygal.style import DarkSolarizedStyle
from pygal import Config
from sklearn.preprocessing import PolynomialFeatures
from sklearn import preprocessing
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import Ridge
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import AdaBoostRegressor
import datetime
import math

def add_3_months(datetime_df):
    for i in range(3):
        last = len(datetime_df.index) - 1
        if datetime_df.loc[last]['month'] == 12:
            datetime_append = pd.DataFrame([[datetime_df.loc[last]['year']+1, 1, 1]], columns=['year', 'month', 'day'])
        else:
            datetime_append = pd.DataFrame([[datetime_df.loc[last]['year'], datetime_df.loc[last]['month'] + 1, 1]], columns=['year', 'month', 'day'])
        datetime_df = datetime_df.append(datetime_append, ignore_index=True)
    datetime_df['date'] = pd.to_datetime(datetime_df[['year','month','day']])
    datetime_df['mjd'] = datetime_df.apply(lambda datetime_df: date_to_mjd(datetime_df['year'], datetime_df['month'], datetime_df['day']), axis=1)
    return datetime_df

def date_to_mjd(year,month,day):
    if month == 1 or month == 2:
        yearp = year - 1
        monthp = month + 12
    else:
        yearp = year
        monthp = month
    # this checks where we are in relation to October 15, 1582, the beginning
    # of the Gregorian calendar.
    if ((year < 1582) or
        (year == 1582 and month < 10) or
        (year == 1582 and month == 10 and day < 15)):
        # before start of Gregorian calendar
        B = 0
    else:
        # after start of Gregorian calendar
        A = math.trunc(yearp / 100.)
        B = 2 - A + math.trunc(A / 4.)
    if yearp < 0:
        C = math.trunc((365.25 * yearp) - 0.75)
    else:
        C = math.trunc(365.25 * yearp)
    D = math.trunc(30.6001 * (monthp + 1))
    jd = B + C + D + day + 1720994.5
    return jd - 2400000.5

def ridge_predict_plot(reviews_df, poly_degree, ridge_alpha):
    try:
        reviews_df['year'] = reviews_df['review_posted_date'].apply(lambda reviews_df:reviews_df.year)
        reviews_df['month'] = reviews_df['review_posted_date'].apply(lambda reviews_df:reviews_df.month)
        monthly_reviews = reviews_df.groupby(['year', 'month']).count().reset_index()
        monthly_reviews['day'] = monthly_reviews['month'].apply(lambda monthly_reviews:1)
        monthly_reviews_counts = monthly_reviews[['year','month', 'day', 'review_posted_date']].rename(columns={'review_posted_date': 'counts'})
        monthly_reviews_counts['date'] = pd.to_datetime(monthly_reviews_counts[['year','month','day']])
        monthly_reviews_counts['mjd'] = monthly_reviews_counts.apply(lambda monthly_reviews_counts: date_to_mjd(monthly_reviews_counts['year'], monthly_reviews_counts['month'], monthly_reviews_counts['day']), axis=1)
        prediction_time = monthly_reviews_counts[['year', 'month', 'day']]
        prediction_time_add_3_months = add_3_months(prediction_time)
        num_row = prediction_time_add_3_months.shape[0]
        train_data = prediction_time_add_3_months['mjd'][:num_row-3].values.reshape(-1, 1)
        all_data = prediction_time_add_3_months['mjd'].values.reshape(-1, 1)
        all_data_scaled = preprocessing.scale(all_data)
        get_poly = PolynomialFeatures(poly_degree)
        all_data_poly = get_poly.fit_transform(all_data_scaled)
        x_training = all_data_poly[:num_row-3]
        y_training = monthly_reviews_counts['counts'].values.reshape(-1, 1)
        y_training_to_list = monthly_reviews_counts['counts'].values
        model = Ridge(alpha=ridge_alpha)
        model.fit(x_training, y_training)
        y_modeled = model.predict(x_training)
        mse = round(mean_squared_error(y_training, y_modeled), 2)
        print(mse)
        all_target = model.predict(all_data_poly)
        all_target_to_list = []
        for sublist in all_target:
            for item in sublist:
                if item < 0:
                    all_target_to_list.append(1)
                else:
                    all_target_to_list.append(item)
        sales_prediction = pygal.Line(height=400, x_label_rotation=20, show_minor_x_labels=False, show_legend=True,dynamic_print_values=True, style=DarkSolarizedStyle(
                      value_font_family='googlefont:Raleway',
                      value_font_size=30,
                      value_colors=('white',)))
        date_list = list(map(lambda d: d.strftime('%Y-%m-%d'), prediction_time_add_3_months['date'].tolist()))
        sales_prediction.x_labels = date_list
        sales_prediction.x_labels_major = date_list[::3]
        sales_prediction.title = 'Monthly Sales Prediction Using Polynomial Ridge Regression - MSE: {}'.format(mse)
        sales_prediction.add("Pedicted Sales", all_target_to_list)
        sales_prediction.add("Actual Sales", y_training_to_list)
        sales_prediction = sales_prediction.render_data_uri()
        return sales_prediction
    except Exception as e:
        return str(e)

def boost_decision_plot(reviews_df, max_depth):
    try:
        rng = np.random.RandomState(1)
        reviews_df['year'] = reviews_df['review_posted_date'].apply(lambda reviews_df:reviews_df.year)
        reviews_df['month'] = reviews_df['review_posted_date'].apply(lambda reviews_df:reviews_df.month)
        monthly_reviews = reviews_df.groupby(['year', 'month']).count().reset_index()
        monthly_reviews['day'] = monthly_reviews['month'].apply(lambda monthly_reviews:1)
        monthly_reviews_counts = monthly_reviews[['year','month', 'day', 'review_posted_date']].rename(columns={'review_posted_date': 'counts'})
        monthly_reviews_counts['date'] = pd.to_datetime(monthly_reviews_counts[['year','month','day']])
        monthly_reviews_counts['mjd'] = monthly_reviews_counts.apply(lambda monthly_reviews_counts: date_to_mjd(monthly_reviews_counts['year'], monthly_reviews_counts['month'], monthly_reviews_counts['day']), axis=1)
        prediction_time = monthly_reviews_counts[['year', 'month', 'day']]
        prediction_time_add_3_months = add_3_months(prediction_time)
        num_row = prediction_time_add_3_months.shape[0]
        X_training = prediction_time_add_3_months['mjd'][:num_row-3].values.reshape(-1, 1)
        y_training = monthly_reviews_counts['counts'].values
        y_training_to_list = monthly_reviews_counts['counts'].values
        all_data = prediction_time_add_3_months['mjd'].values.reshape(-1, 1)

        regr = AdaBoostRegressor(DecisionTreeRegressor(max_depth=max_depth),
                                  n_estimators=300, random_state=rng)
        regr.fit(X_training, y_training)
        y_predict = regr.predict(X_training)
        mse = round(mean_squared_error(y_training, y_predict), 2)
        all_predict = regr.predict(all_data)
        all_predict_to_list = []
        for item in all_predict:
            if item < 0:
                all_predict_to_list.append(1)
            else:
                all_predict_to_list.append(item)
        sales_prediction = pygal.Line(height=400, x_label_rotation=20, show_minor_x_labels=False, show_legend=True,dynamic_print_values=True, style=DarkSolarizedStyle(
                              value_font_family='googlefont:Raleway',
                              value_font_size=30,
                              value_colors=('white',)))
        date_list = list(map(lambda d: d.strftime('%Y-%m-%d'), prediction_time_add_3_months['date'].tolist()))
        sales_prediction.x_labels = date_list
        sales_prediction.x_labels_major = date_list[::3]
        sales_prediction.title = 'Monthly Sales Prediction Using AdaBoost Decision Tree Regression - MSE: {}'.format(mse)
        sales_prediction.add("Predicted Sales", all_predict_to_list)
        sales_prediction.add("Actual Sales", y_training_to_list)
        sales_prediction = sales_prediction.render_data_uri()
        return sales_prediction
    except Exception as e:
        return str(e)
