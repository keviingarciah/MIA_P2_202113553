import React from 'react'
import Navbar from './Navbar';
import Terminal from './Terminal';

const Dashboard = () => {
  return (   
    <div> 
      <Navbar /> 
      <div className="container-fluid mt-4">
        <Terminal />
      </div>  
    </div>    
  )              
}

export default Dashboard