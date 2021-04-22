from flask import Flask, render_template, request
import jsonify
import requests
import pickle
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
app = Flask(__name__)
model = pickle.load(open('random_forest_regression_model.pkl', 'rb'))
@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


standard_to = StandardScaler()
@app.route("/predict", methods=['POST'])
def predict():
    Fuel_Type_Diesel=0
    if request.method == 'POST':
        Year = int(request.form['Year'])
        Mileage=int(request.form['Mileage'])
        Engine_Capacity=int(request.form['Engine_Capacity'])
        Mileage2=np.log(Mileage)
        Transmission=request.form['Transmission']
        Fuel_Type = request.form['Fuel_Type']
        Brand = request.form['Brand']


        if(Fuel_Type=='Petrol'):
                Fuel_Type_Petrol=1
                Fuel_Type_Hybrid=0
        else:
            Fuel_Type_Petrol = 0
            Fuel_Type_Hybrid = 1

        No_of_Years=2021-Year

        if(Transmission=='Automatic'):
                Transmission_Auto=1

        else:
            Transmission_Auto = 0

        if(Brand=='Honda'):
                Brand_Honda=1
                Brand_Toyota=0
        else:
            Brand_Honda = 0
            Brand_Toyota = 1


        prediction=model.predict([[Mileage2,Engine_Capacity,No_of_Years,Transmission_Auto,Fuel_Type_Hybrid,Fuel_Type_Petrol,Brand_Honda,Brand_Toyota]])
        output=round(prediction[0])

        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")

        else:

            return render_template('index.html',prediction_text=" Car Details - Year = " + str(Year) + " , Mileage = " + str(Mileage) + " , Engine Capacity = " + str(Engine_Capacity) + " , Transmission = " + Transmission + " , Fuel Type = " + Fuel_Type + ", Brand = " + Brand + " || Second Hand Price in Rupees =  {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)

