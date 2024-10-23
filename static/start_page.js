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

// Функция для показа уведомлений
function showNotification(message) {
   const notification = document.getElementById('notification');
   notification.innerText = message;
   notification.classList.add('show');

   // Показать уведомление
   notification.style.display = 'block';

   // Скрыть уведомление через несколько секунд
   setTimeout(() => {
       notification.classList.remove('show');
       notification.style.display = 'none';
   }, 3000);
}

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
document.getElementById('registerButton').addEventListener('click', async function() {
   const email = document.getElementById('email').value;
   const name = document.getElementById('name').value;
   const password = document.getElementById('password').value;

   // Проверка заполненности полей
   if (!email || !name || !password) {
       showNotification('Пожалуйста, заполните все поля!');
       return;
   }

   try {
       const response = await fetch('/auth/register', {
           method: 'POST',
           headers: {
               'Content-Type': 'application/json',
           },
           body: JSON.stringify({
               email,
               name,
               password,
           }),
       });

       if (!response.ok) {
           const errorData = await response.json();
           showNotification(errorData.detail); // Показать сообщение об ошибке
           return;
       }

       const data = await response.json();
       showNotification(data.message); // Показать сообщение об успешной регистрации
       window.location.href = data.redirect_url; // Перенаправление на страницу чата
   } catch (error) {
       console.error('Ошибка:', error);
       showNotification('Произошла ошибка при регистрации. Попробуйте еще раз.');
   }
});

// Event listener for login button
document.getElementById('loginButton').addEventListener('click', async function() {
    const email = document.getElementById('loginUsername').value; // Используем поле email для входа
    const password = document.getElementById('loginPassword').value;

    // Проверка заполненности полей
    if (!email || !password) {
        showNotification('Пожалуйста, заполните все поля!');
        return;
    }

    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email, // Передаем email вместо username
                password,
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            showNotification(errorData.detail); // Показать сообщение об ошибке
            return;
        }

        const data = await response.json();
        showNotification("Вы успешно вошли!"); // Показать сообщение об успешном входе
        window.location.href = "/chat"; // Перенаправление на страницу чата после входа
    } catch (error) {
        console.error('Ошибка:', error);
        showNotification('Произошла ошибка при входе. Попробуйте еще раз.');
    }
});