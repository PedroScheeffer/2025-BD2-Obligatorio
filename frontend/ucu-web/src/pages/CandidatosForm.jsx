import { Typography, TextField, Button, Box } from "@mui/material";
import FormContainer from "../components/FormContainer";
import { useState } from "react";

const CandidatosForm = () => {
  const [nombre, setNombre] = useState("");
  const [nacimiento, setNacimiento] = useState("");
  const [partido, setPartido] = useState("");
  const [lista, setLista] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/candidatos", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          nombre,
          nacimiento,
          partido,
          lista,
        }),
      });

      if (!response.ok) {
        throw new Error("Error al cargar el candidato");
      }

      alert("Candidato cargado exitosamente");
      setNombre("");
      setNacimiento("");
      setPartido("");
      setLista("");
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">
        CARGAR CANDIDATOS
      </Typography>
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{ display: "flex", flexDirection: "column", gap: 2 }}
      >
        <TextField
          label="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          fullWidth
        />
        <TextField
          label="Nacimiento"
          type="date"
          InputLabelProps={{ shrink: true }}
          value={nacimiento}
          onChange={(e) => setNacimiento(e.target.value)}
          fullWidth
        />
        <TextField
          label="Partido"
          value={partido}
          onChange={(e) => setPartido(e.target.value)}
          fullWidth
        />
        <TextField
          label="Lista"
          value={lista}
          onChange={(e) => setLista(e.target.value)}
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
              setNombre("");
              setNacimiento("");
              setPartido("");
              setLista("");
            }}
          >
            Cancelar
          </Button>
        </Box>
      </Box>
    </FormContainer>
  );
};

export default CandidatosForm;
