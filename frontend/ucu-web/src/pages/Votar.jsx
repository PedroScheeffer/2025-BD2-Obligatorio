import { Typography, FormGroup, FormControlLabel, Checkbox, Button, Box } from "@mui/material";
import { useState } from "react";
import FormContainer from "../components/FormContainer";

const opciones = [
  "LISTA 1 - PARTIDO A",
  "LISTA 2 - PARTIDO B",
  "LISTA 3 - PARTIDO A",
  "BLANCO",
  "ANULADO"
];

const Votar = () => {
  const [seleccionado, setSeleccionado] = useState("");

  const handleChange = (opcion) => {
    setSeleccionado(opcion);
  };

  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">VOTAR</Typography>
      <FormGroup>
        {opciones.map((op) => (
          <FormControlLabel
            key={op}
            control={
              <Checkbox
                checked={seleccionado === op}
                onChange={() => handleChange(op)}
              />
            }
            label={op}
          />
        ))}
      </FormGroup>
      <Box sx={{ mt: 2, display: "flex", justifyContent: "center" }}>
        <Button variant="contained" color="success">Votar</Button>
      </Box>
    </FormContainer>
  );
};

export default Votar;
