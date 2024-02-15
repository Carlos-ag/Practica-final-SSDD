document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.querySelector("form");

    loginForm.addEventListener("submit", function(e) {
        e.preventDefault(); // Prevent the default form submission

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        // API endpoint where you're sending a POST request for login
        const url = "http://127.0.0.1:6789/login"; // Update this URL to your actual login API endpoint

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: email, // Make sure this matches with your backend expectation
                password: password,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirect to home.html upon successful login
                window.location.href = "home.html";
            } else {
                // Handle login failure (e.g., show an error message)
                alert("Login failed: " + data.message);
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
