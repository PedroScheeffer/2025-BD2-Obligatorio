import { Box, Typography, TextField, Button, MenuItem } from "@mui/material";
import FormContainer from "../components/FormContainer";
import { useState, useEffect } from "react";

const ListaForm = () => {
  const [numero, setNumero] = useState("");
  const [partidoSeleccionado, setPartidoSeleccionado] = useState("");
  const [idEleccion, setIdEleccion] = useState("");
  const [candidatos, setCandidatos] = useState("");
  const [partidos, setPartidos] = useState([]);

  // Obtener partidos desde la API
  useEffect(() => {
    fetch("http://localhost:8000/api/partidos")
      .then((res) => res.json())
      .then((data) => setPartidos(data))
      .catch((err) => console.error("Error al cargar partidos", err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/api/listas", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          numero,
          id_partido: partidoSeleccionado,
          id_eleccion: idEleccion,
          candidatos,
        }),
      });

      if (!response.ok) {
        throw new Error("Error al cargar la lista");
      }

      alert("Lista cargada exitosamente");
      setNumero("");
      setPartidoSeleccionado("");
      setIdEleccion("");
      setCandidatos("");
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
          label="Número de lista"
          value={numero}
          onChange={(e) => setNumero(e.target.value)}
          fullWidth
        />

        <TextField
          select
          label="Partido"
          value={partidoSeleccionado}
          onChange={(e) => setPartidoSeleccionado(e.target.value)}
          fullWidth
        >
          {partidos.map((p) => (
            <MenuItem key={p.id} value={p.id}>
              {p.nombre}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          label="ID Elección"
          value={idEleccion}
          onChange={(e) => setIdEleccion(e.target.value)}
          fullWidth
        />

        <TextField
          label="Candidatos (separados por coma)"
          value={candidatos}
          onChange={(e) => setCandidatos(e.target.value)}
          fullWidth
        />

        <Box sx={{ display: "flex", justifyContent: "space-around", mt: 2 }}>
          <Button variant="contained" color="success" type="submit">
            Aceptar
          </Button>
          <Button
            variant="contained"
            color="error"
            onClick={() => {
              setNumero("");
              setPartidoSeleccionado("");
              setIdEleccion("");
              setCandidatos("");
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
