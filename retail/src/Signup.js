import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import SuccessMessage from './SuccessMessage';

function SignUp( user, setUser) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [passwordConfirmation, setPasswordConfirmation] = useState('');
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  const handleSubmit = (e) => {
    e.preventDefault();

    // Validation for user, email, password and password confirmation
    if (!username || !email || !password || !passwordConfirmation) {
      setError('All fields are required');
      return;
    }

    // Validation for password
    if (password !== passwordConfirmation) {
      setError('Password and confirmation do not match');

      setTimeout(() => {
        setError(null);
      }, 3000);

      return;
    }

    // Fetch request
    fetch('/api/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        email,
        password,
        password_confirmation: passwordConfirmation,
      }),
    })
      .then((response) => {
        if (response.ok) {
          // User creation successful
          setSuccessMessage(`${username} has been created. Please log in.`);
          // Clear the form
          setUsername('');
          setEmail('');
          setPassword('');
          setPasswordConfirmation('');

          setTimeout(() => {
            setSuccessMessage(null);
          }, 5000);
        } else {
          response.json().then((data) => {
            setError(data.error || 'An error occurred during signup.');
          });
        }
      })
      .catch((error) => {
        console.error('Error during signup:', error);
        // Handle errors as needed
        setError('An error occurred during signup.');
      });
  };

  return (
    <Paper
      elevation={3}
      style={{
        padding: '20px',
        position: 'absolute', 
        top: '64px', 
        left: 0,
        width: '100%',
        height: 'calc(100% - 64px)',
        backgroundImage: 'url("https://static.vecteezy.com/system/resources/previews/007/719/484/original/flat-illustration-of-work-desk-with-cup-of-coffee-and-notebook-vector.jpg")',
        backgroundSize: 'cover',
        minHeight: '100vh',
        display: 'center',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
      }}
    >
      {successMessage && (
        <SuccessMessage
          message={successMessage}
          timeout={4000}
          redirectPath="/login"
        />
      )}
      <Typography variant="h4" gutterBottom style={{ color: 'black' }}>
        Sign Up
      </Typography>
      <Typography variant="body1" gutterBottom style={{ color: 'black' }}>
        Start your cafe-hopping journey by signing up! 
      </Typography>
      {error && <Typography variant="body2" style={{ color: 'red' }}>{error}</Typography>}
      <form onSubmit={handleSubmit} style={{ width: '300px', textAlign: 'center' }}>
        <TextField
          type="text"
          label="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          fullWidth
          margin="normal"
          required
        />
        <TextField
          type="text"
          label="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          fullWidth
          margin="normal"
          required
        />
        <TextField
          type="password"
          label="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          fullWidth
          margin="normal"
          required
        />
        <TextField
          type="password"
          label="Password Confirmation"
          value={passwordConfirmation}
          onChange={(e) => setPasswordConfirmation(e.target.value)}
          fullWidth
          margin="normal"
          required
        />
        <Typography variant="body2" gutterBottom style={{ color: 'black' }}>
        Already have an account? Click Log In to log in and jump back into your cafe-hopping experience!
      </Typography>
        <Button type="submit" variant="contained" color="primary" style={{ marginTop: '20px', color: "white", fontWeight: 'bold' }}>
          Sign Up
        </Button>
        <Button type="submit" variant="contained" color="primary" style={{ marginTop: '20px', marginLeft: '40px'}}>
          <NavLink to="/login" style={{ textDecoration: 'none', color: 'white', fontWeight: 'bold', fontSize: '1.0em' }}>
            Log In
          </NavLink>
        </Button>

        
      </form>
    </Paper>
  );
}

export default SignUp;
