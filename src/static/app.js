document.addEventListener('DOMContentLoaded', () => {
    let registeredBuyer = null; // Store registered buyer details

    // Fetch and display products
    fetch('/products')
        .then(response => response.json())
        .then(data => {
            const productsDiv = document.getElementById('products');
            const productSelect = document.getElementById('product-select');

            data.products.forEach(product => {
                // Display product card
                const productInfo = document.createElement('div');
                productInfo.className = 'product-card';
                productInfo.innerHTML = `
                    <div class="product-title"><strong>${product.name}</strong></div>
                    <div class="product-description">${product.description}</div>
                    <div class="product-price">Price: $${product.price.toFixed(2)}</div>
                `;
                productsDiv.appendChild(productInfo);

                // Populate product dropdown
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
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        fetch('/register', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, password })
        })
        .then(response => response.json())
        .then(data => {
            const messagePara = document.getElementById('register-message');
            if (data.error) {
                messagePara.textContent = `Error: ${data.error}`;
                messagePara.style.color = 'red';
            } else {
                messagePara.textContent = `Success: ${data.message}. Redirecting to login...`;
                messagePara.style.color = 'green';
                
                // Redirect to login page after a short delay
                setTimeout(() => {
                    window.location.href = '/login';
                }, 2000);
            }
        })
        .catch(error => {
            console.error('Registration error:', error);
            const messagePara = document.getElementById('register-message');
            messagePara.textContent = 'Error: Unable to register. Please try again.';
            messagePara.style.color = 'red';
        });
    });

    // Handle "Already a user?" button
    const loginButton = document.getElementById('login-button');
    loginButton.addEventListener('click', () => {
        window.location.href = '/login';
    });

    // Handle buyer login
    document.getElementById('login-form').addEventListener('submit', event => {
        event.preventDefault();
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        })
        .then(response => response.json())
        .then(data => {
            const helloMessage = document.getElementById('hello');
            if (data.error) {
                helloMessage.textContent = `Error: ${data.error}`;
                helloMessage.style.color = 'red';
            } else {
                helloMessage.textContent = `Welcome, ${data.username}! Your Buyer ID is ${data.buyer_id}.`;
                helloMessage.style.color = 'green';
                window.location.href = '/shop';
            }
        });
    });

    // Handle order placement
    document.getElementById('order-form').addEventListener('submit', event => {
        event.preventDefault();
        const buyerId = parseInt(document.getElementById('buyer-id').value);
        const productId = parseInt(document.getElementById('product-select').value);
        const quantity = parseInt(document.getElementById('quantity').value);

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

    // Add styles dynamically
    const applyStyles = () => {
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            Object.assign(form.style, {
                maxWidth: '400px',
                margin: '20px auto',
                padding: '20px',
                boxShadow: '0 0 10px rgba(0,0,0,0.1)',
                borderRadius: '8px'
            });
        });

        const inputs = document.querySelectorAll('input, select');
        inputs.forEach(input => {
            Object.assign(input.style, {
                width: '100%',
                padding: '8px',
                marginBottom: '10px',
                borderRadius: '4px',
                border: '1px solid #ddd'
            });
        });

        const buttons = document.querySelectorAll('button[type="submit"]');
        buttons.forEach(button => {
            Object.assign(button.style, {
                width: '100%',
                padding: '10px',
                backgroundColor: '#4CAF50',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
            });
            button.addEventListener('mouseover', () => {
                button.style.backgroundColor = '#45a049';
            });
            button.addEventListener('mouseout', () => {
                button.style.backgroundColor = '#4CAF50';
            });
        });

        document.body.style = `
            background: url('https://img.freepik.com/premium-vector/cartoon-dog-cat-with-blank-signboard-graphic-design_11460-13504.jpg') 
            top center / contain no-repeat fixed, rgba(255, 255, 255, 0.5);
            background-blend-mode: overlay;
            min-height: 100vh;
        `;
    };

    applyStyles();
});