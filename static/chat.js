gsap.from(".chat-title", {
     opacity: 0,
     y: 10,
     duration: 0.5,
     delay: 0.2,
     ease: "power2.inOut"
});

function toggleSendButton() {
     const inputField = document.getElementById("messageInput");
     const sendButton = document.getElementById("sendButton");
     if (inputField.value.trim().length > 0) {
         sendButton.style.display = "block"; // Показываем кнопку
     } else {
         sendButton.style.display = "none"; // Скрываем кнопку
     }
}

// Toggle dropdown menu
const userIcon = document.getElementById('userIcon');
const dropdownMenu = document.getElementById('dropdownMenu');

userIcon.addEventListener('click', function() {
     dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';

     // Animate dropdown items
     const links = dropdownMenu.querySelectorAll('a');
     links.forEach((link, index) => {
         link.style.opacity = '1'; // Show link
         link.style.transform = 'translateY(0)'; // Move to original position
         link.style.transitionDelay = `${index * 50}ms`; // Staggered animation
     });
});

// Logout functionality
document.getElementById('logoutButton').addEventListener('click', function(e) {
     e.preventDefault();
     alert('Вы вышли из аккаунта!'); // Replace this with actual logout logic
     dropdownMenu.style.display = 'none'; // Hide dropdown after logout
});

// Close dropdown when clicking outside of it
window.addEventListener('click', function(event) {
     if (!event.target.matches('.user-icon')) {
         dropdownMenu.style.display = 'none';
         const links = dropdownMenu.querySelectorAll('a');
         links.forEach(link => {
             link.style.opacity = '0'; // Hide link
             link.style.transform = 'translateY(-10px)'; // Move above
         });
     }
});

// Open file dialog when clicking the folder icon
document.getElementById('attachIcon').addEventListener('click', function() {
     document.getElementById('fileInput').click(); // Trigger click on hidden file input
});

// Handle file upload
document.getElementById('fileInput').addEventListener('change', async (event) => {
     const file = event.target.files[0];

     if (file) {
         const formData = new FormData();
         formData.append('file', file);

         const response = await fetch('/uploadfile/', { // Adjust endpoint as necessary
             method: 'POST',
             body: formData,
         });

         const result = await response.json();
         console.log(result); // Handle the response as needed
     }
});