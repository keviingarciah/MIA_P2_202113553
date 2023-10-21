import React from 'react';
import { Link } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav className="navbar bg-success navbar-expand-lg">
      <div className="container-fluid">
        <a className="navbar-brand" style={{ color: 'white' }}>MIA | Proyecto 2</a>
      
        <div className="collapse navbar-collapse" id="navbarNavDropdown">
            <ul className="navbar-nav">
                <li className="nav-item">                    
                    <Link to="/" className="nav-link text-white">Dashboard</Link>
                </li>
            </ul>    
        </div>        
      </div>
    </nav>
  );
};

export default Navbar;
