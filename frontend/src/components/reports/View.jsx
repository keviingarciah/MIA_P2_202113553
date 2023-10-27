import React, { useState, useEffect } from 'react';
import Dropdown from 'react-bootstrap/Dropdown';

const API = import.meta.env.VITE_APP_BACKEND
const Bucket = import.meta.env.VITE_APP_BUCKET_REPORTS

const View = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [reportList, setReportList] = useState([]); // Estado para la lista de reportes

  useEffect(() => {
    // Realiza la solicitud al cargar el componente
    fetch(`${API}/reports`) // Ruta de la API Flask
      .then((response) => response.json())
      .then((data) => setReportList(data.reports))
      .catch((error) => console.error('Error:', error));
  }, []); // El segundo argumento [] garantiza que useEffect se ejecute solo una vez al cargar el componente

  const handleFileSelect = (fileName) => {
    setSelectedFile(fileName);
  };
  
  return (
    <div className="card mb-4">
      <div className="card-body bg-success-subtle">
        <div className="row mb-3">
          <div className="col-12">
            <Dropdown>
              <Dropdown.Toggle variant="success" id="dropdown-basic" style={{ width: '100%' }} className="btn-lg">
                Seleccionar reporte
              </Dropdown.Toggle>

              <Dropdown.Menu style={{ width: '100%' }}>                
                {reportList.map((reportName, index) => (
                    <Dropdown.Item key={index} onClick={() => handleFileSelect(reportName)}>
                      {reportName}
                    </Dropdown.Item>
                  ))}                
              </Dropdown.Menu>
            </Dropdown>
          </div>        
        </div>

        
          <div className="mb-3" style={{ display: 'flex' }}>            
              <img
                //src={`URL_de_la_Imagen/${selectedFile}`}
                src={`${Bucket}/${selectedFile}`}
                alt="  "
                style={{ width: '100%' }} // Ajustar el ancho al 100%
              />          
          </div>
        
      </div>
    </div>
  );
};

export default View;
