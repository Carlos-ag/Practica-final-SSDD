// Listen for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Select the logout button by its class
    var logoutButton = document.querySelector('.btn-outline-success');
    

    // // Add click event listener to the logout button
    logoutButton.addEventListener('click', function() {
        // Redirect the user to the index page
        window.location.href = '../index.html';
    });
});
