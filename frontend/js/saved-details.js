const API = "http://127.0.0.1:8000";


// =================================
// Check Login
// =================================

if (!localStorage.getItem("employee")) {
    window.location.href = "index.html";
}


// =================================
// Logout
// =================================

document
    .getElementById("logout")
    .addEventListener("click", () => {

        localStorage.removeItem("employee");

        window.location.href = "index.html";
    });


// =================================
// Current Tab
// =================================

let currentStatus = "Approved";


// =================================
// Tab Buttons
// =================================

document
    .querySelectorAll(".tabs button")
    .forEach((button) => {

        button.addEventListener("click", () => {

            document
                .querySelectorAll(".tabs button")
                .forEach((btn) => {
                    btn.classList.remove("active");
                });

            button.classList.add("active");

            currentStatus =
                button.dataset.status;

            loadPredictions();
        });

    });


// =================================
// Load Predictions
// =================================

async function loadPredictions() {

    const records =
        document.getElementById("records");

    records.innerHTML =
        "<p>Loading...</p>";


    let endpoint;


    if (currentStatus === "Approved") {

        endpoint =
            "/predictions/approved";

    } else {

        endpoint =
            "/predictions/not-approved";
    }


    try {

        const response =
            await fetch(`${API}${endpoint}`);


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to load predictions"
            );
        }


        // ================================
        // No Records
        // ================================

        if (data.length === 0) {

            records.innerHTML = `
                <p style="
                    color: #718398;
                    text-align: center;
                    padding: 40px;
                ">
                    No ${currentStatus.toLowerCase()}
                    applications found.
                </p>
            `;

            return;
        }


        // Clear loading message

        records.innerHTML = "";


        // ================================
        // Display Records
        // ================================

        data.forEach((prediction) => {

            const record =
                document.createElement("div");

            record.className =
                "record";


            record.innerHTML = `

                <div>

                    <span>
                        Loan ID
                    </span>

                    <strong>
                        #${prediction.id}
                    </strong>

                </div>


                <div>

                    <span>
                        Loan Amount
                    </span>

                    <strong>
                        ₹${Number(
                            prediction.loan_amount
                        ).toLocaleString("en-IN")}
                    </strong>

                </div>


                <div>

                    <span>
                        Risk
                    </span>

                    <strong>
                        ${Number(
                            prediction.risk_percentage
                        ).toFixed(2)}%
                    </strong>

                </div>


                <div>

                    <span>
                        Safety
                    </span>

                    <strong>
                        ${Number(
                            prediction.safety_percentage
                        ).toFixed(2)}%
                    </strong>

                </div>


                <button
                    type="button"
                    class="delete-button"
                    data-id="${prediction.id}"
                >
                    Delete
                </button>

            `;


            // Delete button event

            record
                .querySelector(".delete-button")
                .addEventListener("click", () => {

                    deletePrediction(
                        prediction.id
                    );

                });


            records.appendChild(record);

        });


    } catch (error) {

        console.error(
            "Load predictions error:",
            error
        );


        records.innerHTML = `

            <p style="
                color: #ff8996;
                text-align: center;
                padding: 30px;
            ">
                ${error.message}
            </p>

        `;
    }
}


// =================================
// Delete Prediction
// =================================

async function deletePrediction(id) {

    const confirmed =
        confirm(
            "Are you sure you want to delete this prediction?"
        );


    if (!confirmed) {
        return;
    }


    try {

        const response =
            await fetch(
                `${API}/predictions/${id}`,
                {
                    method: "DELETE"
                }
            );


        const data =
            await response.json();


        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to delete prediction"
            );
        }


        alert(
            "Prediction deleted successfully."
        );


        // Refresh current tab

        loadPredictions();


    } catch (error) {

        console.error(
            "Delete prediction error:",
            error
        );


        alert(
            error.message ||
            "Unable to delete prediction"
        );
    }
}


// =================================
// Initial Load
// =================================

loadPredictions();