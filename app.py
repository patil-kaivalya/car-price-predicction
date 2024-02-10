from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)
data=pd.read_csv("Cleaned Data.csv")
@app.route('/')
def home():
    companys= sorted(data["company"].unique())
    names= sorted(data["name"].unique())
    return render_template('home.html',companys=companys,name=names, price = 0)

@app.route('/prediction', methods=['POST'])
def prediction():
    model = pickle.load(open('PricePrediction.pkl', 'rb'))
    company = request.form.get('company')
    car_model = request.form.get('model')
    year = int(request.form.get('year'))
    kms = int(request.form.get('kms'))
    fuel_type = request.form.get('fuel')
    price = model.predict(pd.DataFrame([[car_model, company, year, kms, fuel_type]], columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']))
    price = "{:,.2f}".format(price[0])
    html_code = '''<script>
                    window.addEventListener('load', function() {
                    window.location.hash = 'answer';
                    });
                </script>'''
    return render_template('home.html', price = price, html_code=html_code)


app.run(debug=True, host='0.0.0.0')