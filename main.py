from flask import Flask, render_template, request
from joblib import dump, load
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/predict", methods=['POST'])
def predict():
    date = str(request.form.get('DateTime'))
    hour = float(request.form.get('Hour'))
    df_sample = pd.DataFrame({'date': [date], 'hour': [hour]})
    df_sample = df_sample.reindex(columns=col_names)
    df_sample.fillna(0, inplace=True)
    date = pd.to_datetime(date)
    year = int(date.year)
    month = int(date.month)
    day = int(date.day)
    if year == 2019:
        df_sample.at[0, 'year_1'] = 1
    elif year == 2020:
        df_sample.at[0, 'year_2'] = 1
    elif year == 2021:
        df_sample.at[0, 'year_3'] = 1
    else:
        pass

    if day!= 1:
        df_sample.at[0, f'day_{day-1}'] = 1

    if month!= 1:
        df_sample.at[0, f'month_{month-1}'] = 1
    output = model.predict(df_sample)[0]
    return render_template('predict.html', output= output)

if __name__ == '__main__':
    model = load('model.pkl')
    col_names = load('column_names.pkl')
    app.run(debug=True)