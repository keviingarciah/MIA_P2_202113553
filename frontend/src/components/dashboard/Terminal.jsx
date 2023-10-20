import React from 'react';

const Terminal = () => {
  return (
    <div className="card">
      <div className="card-body bg-body-tertiary">
        <div className="d-flex justify-content-end mb-3">
          <button type="button" className="btn btn-success me-3">Ejecutar</button>
        </div>
        <div className="mb-3">
          <input class="form-control" id="formFileLg" type="file"/>
        </div>
        <div className="mb-3">
          <label htmlFor="exampleFormControlInput1" className="form-label form-label-lg">Entrada</label>
          <textarea className="form-control" id="exampleFormControlTextarea1" rows="7"></textarea>
        </div>
        <div className="mb-3">
          <label htmlFor="exampleFormControlTextarea1" className="form-label">Salida</label>
          <textarea className="form-control" id="exampleFormControlTextarea1" rows="7"></textarea>
        </div>
      </div>
    </div>
  );
};

export default Terminal;
