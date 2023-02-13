
import requests
import os
import alpha_vantage 
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances
from alpha_vantage.cryptocurrencies import CryptoCurrencies
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd 
from pprint import pprint
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
# matplotlib.rcParams['figure.figsize'] = (20.0, 10.0)
app = Flask(__name__)
apikey='BS2PEZLVY06X5ZOH'
# BS2PEZLVY06X5ZOH
url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED'
newsurl ='https://www.alphavantage.co/query?function=NEWS_SENTIMENT'
overviewurl='https://www.alphavantage.co/query?function=OVERVIEW'
# function=TIME_SERIES_INTRADAY

# replace the "demo" apikey below with your own key from https://www.alphavantage.co/support/#api-key

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def signup():
    return render_template('base.html')


def get_points(symbol):
    ts = TimeSeries(key=apikey, output_format='pandas')
    res = requests.get(f'{url}', params={  'symbol': symbol, 'interval':'5min', 'apikey':{apikey}})
    # res = requests.get(url)
    response_dict= res.json()
    meta_data, header = res.json()
    ticker = pd.DataFrame.from_dict(response_dict[header], orient='index')
    return ticker

@app.route('/geocode', methods=["GET", "POST"])
def sendtostock():

    symbol=request.args['symbol']
    df = get_points(symbol)
    print(df.dtypes)
    df['1. open'] = pd.to_numeric(df['1. open'], errors='coerce')
    df['2. high'] = pd.to_numeric(df['2. high'], errors='coerce')
    df['3. low'] = pd.to_numeric(df['3. low'], errors='coerce')
    df['4. close'] = pd.to_numeric(df['4. close'], errors='coerce')
    df['5. adjusted close'] = pd.to_numeric(df['5. adjusted close'], errors='coerce')
    df['6. volume'] = pd.to_numeric(df['6. volume'], errors='coerce')
    df['7. dividend amount'] = pd.to_numeric(df['7. dividend amount'], errors='coerce')
    df['8. split coefficient'] = pd.to_numeric(df['8. split coefficient'], errors='coerce')

    df.plot()
    plt.savefig('static/img/plot.png')
    return render_template('geocode.html', plot_path='static/img/plot.png')
    # import pdb 
    # pdb.set_trace()
    # return render_template ( 'geocode.html', data=df.to_html(classes='table table-striped')) 

def get_symbols(symbol):
    res = requests.get(f'{newsurl}', params={  'symbol': symbol,'apikey':{apikey}})
    news= res.json()
    data = res.json()
    print(news)
    news = pd.DataFrame(data['feed']).head()
    return news

@app.route('/news', methods=["GET", "POST"])
def show_news():
    symbol=request.args['symbol']
    news = get_symbols(symbol)
    print(news.loc[0])
    print(news)
    news_data = [{'title': row['title'], 'url': row['url'],'summary': row['summary'] } for i, row in news.iterrows()]
    print(news_data)
    return render_template('news.html', symbol=symbol, news_data=news_data)






def get_overview(symbol):
    res = requests.get(f'{overviewurl}', params={  'symbol':symbol,'apikey':{apikey}})
    overviewnews= res.json()
    overview=pd.DataFrame(overviewnews, index = ["Symbol"])
   
    
        # df = pd.DataFrame.from_dict(response_dict[header], orient='index',columns['1. open', '2. high','3. low','4. close' ])
    return overview

@app.route('/companyoverview', methods=["GET", "POST"])
def show_overview():
    overview=request.args['symbol']
    overviewnews_data = get_overview(overview)
    print(overviewnews_data)

    overviewnews_data = [{ 'Name': row['Name'],'Description': row['Description'],'Industry': row['Industry'] } for i, row in overviewnews_data.iterrows()]
    print(overviewnews_data)
    # import pdb 
    # pdb.set_trace()
    return render_template('companyoverview.html', company=overview, overviewnews_data=overviewnews_data)



@app.route('/alldetails', methods=["GET", "POST"])
def show_all():
    overview=request.args['symbol']
    overviewnews_data = get_overview(overview)
    overviewnews_data = [{ 'Name': row['Name'],'Description': row['Description'],'Industry': row['Industry'] } for i, row in overviewnews_data.iterrows()]
    symbol=request.args['symbol']
    news = get_symbols(symbol)
    news_data = [{'title': row['title'], 'url': row['url'],'summary': row['summary'] } for i, row in news.iterrows()]
    symbol=request.args['symbol']
    df = get_points(symbol)
    # import pdb 
    # pdb.set_trace()
    return render_template('alldetails.html', data=df.to_html(classes='table table-striped'),overviewnews_data=overviewnews_data,news_data=news_data, company=overview )

    # return render_template('news.html', symbol=symbol, news_data=news.to_html(classes='table table-striped'))
    # return render_template('base.html',url=url,data=data,key=key)
        # return render_template('news.html', symbol=symbol, news_data=news.to_html(classes='table table-striped'))