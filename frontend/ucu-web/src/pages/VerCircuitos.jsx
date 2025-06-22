import { Typography, Box } from "@mui/material";
import FormContainer from "../components/FormContainer";

const VerCircuito = () => {
  return (
    <FormContainer>
      <Typography variant="h5" gutterBottom align="center">CIRCUITO</Typography>
      <Box sx={{ mt: 2 }}>
        <Typography variant="body1"><strong>CIRCUITO:</strong> XXXX</Typography>
        <Typography variant="body1" sx={{ mt: 2 }}><strong>UBICACIÓN:</strong> XXXX</Typography>
      </Box>
    </FormContainer>
  );
};

export default VerCircuito;
