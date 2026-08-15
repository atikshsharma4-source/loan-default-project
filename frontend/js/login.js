const API = "http://127.0.0.1:8000";


// =================================
// Login Form
// =================================

document
    .getElementById("loginForm")
    .addEventListener("submit", async (e) => {

        e.preventDefault();

        const message =
            document.getElementById("msg");

        const email =
            document.getElementById("email")
                .value
                .trim();

        const password =
            document.getElementById("password")
                .value;


        // Show loading message

        message.textContent =
            "Signing in...";

        message.style.color =
            "#4bbcff";


        try {

            // ================================
            // Call FastAPI Login
            // ================================

            const response =
                await fetch(
                    `${API}/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
                    {
                        method: "POST"
                    }
                );


            const data =
                await response.json();


            // ================================
            // Handle Error
            // ================================

            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Invalid email or password"
                );

            }


            // ================================
            // Store Employee Information
            // ================================

            const employee =
                data.employee;


            localStorage.setItem(
                "employee",
                JSON.stringify(employee)
            );


            // ================================
            // Success Message
            // ================================

            message.textContent =
                "Login successful!";

            message.style.color =
                "#55d6a0";


            // ================================
            // Go to Dashboard
            // ================================

            setTimeout(() => {

                window.location.href =
                    "dashboard.html";

            }, 500);


        } catch (error) {

            console.error(
                "Login error:",
                error
            );


            message.textContent =
                error.message ||
                "Unable to connect to server.";

            message.style.color =
                "#ff8996";

        }

    });