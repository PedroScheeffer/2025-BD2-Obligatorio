import { Box, Typography, TextField, Button, MenuItem } from "@mui/material";
import FormContainer from "../components/FormContainer";
import { useState } from "react";

const EleccionesForm = () => {
  const [tipo, setTipo] = useState("");
  const [fecha, setFecha] = useState("");

  const tiposEleccion = ["Nacional", "Departamental", "Municipal", "Plebiscito", "Ballotage", "Referendum"];

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/elecciones", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          tipo,
          fecha,
        }),
      });

      if (!response.ok) {
        throw new Error("Error al cargar la elección");
      }

      alert("Elección cargada exitosamente");
      setTipo("");
      setFecha("");
    } catch (err) {
      alert("Error: " + err.message);
    }
  };

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">
        CARGAR ELECCIONES
      </Typography>
      <Box
        component="form"
        onSubmit={handleSubmit}
        sx={{ display: "flex", flexDirection: "column", gap: 2 }}
      >
        <TextField
          select
          label="Tipo de elección"
          value={tipo}
          onChange={(e) => setTipo(e.target.value)}
          fullWidth
        >
          {tiposEleccion.map((option) => (
            <MenuItem key={option} value={option}>
              {option}
            </MenuItem>
          ))}
        </TextField>

        <TextField
          label="Fecha"
          type="date"
          InputLabelProps={{ shrink: true }}
          value={fecha}
          onChange={(e) => setFecha(e.target.value)}
          fullWidth
        />

        <Box sx={{ display: "flex", justifyContent: "space-around", mt: 2 }}>
          <Button variant="contained" color="success" onClick={handleSubmit}>
            Aceptar
          </Button>
          <Button
            variant="contained"
            color="error"
            onClick={() => {
              setTipo("");
              setFecha("");
            }}
          >
            Cancelar
          </Button>
        </Box>
      </Box>
    </FormContainer>
  );
};

export default EleccionesForm;
