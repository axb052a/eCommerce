// ProductDetail.js

import React from 'react';

const ProductDetail = ({ product }) => {
  return (
    <div>
      <h2>Product Detail</h2>
      <div>
        <h3>{product.name}</h3>
        <p>{product.description}</p>
        <p>Price: ${product.price}</p>
      </div>
    </div>
  );
}

export default ProductDetail;
