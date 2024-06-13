import React from 'react';
import Button from '@mui/material/Button';
import { useNavigate } from 'react-router-dom';

const Logout = ({ setUser }) => {
  const navigate = useNavigate();

  function handleLogOut() {
    fetch("/api/logout", {
      method: "DELETE",
      credentials: 'include',  
    }).then((r) => {
      if (r.ok) {
        setUser(null);
        navigate.push("/");
      }
    });
  }

  return <Button variant="contained" color="secondary" onClick={handleLogOut}>Logout</Button>;
}

export default Logout;