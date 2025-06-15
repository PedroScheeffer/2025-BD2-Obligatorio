import { Typography, FormGroup, FormControlLabel, Checkbox, Button, Box } from "@mui/material";
import { useState } from "react";
import FormContainer from "../components/FormContainer";

const opciones = [
  "Lista 1 - Partido A",
  "Lista 2 - Partido B",
  "Lista 3 - Partido A",
  "Blanco",
  "Anulado"
];

const Votar = () => {
  const [seleccionado, setSeleccionado] = useState("");

  const handleChange = (opcion) => {
    setSeleccionado(opcion);
  };

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">VOTAR</Typography>
      <Box sx={{ display: "flex", justifyContent: "center", mt: 2 }}>
        <FormGroup >
        {opciones.map((op) => (
          <FormControlLabel
            key={op}
            control={
              <Checkbox
                checked={seleccionado === op}
                onChange={() => handleChange(op)}
                sx={{
                    "&.Mui-checked": { color: "success.main" },
                  }}
              />
            }
            label={op}
          />
        ))}
      </FormGroup>
      </Box>
      <Box sx={{ mt: 3, display: "flex", justifyContent: "space-around" }}>
        <Button variant="contained" color="success">Votar</Button>        
        <Button variant="contained" color="error">Cancelar</Button>
      </Box>
    </FormContainer>
  );
};

export default Votar;
