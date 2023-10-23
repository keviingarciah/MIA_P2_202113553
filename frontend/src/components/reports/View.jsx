import React from 'react';
import Dropdown from 'react-bootstrap/Dropdown';

const View = () => {
  return (
    <div className="card">
      <div className="card-body bg-success-subtle">        
          <Dropdown>
            <Dropdown.Toggle variant="success" id="dropdown-basic" style={{ width: '100%' }} className="btn-lg">
              Seleccionar reporte
            </Dropdown.Toggle>

            <Dropdown.Menu style={{ width: '100%' }}>
              
            </Dropdown.Menu>
          </Dropdown>       
      </div>
    </div>
  );
};

export default View;
