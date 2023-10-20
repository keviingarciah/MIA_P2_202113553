import React from 'react';

const Navbar = () => {
  return (
    <nav className="navbar bg-success navbar-lg">
      <div className="container-fluid">
      <a className="navbar-brand" style={{ color: 'white' }}>MIA | Proyecto 2</a>
        <form className="d-flex" role="login">
          <button className="btn btn-outline-light me-2" type="button">Iniciar Sesión</button>
        </form>
      </div>
    </nav>
  );
};

export default Navbar;
