import React from 'react';

const Login = () => {
  return (
    <div className="d-flex justify-content-center align-items-center min-vh-100">
      <div className="card p-4" style={{ backgroundColor: '#C7EA46' }}>
        <h3 className="text-center mb-4">Iniciar Sesión</h3>
        <form>
          <div className="mb-3">
            <label htmlFor="partitionId" className="form-label text-white">ID Partición</label>
            <input type="text" className="form-control" id="partitionId" />
          </div>
          <div className="mb-3">
            <label htmlFor="username" className="form-label text-white">Usuario</label>
            <input type="text" className="form-control" id="username" />
          </div>
          <div className="mb-3">
            <label htmlFor="password" className="form-label text-white">Contraseña</label>
            <input type="password" className="form-control" id="password" />
          </div>
          <button type="submit" className="btn btn-primary d-block w-100">Ingresar</button>
        </form>
      </div>
    </div>
  );
};

export default Login;