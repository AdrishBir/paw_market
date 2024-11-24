document.addEventListener('DOMContentLoaded', () => {
    // Fetch and display products
    fetch('/products')
        .then(response => response.json())
        .then(data => {
            const productsDiv = document.getElementById('products');
            const productSelect = document.getElementById('product-select');

            data.products.forEach(product => {
                // Display product details
                const productInfo = document.createElement('div');
                productInfo.innerHTML = `
                    <strong>${product.name}</strong><br>
                    ${product.description}<br>
                    Price: $${product.price.toFixed(2)}<br><br>
                `;
                productsDiv.appendChild(productInfo);

                // Add product to the select dropdown
                const option = document.createElement('option');
                option.value = product.id;
                option.textContent = `${product.name} - $${product.price.toFixed(2)}`;
                productSelect.appendChild(option);
            });
        });

    // Handle buyer registration
    const registerForm = document.getElementById('register-form');
    registerForm.addEventListener('submit', event => {
        event.preventDefault();

        const username = document.getElementById('username').value;
        const email    = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        fetch('/buyer/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        })
        .then(response => response.json())
        .then(data => {
            const messagePara = document.getElementById('register-message');
            if (data.error) {
                messagePara.textContent = `Error: ${data.error}`;
            } else {
                messagePara.textContent = `Success: ${data.message}. Your Buyer ID is ${data.buyer_id}.`;
            }
        });
    });

    // Handle order placement
    const orderForm = document.getElementById('order-form');
    orderForm.addEventListener('submit', event => {
        event.preventDefault();

        const buyerId    = parseInt(document.getElementById('buyer-id').value);
        const productId  = parseInt(document.getElementById('product-select').value);
        const quantity   = parseInt(document.getElementById('quantity').value);

        fetch('/buyer/orders', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ buyer_id: buyerId, product_id: productId, quantity })
        })
        .then(response => response.json())
        .then(data => {
            const messagePara = document.getElementById('order-message');
            if (data.error) {
                messagePara.textContent = `Error: ${data.error}`;
            } else {
                messagePara.textContent = `Success: ${data.message}`;
            }
        });
    });
});
