import { useState } from "react";
import { Box } from "@mui/material";
import Header from "./components/Header";
import Layout from "./components/Layout";
import Login from "./pages/Login";
import Votar from "./pages/Votar";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [rol, setRol] = useState(null); 
  const [currentPage, setCurrentPage] = useState("elecciones");
  const [persona, setPersona] = useState(null);

  const handleLogin = (selectedRol, data) => {
    setRol(selectedRol);
    setIsLoggedIn(true);
    setPersona(data.persona); 

    if (selectedRol === "funcionario") {
      setCurrentPage("funcionarioLayout"); 
    } else if (selectedRol === "votante") {
      setCurrentPage("votar");
    }

    console.log("Usuario logueado:", data.persona);
  };

  return (
    <Box sx={{ width: "100%", height: "100vh", display: "flex", flexDirection: "column" }}>
      <Header persona={persona}/>
      {!isLoggedIn ? (
        <Login onLogin={handleLogin} />
      ) : rol === "funcionario" ? (
        <Layout currentPage={currentPage} setCurrentPage={setCurrentPage} />
      ) : currentPage === "votar" ? (
        <Box sx={{ p: 4 }}>
          <Votar persona={persona} />
        </Box>
      ) : (
        <Box sx={{ p: 4 }}>
          <div>Cargando...</div>
        </Box>
      )}
    </Box>
  );
}

export default App;
