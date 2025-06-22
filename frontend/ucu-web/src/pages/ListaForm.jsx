import { Typography, TextField, Button, Box } from "@mui/material";
import FormContainer from "../components/FormContainer";
import { useState } from "react";

const ListaForm = () => {
  const [numero, setNumero] = useState("");
  const [partido, setPartido] = useState("");
  const [candidatos, setCandidatos] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/listas", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          numero,
          partido,
          candidatos,
        }),
      });

      if (!response.ok) {
        throw new Error("Error al cargar la lista");
      }

      const data = await response.json();
      alert("Lista cargada exitosamente");

      setNumero("");
      setPartido("");
      setCandidatos("");
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">CARGAR LISTA</Typography>
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{ display: "flex", flexDirection: "column", gap: 2 }}
      >
        <TextField
          label="Número"
          value={numero}
          onChange={e => setNumero(e.target.value)}
          fullWidth
        />
        <TextField
          label="Partido"
          value={partido}
          onChange={e => setPartido(e.target.value)}
          fullWidth
        />
        <TextField
          label="Candidatos"
          value={candidatos}
          onChange={e => setCandidatos(e.target.value)}
          fullWidth
        />
        <Box sx={{ display: "flex", justifyContent: "space-around", mt: 2 }}>
          <Button type="submit" variant="contained" color="success">Aceptar</Button>
          <Button variant="contained" color="error" onClick={() => {
            setNumero("");
            setPartido("");
            setCandidatos("");
          }}>Cancelar</Button>
        </Box>
      </Box>
    </FormContainer>
  );
};

export default ListaForm;
