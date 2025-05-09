// Fetch food data from Flask API and store in sessionStorage
function fetchFoodData() {
    fetch('/get-food/table')
        .then(response => response.json())
        .then(data => {
            if (data) {
                sessionStorage.setItem("table", JSON.stringify(data)); // Store data in sessionStorage
                console.log("Food Data Saved:", data);
                displayTable(); // Ensure table updates after data is fetched
            }
        })
        .catch(error => console.error('Error fetching food data:', error));
}

// Ensure data is retrieved after fetch completes
function getStoredData() {
    const storedData = sessionStorage.getItem("table");
    return storedData ? JSON.parse(storedData) : [];
}

let currentPage = 1;
const rowsPerPage = 10;

// Display paginated table
function displayTable() {
    const tbody = document.querySelector("#printTable tbody");
    tbody.innerHTML = "";

    const data = getStoredData();
    if (!data.length) return; // Prevent rendering empty table

    const startIndex = (currentPage - 1) * rowsPerPage;
    const endIndex = Math.min(startIndex + rowsPerPage, data.length);
    let ib = 0;
    for (let i = startIndex; i < endIndex; i++) {
        const row = `<tr>${data[i].map(item => `<td>${item}</td>`).join("")}</tr>`;
        tbody.innerHTML += row;
        ib=i;
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

// Print Table - Ensure `span` exists before modifying it
function printTable() {
    const spanElement = document.getElementById("span");
    if (spanElement) spanElement.style.display = "none"; 

    window.print(); // Prints the page

    if (spanElement) spanElement.style.display = "block"; 
}

// Download Table as PDF - Ensure proper data formatting
function downloadTable() {
    const { jsPDF } = window.jspdf;
    const doc = new jsPDF();
    const data = getStoredData(); // Ensure data is retrieved properly
    doc.text("Food Basket", 14, 10); // Add title to the PDF
    doc.autoTable({
        head: [['Food Group', 'Fopd', 'Portions(grams)', 'Portions(kgs)']], // Adjust headers
        body: data.map(row => row.slice(0, 4)), // Limit to 4 columns for consistency
    });

    doc.save('table-data.pdf'); // Downloads the PDF
}

// Clear session data and redirect
function done() {
    sessionStorage.removeItem("table");
    window.location.href = "/";
}

// Ensure data is fetched when the page loads
window.onload = fetchFoodData;
