const API = "http://127.0.0.1:8000";

const signupForm = document.getElementById("signupForm");
const nameInput = document.getElementById("name");
const emailInput = document.getElementById("email");
const passwordInput = document.getElementById("password");
const message = document.getElementById("msg");

signupForm.addEventListener("submit", async (e) => {

    e.preventDefault();

    message.textContent = "Creating account...";
    message.style.color = "#4bbcff";

    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;

    try {

        const url =
            `${API}/signup` +
            `?name=${encodeURIComponent(name)}` +
            `&email=${encodeURIComponent(email)}` +
            `&password=${encodeURIComponent(password)}`;

        const response = await fetch(url, {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail || "Signup failed"
            );
        }

        message.style.color = "#55d6a0";
        message.textContent =
            "Account created. Redirecting...";

        setTimeout(() => {
            window.location.href = "index.html";
        }, 900);

    } catch (error) {

        console.error("Signup error:", error);

        message.style.color = "#ff8996";
        message.textContent =
            error.message || "Signup failed";
    }
});