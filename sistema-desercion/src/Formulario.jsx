import { useState } from "react";
import axios from "axios";

function Formulario() {

  const [formData, setFormData] = useState({});
  const [resultado, setResultado] = useState(null);

  const handleChange = (name, value) => {
    setFormData({
      ...formData,
      [name]: Number(value)
    });
  };

  const enviarDatos = async () => {

    const datos = {
      ...formData,

      // 🔥 VARIABLES OCULTAS (AUTO)
      "Application mode": 1,
      "Application order": 1,
      "Course": 1,
      "Daytime/evening attendance": 1,
      "Previous qualification": 1,
      "Nacionality": 1,
      "Mother's qualification": 1,
      "Father's qualification": 1,
      "Mother's occupation": 1,
      "Father's occupation": 1,
      "Displaced": 0,
      "Educational special needs": 0,
      "Debtor": 0,
      "Tuition fees up to date": 1,
      "Scholarship holder": 0,
      "International": 0,

      // rellenamos otros necesarios
      "Curricular units 1st sem (credited)": 0,
      "Curricular units 1st sem (enrolled)": 6,
      "Curricular units 1st sem (evaluations)": 6,
      "Curricular units 1st sem (without evaluations)": 0,
      "Curricular units 2nd sem (credited)": 0,
      "Curricular units 2nd sem (enrolled)": 6,
      "Curricular units 2nd sem (evaluations)": 6,
      "Curricular units 2nd sem (without evaluations)": 0
    };

    try {
      const res = await axios.post(
        "https://prediccion-production.up.railway.app/predecir",
        datos
      );

      setResultado(res.data);

    } catch (e) {
      alert("Error con la API");
    }
  };

  return (
    <div style={{ maxWidth: "500px", margin: "auto", textAlign: "center" }}>

      <h1>🎓 Predicción de Deserción</h1>
      <p>Ingrese los datos del estudiante</p>

      {/* 👤 */}
      <h3>👤 Datos básicos</h3>

      <input placeholder="Edad"
        onChange={(e)=>handleChange("Age at enrollment",e.target.value)} />

      <select onChange={(e)=>handleChange("Gender",e.target.value)}>
        <option value="">Género</option>
        <option value="1">Hombre</option>
        <option value="0">Mujer</option>
      </select>

      <select onChange={(e)=>handleChange("Marital status",e.target.value)}>
        <option value="">Estado civil</option>
        <option value="0">Soltero</option>
        <option value="1">Casado</option>
      </select>

      {/* 📊 */}
      <h3>📊 Rendimiento</h3>

      <input placeholder="Cursos aprobados 1er ciclo"
        onChange={(e)=>handleChange("Curricular units 1st sem (approved)",e.target.value)} />

      <input placeholder="Cursos aprobados 2do ciclo"
        onChange={(e)=>handleChange("Curricular units 2nd sem (approved)",e.target.value)} />

      <input placeholder="Promedio"
        onChange={(e)=>handleChange("Curricular units 1st sem (grade)",e.target.value)} />

      <input placeholder="Promedio 2do ciclo"
        onChange={(e)=>handleChange("Curricular units 2nd sem (grade)",e.target.value)} />

      {/* 💰 */}
      <h3>💰 Economía</h3>

      <input placeholder="Desempleo"
        onChange={(e)=>handleChange("Unemployment rate",e.target.value)} />

      <input placeholder="Inflación"
        onChange={(e)=>handleChange("Inflation rate",e.target.value)} />

      <input placeholder="PIB"
        onChange={(e)=>handleChange("GDP",e.target.value)} />

      <br /><br />

      <button onClick={enviarDatos}>Predecir</button>

      {resultado && (
        <div>
          <h3>Resultado</h3>
          <p>
            {resultado.prediccion === 1
              ? "⚠️ Alto riesgo"
              : "✅ Bajo riesgo"}
          </p>
          <p>Probabilidad: {resultado.probabilidad}%</p>
        </div>
      )}

    </div>
  );
}

export default Formulario;