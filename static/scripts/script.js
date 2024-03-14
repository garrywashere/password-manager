// Function to generate a random password
function generate_password() {
    // Character banks
    const lower_char_bank = Array.from("abcdefghijklmnopqrstuvwxyz");
    const upper_char_bank = Array.from("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    const digi_bank = Array.from("0123456789");
    const spec_bank = Array.from("!@#$%^&*_-");

    // Retrieve input elements for password length and strength
    const length_input = document.getElementById("length");
    const strength_input = document.getElementById("strength");

    // Parse input values or use default values if inputs are not found
    const length = length_input ? parseInt(length_input.value) || 8 : 8;
    const strength = strength_input ? parseInt(strength_input.value) || 1 : 1;

    // Concatenate all character banks
    const all_chars = [
        ...lower_char_bank,
        ...upper_char_bank,
        ...digi_bank,
        ...spec_bank,
    ];

    // Calculate effective strength and minimum password length
    const effective_strength = Math.max(strength, 1);
    const min_length = effective_strength * 4;
    const password_length = Math.max(length, min_length);

    let password;
    // Generate password until it meets strength requirements
    do {
        password = Array.from(
            { length: password_length },
            () => all_chars[Math.floor(Math.random() * all_chars.length)]
        );

        // Count occurrences of characters from each character bank
        const char_counts = {
            lower: password.filter((char) => lower_char_bank.includes(char))
                .length,
            upper: password.filter((char) => upper_char_bank.includes(char))
                .length,
            digi: password.filter((char) => digi_bank.includes(char)).length,
            spec: password.filter((char) => spec_bank.includes(char)).length,
        };

        // Check if all character counts meet or exceed effective strength
        if (
            Object.values(char_counts).every(
                (count) => count >= effective_strength
            )
        ) {
            break;
        }
    } while (true);

    // Convert password array to string and return
    return password.join("");
}

// Function to copy text to clipboard
function copy(id) {
    var username_element = document.getElementById(id);

    var range = document.createRange();
    range.selectNode(username_element);

    var selection = window.getSelection();
    selection.removeAllRanges();
    selection.addRange(range);

    // Execute copy command
    document.execCommand("copy");

    // Clear selection and alert user
    selection.removeAllRanges();
    alert("Copied " + id);
}

// Function to toggle password visibility
function toggle_password() {
    var password = document.getElementById("password");

    // Change input type based on toggle state
    password.type = document.getElementById("toggle").checked
        ? "text"
        : "password";
}

// Function to fill password text content
function fill_text() {
    const text = document.getElementById("password");
    text.textContent = generate_password();
}

// Function to fill password input value
function fill_value() {
    const value = document.getElementById("password");
    value.value = generate_password();
}
