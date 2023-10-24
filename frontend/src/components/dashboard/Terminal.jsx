import React, { useState } from 'react';
const API = import.meta.env.VITE_APP_BACKEND

const Terminal = () => {
  const [inputText, setInputText] = useState('');
  const [outputText, setOutputText] = useState('');
  const [isExecuting, setIsExecuting] = useState(false); // Estado para el indicador de ejecución

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();

    reader.onload = (event) => {
      const fileContent = event.target.result;
      setInputText(fileContent);
    };

    reader.readAsText(file);
  };

  const handleTextareaChange = (e) => {
    const newText = e.target.value;
    setInputText(newText);
  };

  const executeCode = async () => {
    setOutputText(''); // Limpia el contenido de salida

    if (isExecuting) {
      return;
    }
  
    setIsExecuting(true);
  
    const inputLines = inputText.split('\n');
    const outputLines = [];
    let currentIndex = 0;
    
    while (currentIndex < inputLines.length) {
      const line = inputLines[currentIndex].trim();
      
      if (line.toLowerCase() === "pause") {
        alert("Se encontró la palabra 'pause'. La ejecución se detendrá temporalmente.");
        currentIndex++; // Salta a la siguiente línea
        continue; // Salta al siguiente ciclo del bucle
      }
  
      try {
        const response = await fetch(`${API}/execute`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ inputText: line }),
        });
  
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
  
        const data = await response.json();
        if (data.message) {
          outputLines.push(data.message);
          setOutputText(outputLines.join('\n'));
        } else {
          console.error('Response does not contain the expected message:', data);
        }
      } catch (error) {
        console.error('Error:', error);
        outputLines.push(`Error: ${error.message}`);
      }
  
      currentIndex++; // Avanza al siguiente índice para procesar la siguiente línea
    }
    
    setIsExecuting(false);
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
            <button
              type="button"
              className="btn btn-success me-3"
              onClick={executeCode} // Llama a executeCode al hacer clic en el botón
            >
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
            value={inputText}
            onChange={handleTextareaChange}
            spellCheck="false" // Desactivar revisión ortográfica
          ></textarea>
        </div>
        <div className="mb-3">
          <label htmlFor="exampleFormControlTextarea1" className="form-label">
            Salida
          </label>
          <textarea
            className="form-control"
            id="exampleFormControlTextarea1"
            rows="8"
            readOnly // Hace que el textarea sea de solo lectura
            value={outputText} // Muestra el contenido de salida en el textarea
            spellCheck="false" // Desactivar revisión ortográfica
          ></textarea>
        </div>
      </div>
    </div>
  );
};

export default Terminal;
