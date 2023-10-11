require('dotenv').config();
const axios = require('axios');

const ip = process.env.API_IP;
const link = `http://${ip}:30080/`;
console.log(link)

let data = [] 
document.addEventListener('DOMContentLoaded', () => {
axios.get(link)
    .then(response => {
        data = response.data;
        data = [{name: 'test', image_link: 'test', price: 1, amount_left: 1}]
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
});

console.log(data)

data.forEach(product => {
    const card = document.createElement('div');
    card.className = 'card';
    
    const title = document.createElement('h2');
    title.innerText = product.name;

    const img = document.createElement('img');
    console.log(product.image_link);
    img.src = `./images/${product.image_link}`;

    const price = document.createElement('p');
    price.innerText = 'Price: $' + product.price;


    const amount = document.createElement('p');
    price.innerText = 'Remaining: ' + product.amount_left;

    const buyBtn = document.createElement('button');
    buyBtn.innerText = 'Buy';
    buyBtn.onclick = () => {
        fetch(link, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({id: product.id}),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    };
    
    card.appendChild(title);
    card.appendChild(img);
    card.appendChild(price);
    card.appendChild(buyBtn);
    
    productContainer.appendChild(card);
});