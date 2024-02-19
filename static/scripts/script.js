function login_error() {
    alert(
        "The Username or Password you entered are not recognised. Please try again or reset your password."
    );
}

function generatePassword() {
    // Character banks for lowercase, uppercase, digits, and special characters
    const lowerCharBank = Array.from("abcdefghijklmnopqrstuvwxyz");
    const upperCharBank = Array.from("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    const digiBank = Array.from("0123456789");
    const specBank = Array.from("!@#$%^&*_-");

    // Get input values
    const lengthInput = document.getElementById("length");
    const strengthInput = document.getElementById("strength");

    // Convert input values to numbers, defaulting to 1 if not valid
    const length = parseInt(lengthInput.value) || 1;
    const strength = parseInt(strengthInput.value) || 1;

    // Combine all character banks
    const allChars = [
        ...lowerCharBank,
        ...upperCharBank,
        ...digiBank,
        ...specBank,
    ];

    // Ensure strength is at least 1
    const effectiveStrength = strength < 1 ? 1 : strength;

    // Set minimum length based on strength
    const minLength = effectiveStrength * 4;
    const passwordLength = length < minLength ? minLength : length;

    let running = true;
    let password; // Declare password outside the loop
    while (running) {
        let lowerCharCount = 0,
            upperCharCount = 0,
            digiCount = 0,
            specCount = 0;
        password = []; // Initialize password here

        // Generate a random password
        for (let i = 0; i < passwordLength; i++) {
            password.push(
                allChars[Math.floor(Math.random() * allChars.length)]
            );
        }

        // Count the occurrences of each character type
        lowerCharCount = password.filter((char) =>
            lowerCharBank.includes(char)
        ).length;
        upperCharCount = password.filter((char) =>
            upperCharBank.includes(char)
        ).length;
        digiCount = password.filter((char) => digiBank.includes(char)).length;
        specCount = password.filter((char) => specBank.includes(char)).length;

        // Check if the password meets the strength criteria
        if (
            lowerCharCount >= effectiveStrength &&
            upperCharCount >= effectiveStrength &&
            digiCount >= effectiveStrength &&
            specCount >= effectiveStrength
        ) {
            running = false;
        }

        if (
            [lowerCharCount, upperCharCount, digiCount, specCount].every(
                (count) => count >= effectiveStrength
            )
        ) {
            running = false;
        }
    }

    // Output the password to the <p> tag with the id "pass"
    const passOutput = document.getElementById("pass");
    passOutput.textContent = password.join("");
}

function copy(id) {
    // Find the <p> tag with id "username"
    var usernameElement = document.getElementById(id);

    // Check if the element exists
    if (usernameElement) {
        // Create a range and select the text content
        var range = document.createRange();
        range.selectNode(usernameElement);

        // Create a selection and add the range
        var selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);

        // Copy the selected text to the clipboard
        document.execCommand("copy");

        // Clear the selection
        selection.removeAllRanges();

        // Optionally, you can provide feedback to the user
        alert("Copied.");
    } else {
        // The element with id "username" was not found
        console.error("Element not found.");
    }
}
