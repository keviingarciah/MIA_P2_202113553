import React, { useState } from 'react';

const Terminal = () => {
  const [inputText, setInputText] = useState(''); // Estado para almacenar el contenido del archivo

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = (event) => {
      const fileContent = event.target.result; // Contenido del archivo

      setInputText(fileContent); // Actualiza el estado con el contenido del archivo
    };

    reader.readAsText(file);
  };

  const handleTextareaChange = (e) => {
    const newText = e.target.value; // Nuevo contenido del textarea

    setInputText(newText); // Actualiza el estado con el nuevo contenido
  };

  return (
    <div className="card">
      <div className="card-body bg-success-subtle">
        <div className="row mb-3">
          <div className="col-11">
            <input
              className="form-control"
              id="formFileLg"
              type="file"
              onChange={handleFileChange}
            />
          </div>
          <div className="col-1">
            <button type="button" className="btn btn-success me-3">
              Ejecutar
            </button>
          </div>
        </div>
        <div className="mb-3">
          <label htmlFor="exampleFormControlInput1" className="form-label form-label-lg">
            Entrada
          </label>
          <textarea
            className="form-control"
            id="exampleFormControlTextarea1"
            rows="8"
            value={inputText} // Asigna el valor del estado al textarea
            onChange={handleTextareaChange} // Maneja los cambios en el textarea
          ></textarea>
        </div>
        <div className="mb-3">
          <label htmlFor="exampleFormControlTextarea1" className="form-label">
            Salida
          </label>
          <textarea className="form-control" id="exampleFormControlTextarea1" rows="8"></textarea>
        </div>
      </div>
    </div>
  );
};

export default Terminal;
