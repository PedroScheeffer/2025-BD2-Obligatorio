import React, { useState } from "react";
import { Box, TextField, MenuItem, Typography, Button } from "@mui/material";

function Login({ onLogin }) {
  const [credencial, setCredencial] = useState("");
  const [password, setPassword] = useState("");
  const [rol, setRol] = useState("votante");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://localhost:8000/api/login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          credencial,
          contrasena: password,
          rol,
        }),
      });

      if (!response.ok) {
        throw new Error("Credenciales inválidas");
      }

      const data = await response.json();

      localStorage.setItem("cc", data.persona.cc);
      if (rol === "votante" && data.id_circuito) {
        localStorage.setItem("id_circuito", data.id_circuito);
      }

      onLogin(rol, data);
    } catch (err) {
      alert("Error de login: " + err.message);
    }
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
