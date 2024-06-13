// Cart.js

import React from 'react';

const Cart = ({ cartItems, removeFromCart, updateCart }) => {
  return (
    <div>
      <h2>Shopping Cart</h2>
      <ul>
        {cartItems.map(item => (
          <li key={item.id}>
            <div>
              <h3>{item.name}</h3>
              <p>Quantity: {item.quantity}</p>
              <button onClick={() => removeFromCart(item.id)}>Remove</button>
            </div>
          </li>
        ))}
      </ul>
      <button onClick={updateCart}>Update Cart</button>
    </div>
  );
}

export default Cart;
