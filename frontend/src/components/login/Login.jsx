import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const API = import.meta.env.VITE_APP_BACKEND;

const Login = () => {
  const [user, setUser] = useState('');
  const [password, setPassword] = useState('');
  const [partitionId, setPartitionId] = useState('');

  const history = useNavigate();
  
  const handleLogin = async () => {
    // Construir el cuerpo de la solicitud con los datos del usuario
    const requestBody = {
      username: user,
      password: password,
      id: partitionId,
    };

    try {
      const response = await fetch(`${API}/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(requestBody),
      });

      if (response.ok) {
        const data = await response.text();
        if (data.includes('[ERROR]')) {
          //console.error('Error en la solicitud:', data);
          alert("[ERROR] Ocurrió un error al iniciar sesión.");       

        } else if (data.includes('[EXITOSO]')) {
          //console.log('Solicitud exitosa:', data);
          alert("[EXITOSO] Inicio de sesión correcto.");

          // Redirige a la página de informes        
          history('/reports');
          
        } else {
          //console.error('Respuesta inesperada:', data);
          alert("[ERROR] Ocurrió un error al iniciar sesión.");       
          
        }
      } else {
        // Si la respuesta no es exitosa, puedes manejar el error aquí
        console.error('Error en la solicitud.');
      }
    } catch (error) {
      // Si hay un error al hacer la solicitud, puedes manejarlo aquí
      console.error('Error:', error);
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center min-vh-100 bg-light">
      <div className="card p-4 bg-success">
        <h3 className="text-center mb-4 text-light">Iniciar Sesión</h3>
        <form>
          <div className="mb-3">
            <label htmlFor="partitionId" className="form-label text-white">ID Partición</label>
            <input
              type="text"
              className="form-control"
              id="partitionId"
              onChange={(e) => setPartitionId(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="username" className="form-label text-white">Usuario</label>
            <input
              type="text"
              className="form-control"
              id="username"
              onChange={(e) => setUser(e.target.value)}
            />
          </div>
          <div className="mb-3">
            <label htmlFor="password" className="form-label text-white">Contraseña</label>
            <input
              type="password"
              className="form-control"
              id="password"
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <button
            type="button"
            className="btn btn-outline-light d-block w-100"
            onClick={handleLogin}
          >
            Ingresar
          </button>        
          <Link to="/" className="btn btn-outline-light d-block w-100 mt-2">Regresar</Link>
        </form>
      </div>
    </div>
  );
};

export default Login;
