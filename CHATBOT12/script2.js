// Sidebar Toggle
const sidebar = document.getElementById('sidebar');
const toggleButton = document.getElementById('toggle-sidebar');
toggleButton.addEventListener('click', function() {
  sidebar.classList.toggle('active');
});

// Chat History Buttons
const flowchartBtn = document.getElementById('flowchart-btn');
const guidanceBtn = document.getElementById('guidance-btn');
const askmeBtn = document.getElementById('askme-btn');
const chatDisplay = document.getElementById('chat-display');

// Input field and send button
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');

// Variable to track the current chat type
let currentChatType = '';

// Load chat history from localStorage
function loadChatHistory(type) {
  const chatHistory = localStorage.getItem(type) || "No chat history available.";
  chatDisplay.innerHTML = `<h2>${type} History</h2><p>${chatHistory}</p>`;
  currentChatType = type; // Set the current chat type
}

// Save chat to localStorage
function saveChat(type, message) {
  let currentHistory = localStorage.getItem(type) || '';
  currentHistory += `<br/>${message}`;
  localStorage.setItem(type, currentHistory);
}

// Attach event listeners to load the correct chat history
flowchartBtn.addEventListener('click', () => loadChatHistory('Flowchart'));
guidanceBtn.addEventListener('click', () => loadChatHistory('Guidance'));
askmeBtn.addEventListener('click', () => loadChatHistory('Ask me'));

// Add functionality to send messages to the current section
sendBtn.addEventListener('click', () => {
  const message = chatInput.value.trim();
  if (message && currentChatType) {
    saveChat(currentChatType, message);
    loadChatHistory(currentChatType); // Instantly update the chat display
    chatInput.value = ''; // Clear the input field
  }
});
