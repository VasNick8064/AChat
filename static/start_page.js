// Animate the registration title
gsap.from("#registrationTitle", {
   opacity: 0,
   y: -10,
   duration: 0.5,
   delay: 0.2,
   ease: "power2.inOut"
});

// Animate the auth container
gsap.from("#authContainer", {
   opacity: 0,
   y: -10,
   duration: 0.5,
   delay: 0.4,
   ease: "power2.inOut"
});

// Event listener for toggling to login form
document.getElementById('toggleLink').addEventListener('click', function(e) {
   e.preventDefault();
   document.getElementById('authContainer').style.display = 'none'; // Hide registration
   document.getElementById('loginContainer').style.display = 'flex'; // Show login
   document.getElementById("registrationTitle").innerText = "Login"; // Change title to Login
});

// Event listener for toggling back to registration form
document.getElementById('backToRegisterLink').addEventListener('click', function(e) {
   e.preventDefault();
   document.getElementById('loginContainer').style.display = 'none'; // Hide login
   document.getElementById('authContainer').style.display = 'flex'; // Show registration
   document.getElementById("registrationTitle").innerText = "Sign UP"; // Change title back to Registration
});

// Event listener for registration button
document.getElementById('registerButton').addEventListener('click', function() {
   // Logic for registration can be added here
   alert('Registration logic goes here!');
});

// Event listener for login button
document.getElementById('loginButton').addEventListener('click', function() {
   // Logic for login can be added here
   alert('Login logic goes here!');
});