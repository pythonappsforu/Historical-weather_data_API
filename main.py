from flask import Flask,render_template,jsonify
import pandas as pd


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/v1/<station>/<date>')
def search_word(station,date):
    filename = "data_small" + "\TG_STAID"+ station.zfill(6)+".txt"
    df = pd.read_csv(filename,skiprows=20,parse_dates=['    DATE'])
    temp = df.loc[df['    DATE']==date]['   TG'].squeeze()/10
    station_temp = {
        "temperature" :temp,
        "station":station,
        "date":date
    }
    return station_temp


if __name__ == "__main__":
    app.run(debug=True,port=5001)