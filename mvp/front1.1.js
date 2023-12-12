
const url = 'http://127.0.0.1:5000/';
let endpoint = 'ingles';

const itButton = document.getElementById("it");
const hebButton = document.getElementById("heb");
const enButton = document.getElementById("en");
const frButton = document.getElementById("fr");

document.getElementById("textInput").placeholder;

itButton.addEventListener("click", () => {
    endpoint = 'italiano';
    document.getElementById("textInput").placeholder = "Enter text here... (Italian)";
    document.getElementById("textInput").value = ''
    console.log(endpoint);
});

hebButton.addEventListener("click", () => {
    endpoint = 'hebreo';
    document.getElementById("textInput").placeholder = "Enter text here... (Hebrew)";
    document.getElementById("textInput").value = ''
    console.log(endpoint);
});

enButton.addEventListener("click", () => {
    endpoint = 'ingles';
    document.getElementById("textInput").placeholder = "Enter text here... (English)";
    document.getElementById("textInput").value = ''
    console.log(endpoint);
});

frButton.addEventListener("click", () => {
    endpoint = 'frances';
    document.getElementById("textInput").placeholder = "Enter text here... (French)";
    document.getElementById("textInput").value = ''
    console.log(endpoint);
});


document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("translateForm").addEventListener("submit", async (event) => {
        event.preventDefault();

        try {
            const text = document.getElementById("textInput").value;
            const response = await fetch(url + endpoint, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }

            const data = await response.json();
            let output = '';
            for (const [word, translation] of Object.entries(data)) {
                output += `${word}: ${translation}\n`;
            }

            document.getElementById("translationOutput").textContent = output;
        } catch (error) {
            alert("Error occurred while translating: " + error.message);
        }
    });
});