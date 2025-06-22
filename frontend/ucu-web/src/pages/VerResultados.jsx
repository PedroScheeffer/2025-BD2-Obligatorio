import React, { useState } from "react";
import { Typography, Box, Select, MenuItem, FormControl, InputLabel } from "@mui/material";
import FormContainer from "../components/FormContainer";

const VerResultados = ({ tipo }) => {
  const [categoria, setCategoria] = useState("");

  const handleChange = (event) => {
    setCategoria(event.target.value);
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

      {categoria && (
        <Box sx={{ mt: 4 }}>
          {/* contenido según categoría seleccionada */}
        </Box>
      )}
    </FormContainer>
  );
};

export default VerResultados;
