import { Typography, FormGroup, FormControlLabel, Checkbox, Button, Box } from "@mui/material";
import { useState, useEffect } from "react";
import FormContainer from "../components/FormContainer";

const Votar = () => {
  const [seleccionado, setSeleccionado] = useState("");
  const [opciones, setOpciones] = useState([]);

  const cc = localStorage.getItem("cc");
  const id_circuito = localStorage.getItem("id_circuito");

  useEffect(() => {
    fetch("http://localhost:8000/api/opciones-voto") 
      .then((res) => res.json())
      .then((data) => setOpciones(data))
      .catch((err) => {
        console.error("Error cargando opciones:", err);
        setOpciones([]);
      });
  }, []);

  const handleChange = (opcion) => {
    setSeleccionado(opcion);
  };

  const handleVotar = async () => {
    if (!seleccionado) {
      alert("Selecciona una opción antes de votar");
      return;
    }

    const payload = {
      valor_lista: seleccionado.valor_lista,
      id_partido: seleccionado.id_partido,
      id_eleccion: seleccionado.id_eleccion,
      id_tipo_eleccion: seleccionado.id_tipo_eleccion,
      id_tipo_voto: seleccionado.id_tipo_voto,
      id_circuito: parseInt(id_circuito),
      fecha: new Date().toISOString().split("T")[0],
      es_observado: false,
      cc_persona: cc, 
    };

    try {
      const response = await fetch("http://localhost:8000/api/votos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) throw new Error("No se pudo registrar el voto");

      alert("Voto registrado con éxito");
      setSeleccionado(null);
    } catch (error) {
      alert("Error al votar: " + error.message);
    }
  };

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">VOTAR</Typography>
      <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
      <FormGroup>
        {Array.isArray(opciones) && opciones.map((op) => (
          <FormControlLabel
            key={op.label}
            control={
              <Checkbox
                checked={seleccionado?.label === op.label}
                onChange={() => handleChange(op)}
                sx={{
                    "&.Mui-checked": { color: "success.main" },
                  }}
              />
            }
            label={op.label}
          />
        ))}
      </FormGroup>
      </Box>
      <Box sx={{ mt: 3, display: "flex", justifyContent: "space-around" }}>
        <Button variant="contained" color="success" onClick={handleVotar}>Votar</Button>        
        <Button variant="contained" color="error" onClick={() => setSeleccionado(null)}>Cancelar</Button>
      </Box>
    </FormContainer>
  );
};

export default Votar;
