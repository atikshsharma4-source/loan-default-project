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
// Customer Fields
// =================================

// =================================
// Risk Threshold
// =================================

const thresholdDisplay =
    document.getElementById("threshold");

const thresholdInput =
    document.getElementById("thresholdInput");

const updateThresholdButton =
    document.getElementById("updateThreshold");

const thresholdMsg =
    document.getElementById("thresholdMsg");


// =================================
// Load Current Threshold
// =================================

async function loadThreshold() {

    try {

        const response =
            await fetch(
                `${API}/risk-threshold`
            );

        const data =
            await response.json();

        if (!response.ok) {

            throw new Error(
                data.detail ||
                "Unable to load threshold"
            );
        }

        const threshold =
            Number(data.safety_threshold);

        thresholdDisplay.textContent =
            `${threshold}%`;

        thresholdInput.value =
            threshold;

    } catch (error) {

        console.error(
            "Threshold error:",
            error
        );

        thresholdMsg.textContent =
            "Unable to load threshold.";

        thresholdMsg.style.color =
            "#ff8996";
    }
}


// =================================
// Update Threshold
// =================================

updateThresholdButton.addEventListener(
    "click",
    async () => {

        const newThreshold =
            Number(thresholdInput.value);


        // Validate

        if (
            isNaN(newThreshold) ||
            newThreshold < 0 ||
            newThreshold > 100
        ) {

            thresholdMsg.textContent =
                "Threshold must be between 0 and 100.";

            thresholdMsg.style.color =
                "#ff8996";

            return;
        }


        thresholdMsg.textContent =
            "Updating...";

        thresholdMsg.style.color =
            "#4bbcff";


        try {

            const response =
                await fetch(
                    `${API}/risk-threshold?safety_threshold=${encodeURIComponent(newThreshold)}`,
                    {
                        method: "PUT"
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Unable to update threshold"
                );
            }


            // Update displayed value

            thresholdDisplay.textContent =
                `${newThreshold}%`;


            thresholdInput.value =
                newThreshold;


            thresholdMsg.textContent =
                "Threshold updated successfully.";

            thresholdMsg.style.color =
                "#55d6a0";


        } catch (error) {

            console.error(
                "Update threshold error:",
                error
            );

            thresholdMsg.textContent =
                error.message ||
                "Unable to update threshold.";

            thresholdMsg.style.color =
                "#ff8996";
        }

    }
);


// =================================
// Load Threshold On Dashboard
// =================================

loadThreshold();

const fields = [
    "Age",
    "Gender",
    "Person_Income",
    "Employee_Experience",
    "Loan_Amount",
    "Loan_interest_Rate",
    "Loan_percentage",
    "Credit_History",
    "Credit_Score",
    "Previous_Loan",
    "Education",
    "Home_Onwership",
    "Loan_Intent"
];


// =================================
// Store Last Prediction
// =================================

let lastCustomerData = null;
let predictionCompleted = false;


// =================================
// Prediction
// =================================

document
    .getElementById("predictionForm")
    .addEventListener("submit", async (event) => {

        event.preventDefault();

        const message =
            document.getElementById("msg");

        message.textContent =
            "Analyzing application...";

        message.style.color =
            "#4bbcff";


        // Collect customer data

        const customerData = {};

        fields.forEach((field) => {

            const element =
                document.getElementById(field);

            if (element.type === "number") {

                customerData[field] =
                    Number(element.value);

            } else {

                customerData[field] =
                    element.value;
            }

        });


        try {

            // ================================
            // Call /predict
            // ================================

            const response =
                await fetch(
                    `${API}/predict`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                customerData
                            )
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Prediction failed"
                );
            }


            // ================================
            // Store Data
            // ================================

            lastCustomerData =
                customerData;

            predictionCompleted =
                true;


            // Enable Save button

            document.getElementById(
                "saveButton"
            ).disabled = false;


            // ================================
            // Display Result
            // ================================

            document
                .getElementById("result")
                .classList
                .remove("hidden");


            document.getElementById(
                "risk"
            ).textContent =
                `${Number(
                    data.risk_percentage
                ).toFixed(2)}%`;


            document.getElementById(
                "safety"
            ).textContent =
                `${Number(
                    data.safety_percentage
                ).toFixed(2)}%`;


            document.getElementById(
                "resultThreshold"
            ).textContent =
                `${Number(
                    data.threshold_used
                ).toFixed(0)}%`;


            document.getElementById(
                "decision"
            ).textContent =
                data.decision;


            message.textContent =
                "Prediction completed successfully.";

            message.style.color =
                "#55d6a0";


        } catch (error) {

            console.error(
                "Prediction error:",
                error
            );

            message.textContent =
                error.message ||
                "Prediction failed.";

            message.style.color =
                "#ff8996";
        }

    });


// =================================
// Save Prediction
// =================================

document
    .getElementById("saveButton")
    .addEventListener("click", async () => {

        if (
            !predictionCompleted ||
            !lastCustomerData
        ) {
            return;
        }


        const message =
            document.getElementById("msg");

        message.textContent =
            "Saving prediction...";

        message.style.color =
            "#4bbcff";


        try {

            // ================================
            // Call /save
            // ================================

            const response =
                await fetch(
                    `${API}/save`,
                    {
                        method: "POST",

                        headers: {
                            "Content-Type":
                                "application/json"
                        },

                        body:
                            JSON.stringify(
                                lastCustomerData
                            )
                    }
                );


            const data =
                await response.json();


            if (!response.ok) {

                throw new Error(
                    data.detail ||
                    "Unable to save prediction"
                );
            }


            // ================================
            // Success
            // ================================

            message.textContent =
                "Prediction saved successfully.";

            message.style.color =
                "#55d6a0";


            // Prevent duplicate save

            document.getElementById(
                "saveButton"
            ).disabled = true;


        } catch (error) {

            console.error(
                "Save error:",
                error
            );

            message.textContent =
                error.message ||
                "Unable to save prediction.";

            message.style.color =
                "#ff8996";
        }

    });