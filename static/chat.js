
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
            addMessageToChat(message.content, message.sender_id === currentUserId ? 'me' : 'other', message.name_user);
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
    const recipientId = 1; // Пример ID получателя

    if (content) {
        console.log("Отправка сообщения:", content);

        const token = localStorage.getItem('token'); // Или другой способ получения токена
        const nameUser = "ВашеИмя"; // Замените на фактическое имя пользователя

        const response = await fetch('/chat/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`, // Добавьте токен в заголовок
            },
            body: JSON.stringify({
                content: content,
                recipient_id: recipientId,
                name_user: nameUser
            }),
        });

        if (response.ok) {
            const result = await response.json();
            console.log(result);

            addMessageToChat(result.content, 'me', result.name_user); 

            messageInput.value = ''; 
            toggleSendButton(); 
        } else {
            const errorData = await response.json();
            console.error('Ошибка при отправке сообщения:', errorData);
        }
    } else {
        console.warn('Поле ввода пустое');
    }
});

// Функция для добавления сообщения в чат
function addMessageToChat(content, sender, nameUser) {
    const chatContainer = document.getElementById('chatContainer');

    const messageDiv = document.createElement('div');
    messageDiv.className = sender === 'me' ? 'message me' : 'message other';

    messageDiv.textContent = `${nameUser}: ${content}`;

    chatContainer.appendChild(messageDiv);
}

// Toggle dropdown menu
const userIcon = document.getElementById('userIcon');
const dropdownMenu = document.getElementById('dropdownMenu');

userIcon.addEventListener('click', function() {
    dropdownMenu.style.display = dropdownMenu.style.display === 'block' ? 'none' : 'block';
});

// Эндпоинт для logout
document.getElementById('logoutButton').addEventListener('click', async () => {
    const token = localStorage.getItem('token'); // Получение токена

    const response = await fetch('/auth/logout', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    if (response.ok) {
        localStorage.removeItem('token'); // Удаляем токен из локального хранилища
        window.location.href = '/auth'; // Перенаправляем на страницу логина
    } else {
        console.error('Ошибка при выходе:', response.statusText);
    }
});


