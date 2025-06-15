import React from "react";
import "./Login.css";
import votoImg from "./voto.png";

function Login() {
  return (
    <div>
      <h1>Sistema de Votaciones Electrónicas</h1>
      <form>
        <input type="text" placeholder="Credencial Cívica" />
        <input type="password" placeholder="Contraseña" />
        <label htmlFor="rol">Rol:</label>
        <select id="rol" name="rol">
          <option value="votante">Votante</option>
          <option value="funcionario">Funcionario</option>
        </select>
        <button type="submit">Ingresar</button>
      </form>
    </div>
  );
}

export default Login;
