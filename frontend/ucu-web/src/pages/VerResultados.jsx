import { Typography, Box, List, ListItem, ListItemButton, ListItemText } from "@mui/material";
import FormContainer from "../components/FormContainer";

const VerResultados = () => {
  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">RESULTADOS</Typography>

      <Box sx={{ mt: 4 }}>
        <Typography variant="subtitle1" sx={{ mb: 1 }}>Ver por categoría:</Typography>
        <List>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemText primary="Circuito" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemText primary="Departamento" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemText primary="Lista" />
            </ListItemButton>
          </ListItem>
          <ListItem disablePadding>
            <ListItemButton>
              <ListItemText primary="Partidos" />
            </ListItemButton>
          </ListItem>
        </List>
      </Box>
    </FormContainer>
  );
};

export default VerResultados;
