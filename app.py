from flask import Flask, render_template, request
import pandas as pd
from bokeh.plotting import figure
from bokeh.embed import components
import requests

app = Flask(__name__)
#app.config['EXPLAIN_TEMPLATE_LOADING'] = True

def plotInfo(ticker):

    #My personal API key
    key = 'YY749BF6ETJWL2A7'

    #Define the url and grab the json of the data
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&&symbol={}&apikey={}'.format(ticker, key)
    response = requests.get(url)

    #Define the dataframe as the Daily time series
    df = pd.DataFrame(response.json()['Time Series (Daily)'])

    #Define some plot values
    p = figure(title=ticker+" Close Price", x_axis_type='datetime', x_axis_label='Date', y_axis_label='Price')
    p.title.align = "center"
    p.title.text_color = "black"
    p.title.text_font_size = "25px"

    #Define the line plot as the datetime data and the closing price of the given Ticker.
    #Note this is only for the most recent 31 days of available data (i.e., 1 month)
    p.line(df.iloc[3,0:30].index.values.astype('datetime64[ns]'), df.iloc[3,0:30].values.astype('float64'), line_width=2)

    return p

@app.route('/')
def index():

    return render_template('index.html')


@app.route('/Graph', methods=['GET', 'POST'])
def show_Graph():

    #Initialize the plot and then add the components to the plot.
    myPlots = []
    myPlots.append(components(plotInfo(request.form['ticker'])))

    return render_template('Graph.html', plots=myPlots)


if __name__ == "__main__":
    app.run(port=33507)
