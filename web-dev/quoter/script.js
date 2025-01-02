// ==================== Constants & State ====================
const API_URL = 'https://dummyjson.com/quotes/random';
let quoteCount = 0;

// ==================== DOM Elements ====================
const quoteText = document.getElementById('quoteText');
const quoteAuthor = document.getElementById('quoteAuthor');
const tagsContainer = document.getElementById('tags');
const newQuoteBtn = document.getElementById('newQuoteBtn');
const quoteCountElement = document.getElementById('quoteCount');

// ==================== Functions ====================

/**
 * Fetches a random quote from the API
 * @returns {Promise<Object>} Quote data object
 */
async function fetchQuote() {
    try {
        const response = await fetch(API_URL);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching quote:', error);
        throw error;
    }
}

/**
 * Displays the quote data in the UI with smooth animations
 * @param {Object} data - Quote data from API
 */
function displayQuote(data) {
    // Add loading state for smooth transition
    quoteText.classList.add('loading');

    setTimeout(() => {
        // Update quote text - DummyJSON uses 'quote' instead of 'content'
        const quoteContent = data.quote || data.content;
        quoteText.textContent = `"${quoteContent}"`;
        quoteText.classList.remove('loading');

        // Update author
        quoteAuthor.textContent = data.author;

        // Update tags - DummyJSON doesn't provide tags, so we'll hide the container
        if (data.tags && data.tags.length > 0) {
            displayTags(data.tags);
        } else {
            tagsContainer.innerHTML = '';
        }

        // Update quote count
        quoteCount++;
        updateQuoteCount();
    }, 200);
}

/**
 * Displays tags for the current quote
 * @param {Array<string>} tags - Array of tag strings
 */
function displayTags(tags) {
    // Clear existing tags
    tagsContainer.innerHTML = '';

    // Add new tags with staggered animation
    if (tags && tags.length > 0) {
        tags.forEach((tag, index) => {
            const tagElement = document.createElement('span');
            tagElement.className = 'tag';
            tagElement.textContent = tag;
            tagElement.style.animationDelay = `${index * 0.1}s`;
            tagsContainer.appendChild(tagElement);
        });
    }
}

/**
 * Updates the quote count display with animation
 */
function updateQuoteCount() {
    quoteCountElement.style.transform = 'scale(1.2)';
    quoteCountElement.textContent = quoteCount;

    setTimeout(() => {
        quoteCountElement.style.transform = 'scale(1)';
    }, 200);
}

/**
 * Shows error message to user
 * @param {string} message - Error message to display
 */
function showError(message) {
    quoteText.textContent = message;
    quoteAuthor.textContent = '';
    tagsContainer.innerHTML = '';
    quoteText.classList.remove('loading');
}

/**
 * Main function to get and display a new quote
 */
async function getNewQuote() {
    // Add loading state to button
    newQuoteBtn.classList.add('loading');
    newQuoteBtn.disabled = true;

    try {
        const data = await fetchQuote();
        displayQuote(data);
    } catch (error) {
        showError('Failed to fetch quote. Please try again.');
    } finally {
        // Remove loading state from button
        setTimeout(() => {
            newQuoteBtn.classList.remove('loading');
            newQuoteBtn.disabled = false;
        }, 300);
    }
}

// ==================== Event Listeners ====================
newQuoteBtn.addEventListener('click', getNewQuote);

// Allow Enter key to fetch new quote when button is focused
newQuoteBtn.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
        getNewQuote();
    }
});

// ==================== Initialization ====================
// Load first quote when page loads
window.addEventListener('DOMContentLoaded', () => {
    // Small delay for initial animation
    setTimeout(() => {
        getNewQuote();
    }, 500);
});
