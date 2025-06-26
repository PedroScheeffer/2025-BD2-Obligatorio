import { Typography, TextField, Button, Box } from "@mui/material";
import FormContainer from "../components/FormContainer";
import { useState } from "react";

const CircuitosForm = () => {
  const [establecimiento, setEstablecimiento] = useState("");
  const [mesa, setMesa] = useState("");
  const [accesibilidad, setAccesibilidad] = useState("");
  const [integrantes, setIntegrantes] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/circuitos", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id_establecimiento: parseInt(establecimiento),
          id_zona: 1, 
          id_eleccion: 1, 
          id_tipo_eleccion: 1, 
          accesibilidad: accesibilidad.toLowerCase() === "sí" || accesibilidad.toLowerCase() === "si"
        }),
      });

      if (!response.ok) {
        throw new Error("Error al cargar el circuito");
      }

      alert("Circuito cargado exitosamente");
      setEstablecimiento("");
      setMesa("");
      setAccesibilidad("");
      setIntegrantes("");
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">
        CARGAR CIRCUITOS
      </Typography>
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{ display: "flex", flexDirection: "column", gap: 2 }}
      >
        <TextField
          label="Establecimiento"
          value={establecimiento}
          onChange={(e) => setEstablecimiento(e.target.value)}
          fullWidth
        />
        <TextField
          label="Mesa"
          value={mesa}
          onChange={(e) => setMesa(e.target.value)}
          fullWidth
        />
        <TextField
          label="¿Es accesible?"
          value={accesibilidad}
          onChange={(e) => setAccesibilidad(e.target.value)}
          fullWidth
        />
        <TextField
          label="Integrantes"
          value={integrantes}
          onChange={(e) => setIntegrantes(e.target.value)}
          fullWidth
        />
        <Box sx={{ display: "flex", justifyContent: "space-around", mt: 2 }}>
          <Button type="submit" variant="contained" color="success">
            Aceptar
          </Button>
          <Button
            variant="contained"
            color="error"
            onClick={() => {
              setEstablecimiento("");
              setMesa("");
              setAccesibilidad("");
              setIntegrantes("");
            }}
          >
            Cancelar
          </Button>
        </Box>
      </Box>
    </FormContainer>
  );
};

export default CircuitosForm;
