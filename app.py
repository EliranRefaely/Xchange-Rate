from datetime import datetime
from flask import Flask, render_template, request
import requests

app = Flask(__name__)

keys = '0f02bb8d59f9a5795cf5'
today = str(datetime.now().date())

@app.route("/", methods=["POST", "GET"])
def home():
    
    currencies_api = requests.get(f'https://free.currconv.com/api/v7/currencies?apiKey=0f02bb8d59f9a5795cf5').json()['results'].values()
    curreny_lis = []
    for i in currencies_api:
        curreny_lis += [i['id']]
    curreny_lis.sort()

    if request.method == "POST":
        amount = request.form["amount"]
        if not amount.isnumeric():
            return render_template('index.html', list_currency=curreny_lis, symbol_name="Waiting for your input")
        amount = float(amount)

        basecurreny = request.form["basecurreny"]
        changecurrency = request.form["changecurrency"]

        conversion = requests.get(f'https://free.currconv.com/api/v7/convert?apiKey={keys}&q={basecurreny}_{changecurrency}&compact=ultra&date={today}&endDate={today}').json()
        conversion_cal = float(conversion[f'{basecurreny}_{changecurrency}'][today]) * amount
        try:
            symbol_api = requests.get(f'https://free.currconv.com/api/v7/currencies?apiKey={keys}').json()["results"][changecurrency]["currencySymbol"]
        except KeyError:
            symbol_api = ""
        symbol_name_api = requests.get(f'https://free.currconv.com/api/v7/currencies?apiKey={keys}').json()["results"][changecurrency]["currencyName"]

        return render_template('index.html', list_currency=curreny_lis, conversion=round(conversion_cal, 2), symbol=symbol_api, symbol_name=symbol_name_api)
    else:
        return render_template('index.html', list_currency=curreny_lis, symbol_name="")


if __name__ == "__main__":
    app.run()
