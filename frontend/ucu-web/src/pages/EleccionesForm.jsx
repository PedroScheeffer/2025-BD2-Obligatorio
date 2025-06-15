import { Box, Typography, TextField, Button, MenuItem } from "@mui/material";
import FormContainer from "../components/FormContainer";
import { useState } from "react";

const EleccionesForm = () => {
  const [tipo, setTipo] = useState("");
  const [fecha, setFecha] = useState("");

  const tiposEleccion = ["Nacional", "Departamental", "Municipal"];

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">
        CARGAR ELECCIONES
      </Typography>
      <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
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
          <Button variant="contained" color="success">
            Aceptar
          </Button>
          <Button variant="contained" color="error">
            Cancelar
          </Button>
        </Box>
      </Box>
    </FormContainer>
  );
};

export default EleccionesForm;
