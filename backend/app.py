from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import joblib
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

# Cargar modelo y scaler
modelo = load_model("modelo_desercion.h5")
scaler = joblib.load("scaler_desercion.pkl")


# 👉 Ruta de prueba
@app.route("/")
def home():
    return "API de predicción funcionando 🚀"


# 👉 Endpoint de predicción
@app.route("/predecir", methods=["GET", "POST"])
def predecir():

    if request.method == "GET":
        return jsonify({"mensaje": "Endpoint listo, usa POST para predecir"})

    try:
        datos = request.json

        # 🔥 Armar vector EXACTO (orden del modelo)
        valores = [[
            datos["Marital status"],
            datos["Application mode"],
            datos["Application order"],
            datos["Course"],
            datos["Daytime/evening attendance"],
            datos["Previous qualification"],
            datos["Nacionality"],
            datos["Mother's qualification"],
            datos["Father's qualification"],
            datos["Mother's occupation"],
            datos["Father's occupation"],
            datos["Displaced"],
            datos["Educational special needs"],
            datos["Debtor"],
            datos["Tuition fees up to date"],
            datos["Gender"],
            datos["Scholarship holder"],
            datos["Age at enrollment"],
            datos["International"],
            datos["Curricular units 1st sem (credited)"],
            datos["Curricular units 1st sem (enrolled)"],
            datos["Curricular units 1st sem (evaluations)"],
            datos["Curricular units 1st sem (approved)"],
            datos["Curricular units 1st sem (grade)"],
            datos["Curricular units 1st sem (without evaluations)"],
            datos["Curricular units 2nd sem (credited)"],
            datos["Curricular units 2nd sem (enrolled)"],
            datos["Curricular units 2nd sem (evaluations)"],
            datos["Curricular units 2nd sem (approved)"],
            datos["Curricular units 2nd sem (grade)"],
            datos["Curricular units 2nd sem (without evaluations)"],
            datos["Unemployment rate"],
            datos["Inflation rate"],
            datos["GDP"]
        ]]

        # Convertir a numpy
        valores = np.array(valores)

        # Escalar
        valores = scaler.transform(valores)

        # 🔥 Predicción
        prediccion = modelo.predict(valores)

        # 🔥 DEBUG (ver en Railway logs)
        print("VALORES:", valores)
        print("PREDICCION RAW:", prediccion)

        # Resultado binario
        resultado = int(prediccion[0][0] > 0.5)

        # 🔥 PROBABILIDAD CORRECTA
        probabilidad = float(prediccion[0][0]) * 100

        return jsonify({
            "prediccion": resultado,
            "probabilidad": round(probabilidad, 2)
        })

    except Exception as e:
        print("ERROR:", str(e))  # ver en logs
        return jsonify({"error": str(e)})