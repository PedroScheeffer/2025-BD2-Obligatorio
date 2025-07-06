import { Typography, TextField, Button, Box, MenuItem } from "@mui/material";
import FormContainer from "../components/FormContainer";
import { useState } from "react";

const tipos = [
  { id: 1, label: "Presidente" },
  { id: 2, label: "Vicepresidente" },
  { id: 3, label: "Senador" },
  { id: 4, label: "Alcalde" },
];

const CandidatosForm = () => {
  const [nombre, setNombre] = useState("");
  const [nacimiento, setNacimiento] = useState("");
  const [cc, setCc] = useState("");
  const [idTipo, setIdTipo] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/api/candidatos", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          cc: cc,
          nombre,
          fecha_nacimiento: nacimiento,
          id_tipo: idTipo,
        }),
      });

      if (!response.ok) {
        throw new Error("Error al cargar el candidato");
      }

      alert("Candidato cargado exitosamente");
      setNombre("");
      setNacimiento("");
      setCc("");
      setIdTipo("");
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
          label="Credencial Cívica"
          value={cc}
          onChange={(e) => setCc(e.target.value)}
          fullWidth
        />

        <TextField
          label="Nombre"
          value={nombre}
          onChange={(e) => setNombre(e.target.value)}
          fullWidth
        />

        <TextField
          label="Fecha de Nacimiento"
          type="date"
          InputLabelProps={{ shrink: true }}
          value={nacimiento}
          onChange={(e) => setNacimiento(e.target.value)}
          fullWidth
        />

        <TextField
          select
          label="Tipo de Candidato"
          value={idTipo}
          onChange={(e) => setIdTipo(e.target.value)}
          fullWidth
        >
          {tipos.map((tipo) => (
            <MenuItem key={tipo.id} value={tipo.id}>
              {tipo.label}
            </MenuItem>
          ))}
        </TextField>

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
              setCc("");
              setIdTipo("");
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
