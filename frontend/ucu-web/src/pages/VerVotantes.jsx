import React, { useState, useEffect } from "react";
import { Typography, Box, Select, MenuItem, FormControl, InputLabel, Table, TableBody, TableCell, TableHead, TableRow, Paper } from "@mui/material";
import FormContainer from "../components/FormContainer";

const VerVotantes = () => {
  const [circuitos, setCircuitos] = useState([]);
  const [circuitoSeleccionado, setCircuitoSeleccionado] = useState("");
  const [votantes, setVotantes] = useState([]);

  useEffect(() => {
    const fetchCircuitos = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/circuitos");
        const data = await res.json();
        setCircuitos(data);
      } catch (err) {
        console.error("Error cargando circuitos:", err);
      }
    };

    fetchCircuitos();
  }, []);

  const handleChange = async (event) => {
    const selectedId = event.target.value;
    setCircuitoSeleccionado(selectedId);

    try {
      const res = await fetch(`http://localhost:8000/api/votantes/circuito/${selectedId}`);
      const data = await res.json();
      setVotantes(data);
    } catch (err) {
      console.error("Error cargando votantes:", err);
    }
  };

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">
        Ver Votantes por Circuito
      </Typography>

      <Box sx={{ mt: 4, width: "100%" }}>
        <FormControl fullWidth>
          <InputLabel id="circuito-label">Seleccione un circuito</InputLabel>
          <Select
            labelId="circuito-label"
            value={circuitoSeleccionado}
            label="Seleccione un circuito"
            onChange={handleChange}
          >
            {circuitos.map((circuito) => (
              <MenuItem key={circuito.id} value={circuito.id}>
                {circuito.nombre}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {votantes.length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Paper>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Credencial Cívica</TableCell>
                  <TableCell>Nombre</TableCell>
                  <TableCell>CI</TableCell>
                  <TableCell>Fecha de Nacimiento</TableCell>
                  <TableCell>¿Votó?</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {votantes.map((votante, index) => (
                  <TableRow key={index}>
                    <TableCell>{votante.cc}</TableCell>
                    <TableCell>{votante.nombre}</TableCell>
                    <TableCell>{votante.ci}</TableCell>
                    <TableCell>{votante.fecha_nacimiento}</TableCell>
                    <TableCell>{votante.voto ? "Si" : "No"}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
        </Box>
      )}
    </FormContainer>
  );
};

export default VerVotantes;
