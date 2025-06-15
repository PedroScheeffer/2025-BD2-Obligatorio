import React, { useState } from "react";
import { Box, TextField, MenuItem, Typography, Button } from "@mui/material";

function Login({ onLogin }) {
  const [credencial, setCredencial] = useState("");
  const [password, setPassword] = useState("");
  const [rol, setRol] = useState("votante");

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(rol);
  };

  return (
    <Box sx={{ display: "flex", height: "calc(100vh - 95px)" }}>
      <Box
        sx={{
          flex: 3,
          backgroundColor: "#fff8e1", 
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{
            display: "flex",
            flexDirection: "column",
            width: "80%",
            maxWidth: 400,
          }}
        >
          <Typography variant="h5" gutterBottom align="center" sx={{ mb: 6 }}>
            Sistema de Votaciones Electrónicas
          </Typography>
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2 }}>
            <TextField
              label="Credencial Cívica"
              value={credencial}
              onChange={(e) => setCredencial(e.target.value)}
              fullWidth
            />
            <TextField
              label="Contraseña"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              fullWidth
            />
            <TextField
              select
              label="Rol"
              value={rol}
              onChange={(e) => setRol(e.target.value)}
              fullWidth
            >
              <MenuItem value="votante">Votante</MenuItem>
              <MenuItem value="funcionario">Funcionario</MenuItem>
            </TextField>
          </Box>
            <Button type="submit" variant="contained" color="success" sx={{ mt: 7 }}>Ingresar</Button>
        </Box>
      </Box>

    <Box sx={{ flex: 2, display: "flex", alignItems: "center", justifyContent: "center" }}>
      <img
        src="/voto.png"
        alt="Voto ilustración"
        style={{
          width: "100%",
          height: "100%",
          opacity: "60%",
          objectFit: "cover",
        }}
      />
    </Box>
    </Box>
  );
}

export default Login;
