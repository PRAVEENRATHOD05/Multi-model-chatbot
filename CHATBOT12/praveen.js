const sidebar = document.getElementById('sidebar');
const toggleSidebar = document.getElementById('toggle-sidebar');
const toggleHistory = document.getElementById('toggle-history');
const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const chatSection = document.getElementById('chat-section');
const historyList = document.getElementById('history-list');
const fileUpload = document.getElementById('file-upload');

// Load chat history from local storage when the page loads
window.onload = function() {
    localStorage.removeItem('chatHistory');
    chatSection.innerHTML = '';
};

// Toggle Sidebar
toggleSidebar.addEventListener('click', function() {
    if (sidebar.style.transform === 'translateX(0)') {
        sidebar.style.transform = 'translateX(-100%)';
        chatHistory.classList.add('hidden');
    } else {
        sidebar.style.transform = 'translateX(0)';
    }
});

// Show/Hide Chat History
toggleHistory.addEventListener('click', function() {
    chatHistory.classList.toggle('hidden');
});

// Close chat history when clicking outside
document.addEventListener('click', function(event) {
    const isClickInsideChatHistory = chatHistory.contains(event.target) || toggleHistory.contains(event.target);
    const isClickInsideSidebar = sidebar.contains(event.target) || toggleSidebar.contains(event.target);

    if (!isClickInsideChatHistory && !isClickInsideSidebar) {
        chatHistory.classList.add('hidden');
        sidebar.style.transform = 'translateX(-100%)';
    }
});

// File Upload
fileUpload.addEventListener('change', function(event) {
    const file = event.target.files[0];
    if (file) {
        const message = `File uploaded: ${file.name}`;
        appendMessage(message, 'user');
    }
});

// Send Message
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const userMessage = userInput.value.trim();
    if (userMessage) {
        appendMessage(userMessage, 'user');
        userInput.value = '';

        const botThinkingMessage = appendMessage('ChatBot thinking...', 'bot');

        try {
            const botMessage = await getBotResponse(userMessage);
            botThinkingMessage.innerText = botMessage;
            saveChatHistory(userMessage, botMessage);
        } catch (error) {
            botThinkingMessage.innerText = 'Error: Could not fetch the bot response.';
        }
    }
}

async function getBotResponse(userMessage) {
    const response = await fetch('http://127.0.0.1:5000/api/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    });
    const data = await response.json();
    return data.response;
}

function appendMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.innerText = message;
    chatSection.appendChild(messageElement);
    chatSection.scrollTop = chatSection.scrollHeight;
    return messageElement;
}
function saveChatHistory(userMessage, botMessage) {
    const historyItem = document.createElement('li');
    historyItem.classList.add('history-item');
    historyItem.innerHTML = `<strong>You:</strong> ${userMessage}<br><strong>Bot:</strong> ${botMessage}`;
    historyList.appendChild(historyItem);
}

