const API = "https://loanrisk-api.onrender.com";

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



            const response =
                await fetch(
                    `${API}/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
                    {
                        method: "POST"
                    }
                );


            const data =
                await response.json();




            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Invalid email or password"
                );

            }



            const employee =
                data.employee;


            localStorage.setItem(
                "employee",
                JSON.stringify(employee)
            );



            message.textContent =
                "Login successful!";

            message.style.color =
                "#55d6a0";


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