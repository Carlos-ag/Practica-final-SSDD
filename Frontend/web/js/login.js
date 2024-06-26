document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.querySelector("form");

    loginForm.addEventListener("submit", function(e) {
        e.preventDefault(); // Prevent the default form submission

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        // API endpoint for login
        const url = "http://127.0.0.1:6789/api/login"; 

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                
                "Authorization": 'Basic ' + btoa(email + ":" + password)
            },
            body: JSON.stringify({
                username: email,
                password: password,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Create a cookie with user_id here
                console.log("User ID: " + data.user_id);
                localStorage.setItem("user_id", data.user_id);

                // Redirect to home.html upon successful login
                window.location.href = "home.html";
            } else {
                // Handle login failure (e.g., show an error message)
                alert("Login failed: " + data.message);
            }
        })
        .catch(error => alert("Ha habido un error"));
    });
});
