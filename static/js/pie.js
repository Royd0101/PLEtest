const pieCanvas = document.querySelector("#pie"); // Assuming you have an HTML element with id="pie" for the pie chart

fetch("/api/receipts/")
  .then((response) => response.json())
  .then((data) => {
    const currentYear = new Date().getFullYear();

    // Filter data for the current year
    const currentYearData = data.filter(
      (entry) => new Date(entry.expiry_date).getFullYear() === currentYear
    );

    // Group data by company
    const groupedData = groupDataByCompany(currentYearData);

    // Extract labels and total fines for each company
    const labels = Object.keys(groupedData).sort(); // Sort companies alphabetically
    const totalFines = labels.map((company) =>
      groupedData[company].reduce(
        (sum, entry) => sum + parseFloat(entry.fined),
        0
      )
    );

    // Generate colors using the same logic as the bar chart
    const companyColors = {};
    labels.forEach((company, index) => {
      companyColors[company] = getRandomColor(index);
    });

    // Create the pie chart
    const myPieChart = new Chart(pieCanvas, {
      type: "pie",
      data: {
        labels: labels,
        datasets: [
          {
            data: totalFines,
            backgroundColor: labels.map((company) => companyColors[company]),
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
        },
        title: {
          display: true,
          text: `Total Penalty for ${currentYear}`,
          fontSize: 16,
        },
      },
    });
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });

// Helper function to group data by company
function groupDataByCompany(data) {
  return data.reduce((result, entry) => {
    const company = entry.company_name;

    if (!result[company]) {
      result[company] = [];
    }

    result[company].push(entry);
    return result;
  }, {});
}

// Helper function to generate a random color
function getRandomColor(index) {
  const colors = [
    "rgba(255, 99, 132, 0.4)", // Lighter red
    "rgba(54, 162, 235, 0.4)", // Lighter blue
    "rgba(255, 206, 86, 0.4)", // Lighter yellow
    "rgba(75, 192, 192, 0.4)", // Lighter green
    // Add more colors as needed
  ];

  return colors[index % colors.length];
}
