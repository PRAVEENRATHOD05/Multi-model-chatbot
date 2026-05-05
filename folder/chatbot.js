const sidebar = document.getElementById('sidebar');
const toggleSidebar = document.getElementById('toggle-sidebar');
const toggleHistory = document.getElementById('toggle-history');
const chatHistory = document.getElementById('chat-history');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const chatSection = document.getElementById('chat-section');
const historyList = document.getElementById('history-list');
const fileUpload = document.getElementById('file-upload');
const profileBtn = document.getElementById('profileBtn');
const dropdownContent = document.getElementById('dropdownContent');

// Toggle Sidebar
toggleSidebar.addEventListener('click', function() {
    sidebar.style.transform = sidebar.style.transform === 'translateX(0px)' ? 'translateX(-100%)' : 'translateX(0px)';
    chatHistory.classList.add('hidden');
});

// Show/Hide Chat History
toggleHistory.addEventListener('click', function() {
    chatHistory.classList.toggle('hidden');
});

// Send Message
function handleMessageInput(event) {
    if (event.type === 'click' || (event.key === 'Enter' && !event.shiftKey)) {
        event.preventDefault();
        sendMessage();
    }
}

sendBtn.addEventListener('click', handleMessageInput);
userInput.addEventListener('keypress', handleMessageInput);

async function sendMessage() {
    const userMessage = userInput.value.trim();
    if (userMessage) {
        appendMessage(userMessage, 'user');
        userInput.value = '';
        
        const botThinkingMessage = appendMessage('Bot is typing...', 'bot');

        try {
            const botMessage = await getBotResponse(userMessage);
            botThinkingMessage.innerHTML = marked.parse(botMessage); // Parse Markdown response
            saveChatHistory(userMessage, botMessage);
        } catch (error) {
            botThinkingMessage.innerHTML = 'Error: Could not fetch the bot response.';
        }
    }
}

async function getBotResponse(userMessage) {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/get_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question: userMessage })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        if (!data.response) {
            throw new Error('No response data from server');
        }

        return data.response;
    } catch (error) {
        console.error("Error fetching bot response:", error);
        return "Error: Could not fetch the bot response. Please try again.";
    }
}

function appendMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender);
    messageElement.innerHTML = sender === 'bot' ? marked.parse(message) : message;
    chatSection.appendChild(messageElement);
    chatSection.scrollTop = chatSection.scrollHeight;
    return messageElement;
}

function saveChatHistory(userMessage, botMessage) {
    const historyItem = { userMessage, botMessage };
    const storedChatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    storedChatHistory.push(historyItem);
    localStorage.setItem('chatHistory', JSON.stringify(storedChatHistory));
}
