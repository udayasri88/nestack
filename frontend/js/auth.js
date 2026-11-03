// Registration functionality

const registerForm = document.getElementById("registerForm");

if (registerForm) {

    registerForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const username = document.getElementById("username").value;

        const password = document.getElementById("password").value;

        const response = await fetch("/register", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                password: password
            })

        });

        const result = await response.json();

        document.getElementById("message").textContent =
            result.message || result.error;

        if (response.status === 201) {

            setTimeout(function() {
                window.location.href = "/login-page";
            }, 1500);

        }

    });

}


// Login functionality

const loginForm = document.getElementById("loginForm");

if (loginForm) {

    loginForm.addEventListener("submit", async function(event) {

        event.preventDefault();

        const username = document.getElementById("username").value;

        const password = document.getElementById("password").value;

        const response = await fetch("/login", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username: username,
                password: password
            })

        });

        const result = await response.json();

        if (response.ok) {

            sessionStorage.setItem(
                "session_token",
                result.session_token
            );

            window.location.href = "/dashboard-page";

        } else {

            document.getElementById("message").textContent =
                result.error;

        }

    });

}