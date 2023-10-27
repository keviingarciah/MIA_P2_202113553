import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'

import { LoggedProvider } from './components/login/Logged.jsx'; // Importa tu proveedor de contexto
import { BrowserRouter} from 'react-router-dom';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <LoggedProvider>
        <App />
      </LoggedProvider>      
    </BrowserRouter>
  </React.StrictMode>,
)
