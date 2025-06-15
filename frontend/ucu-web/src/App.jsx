import { useState } from "react";
import { Box } from "@mui/material";
import Header from "./components/Header";
import Layout from "./components/Layout";

function App() {
  const [currentPage, setCurrentPage] = useState("elecciones");

  return (
    <Box sx={{ width: "100%", height: "100vh", display: "flex", flexDirection: "column" }}>
      <Header />
      <Layout currentPage={currentPage} setCurrentPage={setCurrentPage} />
    </Box>
  );
}

export default App;
