import React from 'react';
import { Link } from 'react-router-dom';

const API = import.meta.env.VITE_APP_BACKEND;

const Navbar = () => {
  // Modifica handleSessionCheck para que retorne el valor de data.logged
  const handleSessionCheck = async () => {
    try {
      const response = await fetch(`${API}/session`);

      if (response.ok) {
        const data = await response.json();
        console.log("Estado de la sesión:", data.logged);
        return data.logged;
      } else {
        console.error("Error al obtener el estado de la sesión");
        return false;
      }
    } catch (error) {
      console.error("Error de red:", error);
      return false;
    }
  };

  const handleReportButtonClick = async () => {
    // Realizar la petición al backend cuando se hace clic en el botón "Reportes".
    const isLogged = await handleSessionCheck();
    if (isLogged) {
      // Redirige a la página de informes
      window.location.href = '/reports';
    } else {
      alert('[ERROR] Debes iniciar sesión para ver los reportes.');
      window.location.href = '#/';
    }
  };


  return (
    <nav className="navbar bg-success navbar-expand-lg">
      <div className="container-fluid">
        <a className="navbar-brand" style={{ color: 'white' }}>
          MIA | Proyecto 2
        </a>

        <div className="collapse navbar-collapse" id="navbarNavDropdown">
          <ul className="navbar-nav">
            <li className="nav-item">
              <button className="nav-link text-white" onClick={handleReportButtonClick}>
                Reportes
              </button>
            </li>
          </ul>
        </div>

        <form className="d-flex" role="login">
          <Link to="/login" className="btn btn-outline-light me-2">
              Iniciar Sesión
          </Link>
        </form>
      </div>
    </nav>
  );
};

export default Navbar;
