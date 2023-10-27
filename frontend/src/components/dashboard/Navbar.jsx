import React from 'react';
import { Link } from 'react-router-dom';

import { useLogged } from '../login/Logged';

const Navbar = () => {
  const { isLogged, setToTrue, setToFalse } = useLogged();

  const handleReportLinkClick = () => {
    if (!isLogged) {
      alert('[ERROR] Debes iniciar sesión para ver los reportes.');
    }
  };

  const handleLoginLinkClick = () => {
    if (isLogged) {
      alert('[ERROR] Hay una sesión iniciada.');
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
              {isLogged ? (
                <Link to="/reports" className="nav-link text-white" onClick={handleReportLinkClick}>
                  Reportes
                </Link>
              ) : (
                <a href="#/" className="nav-link text-white" onClick={handleReportLinkClick}>
                  Reportes
                </a>
              )}
            </li>
          </ul>
        </div>

        <form className="d-flex" role="login">
          {isLogged ? (
            <a href="#/" className="btn btn-outline-light me-2" onClick={handleLoginLinkClick}>
              Iniciar Sesión
            </a>
          ) : (
            <Link to="/login" className="btn btn-outline-light me-2">
              Iniciar Sesión
            </Link>
          )}
        </form>
      </div>
    </nav>
  );
};

export default Navbar;
