// Retrieve session token
const token = sessionStorage.getItem("session_token");

// Redirect if token is missing
if (!token) {
    window.location.href = "/login-page";
}


// Common function for authenticated API requests
async function apiRequest(url, options = {}) {

    const response = await fetch(url, {

        ...options,

        headers: {
            ...options.headers,
            "Authorization": `Bearer ${token}`
        }

    });

    if (response.status === 401) {

        sessionStorage.removeItem("session_token");

        window.location.href = "/login-page";

        throw new Error("Session expired or invalid");

    }

    return response;
}


// Load logged-in user information
async function loadUser() {

    try {

        const response = await apiRequest("/me");

        const user = await response.json();

        document.getElementById("welcome").textContent =
            `Welcome, ${user.username} | Role: ${user.role}`;

    } catch (error) {

        console.error(error);

    }

}


// Create a record
document.getElementById("recordForm").addEventListener(
    "submit",
    async function(event) {

        event.preventDefault();

        const title = document.getElementById("title").value;

        const body = document.getElementById("body").value;

        try {

            const response = await apiRequest("/records", {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    title: title,
                    body: body
                })

            });

            const result = await response.json();

            document.getElementById("recordMessage").textContent =
                result.message || result.error;

            if (response.ok) {

                document.getElementById("recordForm").reset();

                loadRecords();

            }

        } catch (error) {

            document.getElementById("recordMessage").textContent =
                error.message;

        }

    }
);


// Display records
async function loadRecords() {

    try {

        const response = await apiRequest("/records");

        const records = await response.json();

        const recordsList = document.getElementById("recordsList");

        recordsList.replaceChildren();

        if (records.length === 0) {

            recordsList.textContent = "No records found.";

            return;

        }

        records.forEach(record => {

            const item = document.createElement("div");

            item.className = "record-item";

            const title = document.createElement("h4");
            title.textContent = record.title;

            const id = document.createElement("p");
            id.textContent = `Record ID: ${record.id}`;

            const button = document.createElement("button");

            button.textContent = "View Details";

            button.addEventListener("click", () => {
                viewRecord(record.id);
            });

            item.append(title, id, button);

            recordsList.appendChild(item);

        });

    } catch (error) {

        console.error(error);

        document.getElementById("recordsList").textContent =
            "Unable to load records.";

    }

}


// View individual record
async function viewRecord(recordId) {

    try {

        const response = await apiRequest(`/records/${recordId}`);

        const result = await response.json();

        const details = document.getElementById("recordDetails");

        details.replaceChildren();

        if (!response.ok) {

            details.textContent = result.error || "Unable to retrieve record.";

            return;

        }

        const title = document.createElement("h4");
        title.textContent = result.title;

        const body = document.createElement("p");
        body.textContent = result.body;

        const date = document.createElement("p");
        date.textContent = `Created: ${result.created_at}`;

        details.append(title, body, date);

    } catch (error) {

        document.getElementById("recordDetails").textContent =
            error.message;

    }

}


// Logout
document.getElementById("logoutBtn").addEventListener("click", () => {

    sessionStorage.removeItem("session_token");

    window.location.href = "/login-page";

});


// Initialize dashboard
loadUser();
loadRecords();