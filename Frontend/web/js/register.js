document.addEventListener("DOMContentLoaded", function() {
    const registerForm = document.querySelector("form");

    registerForm.addEventListener("submit", function(e) {
        e.preventDefault(); // Prevent the default form submission

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const confirmPassword = document.getElementById("confirm-password").value;

        if (password !== confirmPassword) {
            alert("Passwords do not match.");
            return;
        }

        // API endpoint where you're sending a POST request for registration
        const url = "http://127.0.0.1:6789/api/register"; // Update this URL to your actual register API endpoint

        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                name: name,
                username: email, // Make sure this matches with your backend expectation
                password: password,
            }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Success:", data);
                console.log("User ID: " + data.user_id);
                localStorage.setItem("user_id", data.user_id);

                // Redirect to home.html upon successful registration
                window.location.href = "home.html";
            } else {
                // Handle registration failure (e.g., show an error message)
                alert("Registration failed: " + data.message);
            }
        })
        .catch(error => console.error("Error:", error));
    });
});
