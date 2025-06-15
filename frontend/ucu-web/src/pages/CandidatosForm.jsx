import { Typography, TextField, Button, Box } from "@mui/material";
import FormContainer from "../components/FormContainer";
import { useState } from "react";

const CandidatosForm = () => {
  const [nombre, setNombre] = useState("");
  const [nacimiento, setNacimiento] = useState("");
  const [partido, setPartido] = useState("");
  const [lista, setLista] = useState("");

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">CARGAR CANDIDATOS</Typography>
      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        <TextField label="Nombre" value={nombre} onChange={e => setNombre(e.target.value)} fullWidth />
        <TextField label="Nacimiento" type="date" InputLabelProps={{ shrink: true }} value={nacimiento} onChange={e => setNacimiento(e.target.value)} fullWidth />
        <TextField label="Partido" value={partido} onChange={e => setPartido(e.target.value)} fullWidth />
        <TextField label="Lista" value={lista} onChange={e => setLista(e.target.value)} fullWidth />
        <Box sx={{ display: "flex", justifyContent: "space-around", mt: 2 }}>
          <Button variant="contained" color="success">Aceptar</Button>
          <Button variant="contained" color="error">Cancelar</Button>
        </Box>
      </Box>
    </FormContainer>
  );
};

export default CandidatosForm;
