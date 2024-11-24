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

// Add some basic styling
document.addEventListener('DOMContentLoaded', () => {
    // Style the forms
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.style.maxWidth = '400px';
        form.style.margin = '20px auto';
        form.style.padding = '20px';
        form.style.boxShadow = '0 0 10px rgba(0,0,0,0.1)';
        form.style.borderRadius = '8px';
    });

    // Style the inputs
    const inputs = document.querySelectorAll('input, select');
    inputs.forEach(input => {
        input.style.width = '100%';
        input.style.padding = '8px';
        input.style.marginBottom = '10px';
        input.style.borderRadius = '4px';
        input.style.border = '1px solid #ddd';
    });

    // Style the submit buttons
    const buttons = document.querySelectorAll('button[type="submit"]');
    buttons.forEach(button => {
        button.style.width = '100%';
        button.style.padding = '10px';
        button.style.backgroundColor = '#4CAF50';
        button.style.color = 'white';
        button.style.border = 'none';
        button.style.borderRadius = '4px';
        button.style.cursor = 'pointer';
        
        // Add hover effect
        button.addEventListener('mouseover', () => {
            button.style.backgroundColor = '#45a049';
        });
        button.addEventListener('mouseout', () => {
            button.style.backgroundColor = '#4CAF50';
        });
    });

    // Style the message paragraphs
    const messages = document.querySelectorAll('#register-message, #order-message');
    messages.forEach(message => {
        message.style.margin = '10px 0';
        message.style.padding = '10px';
        message.style.borderRadius = '4px';
        message.style.backgroundColor = '#f8f9fa';
        message.style.textAlign = 'center';
    });
});
// Style the product cards
const productCards = document.querySelectorAll('.product-card');
productCards.forEach(card => {
    card.style.border = '1px solid #ddd';
    card.style.borderRadius = '8px';
    card.style.padding = '15px';
    card.style.margin = '10px';
    card.style.width = '250px';
    card.style.display = 'inline-block';
    card.style.verticalAlign = 'top';
    card.style.backgroundColor = 'white';
    card.style.boxShadow = '0 2px 5px rgba(0,0,0,0.1)';
});

// Style the product images
const productImages = document.querySelectorAll('.product-image');
productImages.forEach(img => {
    img.style.width = '100%';
    img.style.height = '200px';
    img.style.objectFit = 'cover';
    img.style.borderRadius = '4px';
    img.style.marginBottom = '10px';
});

// Style the product titles
const productTitles = document.querySelectorAll('.product-title');
productTitles.forEach(title => {
    title.style.fontSize = '18px';
    title.style.fontWeight = 'bold';
    title.style.marginBottom = '8px';
    title.style.color = '#333';
});

// Style the product prices
const productPrices = document.querySelectorAll('.product-price');
productPrices.forEach(price => {
    price.style.fontSize = '16px';
    price.style.color = '#4CAF50';
    price.style.marginBottom = '10px';
    price.style.fontWeight = '500';
});

// Style the product descriptions
const productDescriptions = document.querySelectorAll('.product-description');
productDescriptions.forEach(desc => {
    desc.style.fontSize = '14px';
    desc.style.color = '#666';
    desc.style.marginBottom = '15px';
    desc.style.lineHeight = '1.4';
});

// Style the add to cart buttons
const addToCartButtons = document.querySelectorAll('.add-to-cart');
addToCartButtons.forEach(button => {
    button.style.width = '100%';
    button.style.padding = '8px';
    button.style.backgroundColor = '#4CAF50';
    button.style.color = 'white';
    button.style.border = 'none';
    button.style.borderRadius = '4px';
    button.style.cursor = 'pointer';
    button.style.fontSize = '14px';
    
    // Add hover effect
    button.addEventListener('mouseover', () => {
        button.style.backgroundColor = '#45a049';
    });
    button.addEventListener('mouseout', () => {
        button.style.backgroundColor = '#4CAF50';
    });
});

// Style the products container
const productsContainer = document.querySelector('#products-container');
if (productsContainer) {
    productsContainer.style.padding = '20px';
    productsContainer.style.maxWidth = '1200px';
    productsContainer.style.margin = '0 auto';
    productsContainer.style.textAlign = 'center';
}

// Style the quantity inputs
const quantityInputs = document.querySelectorAll('.quantity-input');
quantityInputs.forEach(input => {
    input.style.width = '60px';
    input.style.padding = '5px';
    input.style.marginBottom = '10px';
    input.style.borderRadius = '4px';
    input.style.border = '1px solid #ddd';
    input.style.textAlign = 'center';
});

// Add background image to the body
document.body.style.backgroundImage = "url('https://media.gettyimages.com/id/979081604/photo/kitten-sitting-on-dog.jpg?s=612x612&w=gi&k=20&c=gEKiIdzPQ8u3hZvf95mxqn2p7jttefJp1WTINiDqUr0=')";
document.body.style.backgroundSize = 'cover';
document.body.style.backgroundPosition = 'center';
document.body.style.backgroundRepeat = 'no-repeat';
document.body.style.backgroundAttachment = 'fixed';
document.body.style.minHeight = '100vh';

