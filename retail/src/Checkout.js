// Checkout.js

import React, { useState } from 'react';

const Checkout = ({ cartItems, onCheckout }) => {
  const [address, setAddress] = useState('');

  const handleCheckout = () => {
    // Perform validation if needed
    // For simplicity, we directly pass the address to the parent component
    onCheckout(address);
  };

  return (
    <div>
      <h2>Checkout</h2>
      <ul>
        {cartItems.map(item => (
          <li key={item.id}>
            <div>
              <h3>{item.name}</h3>
              <p>Quantity: {item.quantity}</p>
            </div>
          </li>
        ))}
      </ul>
      <input type="text" placeholder="Address" value={address} onChange={(e) => setAddress(e.target.value)} />
      <button onClick={handleCheckout}>Checkout</button>
    </div>
  );
}

export default Checkout;
