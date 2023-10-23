import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar bg-success navbar-expand-lg">
      <div className="container-fluid">
        <a className="navbar-brand" style={{ color: 'white' }}>MIA | Proyecto 2</a>
      
        <div class="collapse navbar-collapse" id="navbarNavDropdown">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <Link to="/reports" className="nav-link text-white">Reportes</Link>
                </li>
            </ul>    
        </div>        

        <form className="d-flex" role="login">          
            <Link to="/login" className="btn btn-outline-light me-2">Iniciar Sesión</Link>
        </form>
      </div>
    </nav>
  );
};

export default Navbar;
