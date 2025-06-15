import { useState } from "react";
//import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Box } from "@mui/material";
import Header from "./components/Header";
import Layout from "./components/Layout";
import Login from "./pages/Login";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [rol, setRol] = useState(null); // "votante" o "funcionario"
  const [currentPage, setCurrentPage] = useState("elecciones");

  const handleLogin = (selectedRol) => {
    setRol(selectedRol);
    setIsLoggedIn(true);
  };

  return (
    <Box sx={{ width: "100%", height: "100vh", display: "flex", flexDirection: "column" }}>
      <Header />
      {!isLoggedIn ? (
        <Login onLogin={handleLogin} />
      ) : rol === "funcionario" ? (
        <Layout currentPage={currentPage} setCurrentPage={setCurrentPage} />
      ) : (
        <Box sx={{ p: 4 }}>
          <h2>Bienvenido, votante</h2>
          {/* Acá podrías renderizar algo especial para el votante */}
        </Box>
      )}
    </Box>
  );
}

export default App;

