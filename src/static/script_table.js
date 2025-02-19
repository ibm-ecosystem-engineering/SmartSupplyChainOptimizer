  // Function to create a table
function createTable(data, selectButtonFlag) {
    
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const tbody = document.createElement("tbody");

    console.log (data)
    console.log (data[0])

    // Create table header
    const headerRow = document.createElement("tr");
    Object.keys(data[0]).forEach(key => {
        const th = document.createElement("th");
        th.textContent = key;
        headerRow.appendChild(th);
    });
    if (selectButtonFlag) {
        th = document.createElement("th");
        th.textContent = "Select";
        headerRow.appendChild(th);
    }

    thead.appendChild(headerRow);
    table.appendChild(thead);

    // Create table body
    data.forEach(item => {
        const row = document.createElement("tr");
        Object.values(item).forEach(value => {
            const td = document.createElement("td");
            td.textContent = value;
            row.appendChild(td);
        });
        if (selectButtonFlag)
            row.appendChild(createButton("Select"));
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    return table;
}

function createButton(label) {
    let newButton = document.createElement("button");
    newButton.innerText = label;
    // newButton.addEventListener("click", selectSupplier);
    return newButton
}

function createButton(label) {
    let newButton = document.createElement("button");
    newButton.innerText = label;
    newButton.className = "table-button"
    // newButton.addEventListener("click", selectSupplier);
    return newButton
}