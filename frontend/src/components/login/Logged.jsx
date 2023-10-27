import React, { createContext, useContext, useState } from 'react';

const LoggedContext = createContext();

export const useLogged = () => {
  return useContext(LoggedContext);
};

export const LoggedProvider = ({ children }) => {
  const [isLogged, setIsLogged] = useState(false);

  const setToTrue = () => {
    setIsLogged(true);
  };

  const setToFalse = () => {
    setIsLogged(false);
  };

  return (
    <LoggedContext.Provider value={{ isLogged, setToTrue, setToFalse }}>
      {children}
    </LoggedContext.Provider>
  );
};
