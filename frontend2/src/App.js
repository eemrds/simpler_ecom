import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [products, setProducts] = useState([]);
  const link = 'http://localhost';
  const port = '8080';
  const url = `${link}:${port}`;

  useEffect(() => {
    fetch(`${url}/products`)
      .then(response => response.json())
      .then(data => setProducts(data.data))
      .catch(error => console.error('Error fetching data:', error));
  }, [url]);

  const handleBuy = (productId) => {
    fetch(`${url}/products`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ id: productId }),
    })
      .then(response => response.json())
      .then(data => {
        alert(data.message);
        // re-fetch products after buying to update the UI
        fetch(`${url}/products`)
          .then(response => response.json())
          .then(data => setProducts(data.data))
          .catch(error => console.error('Error fetching data:', error));
      })
      .catch(error => console.error('Error:', error));
  };

  return (
    <div className="App">
      <h1>Products</h1>
      <div id="productContainer">
        {products.map(product => (
          <div className="card" key={product.id}>
            <h2>{product.name}</h2>
            <img src={`./images/${product.image_link}`} alt={product.name} />
            <p>Price: ${product.price}</p>
            <p>Remaining: {product.amount_left}</p>
            <button onClick={() => handleBuy(product.id)}>Buy</button>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;