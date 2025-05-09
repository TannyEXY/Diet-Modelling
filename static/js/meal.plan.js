// Fetch food data from Flask API and store in sessionStorage
function fetchFoodData() {
    fetch('/get-food')
        .then(response => response.json())
        .then(data => {
            if (data) {
                sessionStorage.setItem("food", JSON.stringify(data)); // Store in sessionStorage
                console.log("Food Data Saved:", data);
                displayTable(); // Ensure table updates once data is available
            }
        })
        .catch(error => console.error('Error fetching food data:', error));
}

// Ensure data is retrieved after fetch completes
function getStoredData() {
    const storedData = sessionStorage.getItem("food");
    return storedData ? JSON.parse(storedData) : [];
}

let currentPage = 1;
const rowsPerPage = 10;

// Display paginated table
function displayTable() {
    const tbody = document.querySelector("#dataTable tbody");
    tbody.innerHTML = "";

    const data = getStoredData();
    if (!data.length) return; // Prevent rendering empty table

    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = startIndex + rowsPerPage;
    let ib = startIndex;

    for (let i = startIndex; i < endIndex && i < data.length; i++) {
        const row = `<tr>
            ${data[i].map(item => `<td>${item}</td>`).join("")}
        </tr>`;
        tbody.innerHTML += row;
        ib = i;
    }

    document.getElementById("pageInfo").innerText = `Showing ${startIndex + 1} to ${ib + 1} entries of ${data.length} entries`;
    document.getElementById("pageNumber").innerText = `Page ${currentPage}`;
}

// Pagination Controls
function nextPage() {
    const data = getStoredData();
    if (currentPage * rowsPerPage < data.length) {
        currentPage++;
        displayTable();
    }
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        displayTable();
    }
}

// Navigation Functions
function back() {
    window.location.href = "/meals/add";
}

function done() {
    sessionStorage.removeItem("food");
    window.location.href = "/meal/plan/add/basket";
}

// Ensure data is fetched when the page loads
window.onload = fetchFoodData;
