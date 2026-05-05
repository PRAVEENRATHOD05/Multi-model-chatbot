// Get the elements
const sidebar = document.getElementById('sidebar');
const toggleButton = document.getElementById('toggle-sidebar');

// Add click event listener to the toggle button
toggleButton.addEventListener('click', function() {
  // Toggle the 'active' class on the sidebar to open/close it
  sidebar.classList.toggle('active');
});

// Function to close sidebar if clicked outside
document.addEventListener('click', function(event) {
  const isClickInside = sidebar.contains(event.target) || toggleButton.contains(event.target);

  // If the click is outside the sidebar and it is active, close it
  if (!isClickInside && sidebar.classList.contains('active')) {
    sidebar.classList.remove('active');
  }
});

// Theme switching functionality
document.getElementById('lightMode').addEventListener('click', (event) => {
  event.preventDefault(); // Prevent default link behavior
  document.body.classList.remove('dark-mode'); // Remove dark mode
});

document.getElementById('darkMode').addEventListener('click', (event) => {
  event.preventDefault(); // Prevent default link behavior
  document.body.classList.add('dark-mode'); // Add dark mode
});
// Profile dropdown functionality
const profileBtn = document.getElementById('profileBtn');
const dropdownContent = document.getElementById('dropdownContent');

profileBtn.addEventListener('click', (event) => {
    event.stopPropagation(); // Prevents click event from bubbling up
    dropdownContent.style.display = dropdownContent.style.display === 'block' ? 'none' : 'block';
});

// Click outside to close dropdown
window.addEventListener('click', (event) => {
    if (!profileBtn.contains(event.target) && !dropdownContent.contains(event.target)) {
        dropdownContent.style.display = 'none';
    }
});
