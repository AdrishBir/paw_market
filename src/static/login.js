document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    // Handle form submission
    loginForm.addEventListener('submit', event => {
        event.preventDefault();

        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;

        // Send login request to the server
        fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        })
        .then(response => response.json())
        .then(data => {
            const loginMessage = document.getElementById('login-message');
            if (data.error) {
                loginMessage.textContent = `Error: ${data.error}`;
                loginMessage.style.color = 'red';
            } else {
                loginMessage.textContent = `Welcome, ${data.username}! Redirecting...`;
                loginMessage.style.color = 'green';

                // Redirect to shop page after login
                setTimeout(() => {
                    window.location.href = '/shop';
                }, 2000);
            }
        });
    });
});