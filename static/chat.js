gsap.from(".chat-title", {
    opacity: 0,
    y: 10,
    duration: 0.5,
    delay: 0.2,
    ease: "power2.inOut"
});

// Получите ID текущего пользователя из глобальной переменной или API
const currentUserId = 3; // Замените на фактический способ получения ID текущего пользователя

function toggleSendButton() {
    const inputField = document.getElementById("messageInput");
    const sendButton = document.getElementById("sendButton");
    sendButton.style.display = inputField.value.trim().length > 0 ? "block" : "none";
}

async function loadMessages() {
    const userId = 1; // Замените на фактический ID получателя
    const response = await fetch(`/chat/message/${userId}`);

    if (response.ok) {
        const messages = await response.json();
        messages.forEach(message => {
            addMessageToChat(message.content, message.sender_id === currentUserId ? 'me' : 'other', message.name_user); // Используем currentUserId и name_user
        });
    } else {
        console.error('Ошибка при загрузке сообщений:', response.statusText);
    }
}

// Вызов функции загрузки сообщений при загрузке страницы
window.onload = loadMessages;

document.getElementById('sendButton').addEventListener('click', async () => {
    const messageInput = document.getElementById('messageInput');
    const content = messageInput.value.trim();

    // Замените на фактический ID получателя
    const recipientId = 1; // Пример ID получателя

    if (content) {
        console.log("Отправка сообщения:", content); // Отладочная информация

        // Получите токен аутентификации из локального хранилища или другого места
        const token = localStorage.getItem('token'); // Или другой способ получения токена

        // Получите имя пользователя (например, из глобальной переменной или API)
        const nameUser = "ВашеИмя"; // Замените на фактическое имя пользователя

        const response = await fetch('/chat/messages', { // Правильный маршрут
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`, // Добавьте токен в заголовок
            },
            body: JSON.stringify({
                content: content,
                recipient_id: recipientId,
                name_user: nameUser // Добавляем name_user
            }),
        });

        if (response.ok) {
            const result = await response.json();
            console.log(result); // Обработка результата

            // Добавление сообщения в чат с учетом имени пользователя
            addMessageToChat(result.content, 'me', result.name_user); // 'me' для отправителя

            messageInput.value = ''; // Очистка поля ввода
            toggleSendButton(); // Скрыть кнопку отправки
        } else {
            const errorData = await response.json();
            console.error('Ошибка при отправке сообщения:', errorData); // Выводим подробности об ошибке
        }
    } else {
        console.warn('Поле ввода пустое');
    }
});

// Функция для добавления сообщения в чат
function addMessageToChat(content, sender, nameUser) {
    const chatContainer = document.getElementById('chatContainer');

    const messageDiv = document.createElement('div');
    messageDiv.className = sender === 'me' ? 'message me' : 'message other'; // Добавьте соответствующий класс для стилизации

    messageDiv.textContent = `${nameUser}: ${content}`; // Добавляем имя пользователя к сообщению

    chatContainer.appendChild(messageDiv);
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

    localStorage.removeItem('token'); // Удаляем токен из локального хранилища

    alert('Вы вышли из аккаунта!');
    dropdownMenu.style.display = 'none'; // Скрыть выпадающее меню после выхода

    window.location.href = '/login'; // Замените на фактический путь к странице входа
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

        const response = await fetch('/uploadfile/', {
            method: 'POST',
            body: formData,
        });

        const result = await response.json();
        console.log(result); // Обработка ответа по мере необходимости
    }
});