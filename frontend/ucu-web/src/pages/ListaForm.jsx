import { Typography, TextField, Button, Box, MenuItem } from "@mui/material";
import FormContainer from "../components/FormContainer";
import { useState } from "react";

const ListaForm = () => {
  const [numero, setNumero] = useState("");
  const [partido, setPartido] = useState("");
  const [candidatos, setCandidatos] = useState("");
  const [idEleccion, setIdEleccion] = useState("");
  const [tipo, setTipo] = useState("");

  const tiposEleccion = [
    { label: "Nacional", value: 1 },
    { label: "Departamental", value: 2 },
    { label: "Municipal", value: 3 },
    { label: "Plebiscito", value: 4 },
    { label: "Ballotage", value: 5 },
    { label: "Referendum", value: 6 },
  ];

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
          id_eleccion: idEleccion,
          id_tipo_eleccion: tipo,
        }),
      });

      if (!response.ok) {
        throw new Error("Error al cargar la lista");
      }

      alert("Lista cargada exitosamente");

      setNumero("");
      setPartido("");
      setCandidatos("");
      setIdEleccion("");
      setTipo("");
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">
        CARGAR LISTA
      </Typography>
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{ display: "flex", flexDirection: "column", gap: 2 }}
      >
        <TextField
          label="Número"
          value={numero}
          onChange={(e) => setNumero(e.target.value)}
          fullWidth
        />
        <TextField
          label="Partido"
          value={partido}
          onChange={(e) => setPartido(e.target.value)}
          fullWidth
        />
        <TextField
          label="Candidatos"
          value={candidatos}
          onChange={(e) => setCandidatos(e.target.value)}
          fullWidth
        />
        <TextField
          label="Número de elección"
          value={idEleccion}
          onChange={(e) => setIdEleccion(e.target.value)}
          fullWidth
        />
        <TextField
          select
          label="Tipo de elección"
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
          fullWidth
        >
          {tiposEleccion.map((option) => (
            <MenuItem key={option.value} value={option.value}>
              {option.label}
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
              setNumero("");
              setPartido("");
              setCandidatos("");
              setIdEleccion("");
              setTipo("");
            }}
          >
            Cancelar
          </Button>
        </Box>
      </Box>
    </FormContainer>
  );
};

export default ListaForm;
