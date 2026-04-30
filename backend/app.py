
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


@app.route("/predecir", methods=["POST"])
def predecir():
    try:
        datos = request.json

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

        valores = np.array(valores)
        valores = scaler.transform(valores)

        prediccion = modelo.predict(valores)
        resultado = int(prediccion[0][0] > 0.5)

        probabilidad = float(prediccion[0][0] * 100)

        return jsonify({
            "prediccion": resultado,
            "probabilidad": round(probabilidad, 2)
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        })


if __name__ == "__main__":
    app.run(debug=True)
