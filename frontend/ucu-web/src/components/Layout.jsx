import { Box } from "@mui/material";
import Sidebar from "./Sidebar";

import EleccionesForm from "../pages/EleccionesForm";
import ListaForm from "../pages/ListaForm";
import CandidatosForm from "../pages/CandidatosForm";
import CircuitosForm from "../pages/CircuitosForm";


import VerCircuito from "../pages/VerCircuitos";
import Votar from "../pages/Votar";
import VerResultados from "../pages/VerResultados";

const Layout = ({ currentPage, setCurrentPage }) => {
  const renderContent = () => {
    switch (currentPage) {
      case "elecciones": return <EleccionesForm />;
      case "listas": return <ListaForm />;
      case "candidatos": return <CandidatosForm />;
      case "circuitos": return <CircuitosForm />;
      case "ver-circuito": return <VerCircuito />;
      case "votar": return <Votar />;
      case "ver-resultados": return <VerResultados />;
      default: return <div>Seleccioná una opción</div>;
    }
  };

  return (
    <Box sx={{ display: "flex", flexGrow: 1 }}>
      <Sidebar setCurrentPage={setCurrentPage} />
      <Box sx={{ flexGrow: 1, p: 4 }}>{renderContent()}</Box>
    </Box>
  );
};

export default Layout;
