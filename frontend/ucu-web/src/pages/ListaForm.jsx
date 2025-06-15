import { Typography, TextField, Button, Box } from "@mui/material";
import FormContainer from "../components/FormContainer";
import { useState } from "react";

const ListaForm = () => {
  const [numero, setNumero] = useState("");
  const [partido, setPartido] = useState("");
  const [candidatos, setCandidatos] = useState("");

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">CARGAR LISTA</Typography>
      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
        <TextField label="Número" value={numero} onChange={e => setNumero(e.target.value)} fullWidth />
        <TextField label="Partido" value={partido} onChange={e => setPartido(e.target.value)} fullWidth />
        <TextField label="Candidatos" value={candidatos} onChange={e => setCandidatos(e.target.value)} fullWidth />
        <Box sx={{ display: "flex", justifyContent: "space-around", mt: 2 }}>
          <Button variant="contained" color="success">Aceptar</Button>
          <Button variant="contained" color="error">Cancelar</Button>
        </Box>
      </Box>
    </FormContainer>
  );
};

export default ListaForm;
