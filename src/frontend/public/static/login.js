document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const loginButton = document.getElementById('login-button');
    const buttonText = loginButton.querySelector('.button-text');
    const spinner = loginButton.querySelector('.spinner');
    const errorMessageDiv = document.getElementById('error-message');

    const displayError = (message) => {
        errorMessageDiv.textContent = message;
        errorMessageDiv.classList.add('show');
    };

    const clearError = () => {
        errorMessageDiv.textContent = '';
        errorMessageDiv.classList.remove('show');
    };

    const setLoadingState = (isLoading) => {
        if (isLoading) {
            loginButton.disabled = true;
            buttonText.style.display = 'none';
            spinner.style.display = 'block';
            clearError();
        } else {
            loginButton.disabled = false;
            buttonText.style.display = 'block';
            spinner.style.display = 'none';
        }
    };

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const usernameInput = document.getElementById('username');
            const passwordInput = document.getElementById('password');

            const username = usernameInput.value.trim();
            const password = passwordInput.value.trim();

            if (username === '') {
                displayError('Please enter your username.');
                usernameInput.focus();
                return;
            }
            if (password === '') {
                displayError('Please enter your password.');
                passwordInput.focus();
                return;
            }

            setLoadingState(true);

            try {
                // Simulate network request
                await new Promise(resolve => setTimeout(resolve, 1500));
                
                // This is where you would make the actual fetch call
                const response = await fetch('/users/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ username, password })
                });

                if (!response.ok) {
                    console.log(response)
                   const errorData = await response.json();
                   throw new Error(errorData.message || 'Login failed');
                }
                
                // On successful login, redirect to dashboard
                window.location.href = '/dashboard';

            } catch (error) {
                console.error('Login failed:', error);
                displayError(error.message || 'An unexpected error occurred.');
                setLoadingState(false);
            }
        });

        // Clear errors when user starts typing again
        ['username', 'password'].forEach(id => {
            const input = document.getElementById(id);
            input.addEventListener('input', clearError);
        });
    }
});