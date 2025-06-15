import "../styles/Sidebar.css";
import { Button } from "@mui/material";

const Sidebar = ({ setCurrentPage }) => {
  return (
    <div className="sidebar">
      <Button onClick={() => setCurrentPage("elecciones")}>Cargar elecciones</Button>
      <Button onClick={() => setCurrentPage("listas")}>Cargar listas</Button>
      <Button onClick={() => setCurrentPage("candidatos")}>Cargar candidatos</Button>
      <Button onClick={() => setCurrentPage("circuitos")}>Cargar circuitos</Button>
    </div>
  );
};

export default Sidebar;