from flask import Flask, render_template,request

import requests
import json
from ibm_watson import LanguageTranslatorV3
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from code_country import code_country_en
from code_country import code_country_jp
from code_country import utc_to
import re
import datetime


app = Flask(__name__)

@app.route('/')
def hello():
    html = render_template('index.html')
    return html
 

@app.route('/introduction')
def input():
    input_html = render_template('input.html')
    return input_html


@app.route('/introductionja')
def inputja():
    inputja_html = render_template('inputja.html')
    return inputja_html

@app.route('/temperture',methods=["GET","POST"])
def search_city():
    
    API_KEY = '4415a57f4cae6fc0551641214943ed80'  # initialize your key here
     # city name passed as argument
    city = request.form['region']
    value = request.form['language']
    flag = 0
    if re.search(r'^[^a-zA-Z]',city):
        flag = 1
        cityjp = city
        authenticator = IAMAuthenticator('9S_8AcwsUO09e7u8iqno2rgt7fb41mQSpgmlv9qocHzd')
        language_translator = LanguageTranslatorV3(
            version='2018-05-01',
            authenticator=authenticator
        )
        language_translator.set_service_url('https://api.jp-tok.language-translator.watson.cloud.ibm.com/instances/a07cc900-3f25-489d-9a4c-fc8f10ea5292')
        translation = language_translator.translate(
            text=city,
            model_id='ja-en').get_result()
        city = translation['translations'][0]['translation']


    # call API and convert response into Python dictionary
    url = f'http://api.openweathermap.org/data/2.5/weather?units=metric&q={city}&APPID={API_KEY}'
    response = requests.get(url).json()
    
    # error like unknown city name, inavalid api key
    if response.get('cod') != 200:
        message = response.get('message', '')
        return f'Error getting temperature for {city.title()}. Error message = {message}'
    
    # get current temperature and convert it into Celsius
    current_temperature = response.get('main', {}).get('temp')
    country_name = response.get('sys',{}).get('country')
    current_time = response.get('timezone')

    if current_temperature:
        if value == '0':
            texts, links=code_country_en(country_name)
            time = utc_to(current_time)
            return render_template("advice.html",current_temp=current_temperature,city=city.title(),data = zip(texts,links),time=time)        elif value== '1':
            texts, links = code_country_jp(country_name)
            time = utc_to(current_time)
            return render_template('adviceja.html',current_temp=current_temperature,city=cityjp if flag==1 else city.title(),data = zip(texts,links),time=time)
    else:
        return f'Error getting temperature for {city.title()}'

if __name__=="__main__":
    app.run(debug=True)