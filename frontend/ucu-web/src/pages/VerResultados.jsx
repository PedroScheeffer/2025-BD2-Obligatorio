import React, { useState } from "react";
import { Typography, Box, Select, MenuItem, FormControl, InputLabel, Table, TableBody, TableCell, TableHead, TableRow, Paper } from "@mui/material";
import FormContainer from "../components/FormContainer";

const VerResultados = ({ tipo }) => {
  const [categoria, setCategoria] = useState("");
  const [resultados, setResultados] = useState([]);

  const handleChange = async (event) => {
    const selected = event.target.value;
    setCategoria(selected);

    try {
      const res = await fetch(`http://localhost:8000/api/resultados/${selected}`);
      const data = await res.json();
      setResultados(data);
    } catch (err) {
      console.error("Error al obtener resultados:", err);
    }
  };

  const opcionesPorTipo = {
    "ver-resultados": [
      { value: "circuito", label: "Circuitos" },
      { value: "departamento", label: "Departamentos" },
      { value: "lista", label: "Listas" },
      { value: "partidos", label: "Partidos" },
    ]
  };

  const opciones = opcionesPorTipo[tipo] || [];

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">
        {tipo === "ver-resultados" ? "RESULTADOS" : "CIRCUITOS"}
      </Typography>

      <Box sx={{ mt: 4, width: "100%" }}>
        <FormControl fullWidth>
          <InputLabel id="categoria-label">Seleccione una opción</InputLabel>
          <Select
            labelId="categoria-label"
            value={categoria}
            label="Seleccione una opción"
            onChange={handleChange}
          >
            {opciones.map(({ value, label }) => (
              <MenuItem key={value} value={value}>
                {label}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {categoria && resultados.length > 0 && (
        <Box sx={{ mt: 4 }}>
<<<<<<< HEAD
          {/* contenido según categoría seleccionada */}
=======
          <Paper>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>{categoria.toUpperCase()}</TableCell>
                  <TableCell>Votos</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {resultados.map((item, index) => (
                  <TableRow key={index}>
                    <TableCell>{Object.values(item)[0]}</TableCell>
                    <TableCell>{Object.values(item)[1]}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </Paper>
>>>>>>> 361c5296bd1db0062737fe44a32b524a5e989dc7
        </Box>
      )}
    </FormContainer>
  );
};

export default VerResultados;
