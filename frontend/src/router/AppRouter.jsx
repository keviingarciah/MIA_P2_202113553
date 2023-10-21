import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Dashboard from '../components/dashboard/Dashboard';
import Login from '../components/login/Login';
import Reports from '../components/reports/Reports';

const AppRouter = () => {
    return (   
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/login" element={<Login />} />
        <Route path="/reports" element={<Reports />} />
       </Routes> 
    )              
  }
  
  export default AppRouter