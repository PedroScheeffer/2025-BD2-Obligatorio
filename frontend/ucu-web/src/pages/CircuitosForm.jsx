import { Typography, TextField, Button, Box } from "@mui/material";
import FormContainer from "../components/FormContainer";
import { useState } from "react";

const CircuitosForm = () => {
  const [establecimiento, setEstablecimiento] = useState("");
  const [mesa, setMesa] = useState("");
  const [accesibilidad, setAccesibilidad] = useState("");
  const [integrantes, setIntegrantes] = useState("");

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">CARGAR CIRCUITOS</Typography>
      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        <TextField label="Establecimiento" value={establecimiento} onChange={e => setEstablecimiento(e.target.value)} fullWidth />
        <TextField label="Mesa" value={mesa} onChange={e => setMesa(e.target.value)} fullWidth />
        <TextField label="¿Es accesible?" value={accesibilidad} onChange={e => setAccesibilidad(e.target.value)} fullWidth />
        <TextField label="Integrantes" value={integrantes} onChange={e => setIntegrantes(e.target.value)} fullWidth />
        <Box sx={{ display: "flex", justifyContent: "space-around", mt: 2 }}>
          <Button variant="contained" color="success">Aceptar</Button>
          <Button variant="contained" color="error">Cancelar</Button>
        </Box>
      </Box>
    </FormContainer>
  );
};

export default CircuitosForm;
