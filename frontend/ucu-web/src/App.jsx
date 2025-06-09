import { useState } from "react";
import { Tabs, Tab, Box } from "@mui/material";
import "./App.css";

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(true);
  const [tabIndex, setTabIndex] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabIndex(newValue);
  };

  if (!isLoggedIn) {
    return <div>Please log in to access the app.</div>;
  }

  return (
    <Box sx={{ width: "100%" }}>
      <TextField>clean bs </TextField>
    </Box>
  );
}

export default App;
