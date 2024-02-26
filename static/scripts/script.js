function login_error() {
    alert(
        "The Username or Password you entered are not recognised. Please try again or reset your password."
    );
}

function generate_password() {
    const lower_char_bank = Array.from("abcdefghijklmnopqrstuvwxyz");
    const upper_char_bank = Array.from("ABCDEFGHIJKLMNOPQRSTUVWXYZ");
    const digi_bank = Array.from("0123456789");
    const spec_bank = Array.from("!@#$%^&*_-");

    // Check if length_input and strength_input are present
    const length_input = document.getElementById("length");
    const strength_input = document.getElementById("strength");

    // Set default values if inputs are not found
    const length = length_input ? parseInt(length_input.value) || 8 : 8;
    const strength = strength_input ? parseInt(strength_input.value) || 1 : 1;

    const all_chars = [
        ...lower_char_bank,
        ...upper_char_bank,
        ...digi_bank,
        ...spec_bank,
    ];

    const effective_strength = Math.max(strength, 1);

    const min_length = effective_strength * 4;
    const password_length = Math.max(length, min_length);

    let password;
    do {
        password = Array.from(
            { length: password_length },
            () => all_chars[Math.floor(Math.random() * all_chars.length)]
        );

        const char_counts = {
            lower: password.filter((char) => lower_char_bank.includes(char))
                .length,
            upper: password.filter((char) => upper_char_bank.includes(char))
                .length,
            digi: password.filter((char) => digi_bank.includes(char)).length,
            spec: password.filter((char) => spec_bank.includes(char)).length,
        };

        if (
            Object.values(char_counts).every(
                (count) => count >= effective_strength
            )
        ) {
            break;
        }
    } while (true);

    return password.join("");
}

function fill_text() {
    const text = document.getElementById("password");
    text.textContent = generate_password();
}

function fill_value() {
    const value = document.getElementById("password");
    value.value = generate_password();
}

function copy(id) {
    // Find the <p> tag with id "username"
    var usernameElement = document.getElementById(id);

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

    alert("Copied " + id);
}
