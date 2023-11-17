from flask import Flask,render_template,jsonify
import pandas as pd


app = Flask(__name__)

df = pd.read_csv("data_small/stations.txt",skiprows=17)
stations = df[['STAID','STANAME']]

@app.route('/')
def home():
    return render_template('home.html',data=stations.to_html())

@app.route('/api/v1/<station>/<date>')
def search_station(station,date):
    filename = "data_small" + "\TG_STAID"+ station.zfill(6)+".txt"
    df = pd.read_csv(filename,skiprows=20,parse_dates=['    DATE'])
    temp = df.loc[df['    DATE']==date]['   TG'].squeeze()/10
    station_temp = {
        "temperature" :temp,
        "station":station,
        "date":date
    }
    return station_temp

@app.route('/api/v1/<station>')
def station_data(station):
    filename = "data_small" + "\TG_STAID"+ station.zfill(6)+".txt"
    station_temp = pd.read_csv(filename,skiprows=20,parse_dates=['    DATE'])

    return station_temp.to_dict(orient='records')


@app.route('/api/v1/yearly/<station>/<year>')
def yearly_data(station,year):
    filename = "data_small" + "\TG_STAID"+ station.zfill(6)+".txt"
    df = pd.read_csv(filename,skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    station_temp = df[df['    DATE'].str.startswith(year)]
    return station_temp.to_dict(orient='records')


if __name__ == "__main__":
    app.run(debug=True,port=5001)