import React, { useEffect } from 'react';
import { Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom';

const SuccessMessage = ({ message, timeout, redirectPath }) => {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      // Redirect to the specified path after the timeout
      navigate(redirectPath);
    }, timeout);

    // Clear the timer when the component is unmounted
    return () => clearTimeout(timer);
  }, [timeout, redirectPath, navigate]);

  return (
    <Typography variant="body1" style={{ color: 'green', marginBottom: '10px' }}>
      {message}
    </Typography>
  );
};

export default SuccessMessage;
