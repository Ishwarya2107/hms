// Ensure the script runs after the DOM is fully loaded
document.addEventListener('DOMContentLoaded', () => {
    // Select the search button and input field
    const searchButton = document.querySelector('.search-button');
    const searchInput = document.querySelector('.search-input');

    // Add click event listener to the search button
    searchButton.addEventListener('click', () => {
        // Get the value from the input field
        const userInput = searchInput.value;

        // Check if the input is not empty
        if (userInput.trim()) {
            // Store the input in localStorage
            localStorage.setItem('userInput', userInput);

            // Log the input to the console
            console.log('User Input:', userInput);
        } else {
            console.log('Input is empty');
        }
    });
});

