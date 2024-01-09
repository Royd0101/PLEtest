const person_barCanvas = document.querySelector("#person_bar");

// Fetch data from the API
fetch("/api/receipts/person_receipt/")
  .then((response) => response.json())
  .then((data) => {
    // Group data by company and year of timestamp
    const groupedData = groupDataByCompanyAndYear(data);

    // Extract labels and total fines for each company and year
    const labels = [];
    const totalFines = [];
    const companyColors = {}; // Store colors for each company

    Object.keys(groupedData).forEach((company, index) => {
      // Use the same color logic as the pie chart
      const color = getRandomColor(index);
      companyColors[company] = color;

      Object.keys(groupedData[company]).forEach((timestamp) => {
        const yearData = groupedData[company][timestamp];
        labels.push(`${company} - ${timestamp}`);
        totalFines.push(
          yearData.reduce((sum, entry) => sum + parseFloat(entry.fined), 0)
        );
      });
    });

    // Create the bar chart
    const myChart = new Chart(person_barCanvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Total Fine",
            data: totalFines,
            backgroundColor: labels.map(
              (label) => companyColors[label.split(" - ")[0]]
            ),
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          yAxes: [
            {
              ticks: {
                beginAtZero: true,
              },
            },
          ],
        },
      },
    });
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });

// Helper function to group data by company and year of timestamp
function groupDataByCompanyAndYear(data) {
  return data.reduce((result, entry) => {
    const company = entry.company_name;
    const timestamp = new Date(entry.timestamp).getFullYear();

    if (!result[company]) {
      result[company] = {};
    }

    if (!result[company][timestamp]) {
      result[company][timestamp] = [];
    }

    result[company][timestamp].push(entry);
    return result;
  }, {});
}

// Helper function to generate a random color
function getRandomColor(index) {
  const colors = [
    "rgba(255, 99, 132, 0.4)", // Lighter red
    "rgba(4, 102, 139, 1)", // Lighter blue
    "rgba(255, 206, 86, 0.4)", // Lighter yellow
    "rgba(75, 192, 192, 0.4)", // Lighter green
    "rgba(153, 102, 255, 0.4)", // Lighter purple
    "rgba(255, 159, 64, 0.4)", // Lighter orange
    "rgba(0, 255, 0, 0.4)", // Lighter lime green
    "rgba(0, 0, 255, 0.4)", // Lighter navy blue
    "rgba(128, 0, 128, 0.4)", // Lighter purple
  ];

  return colors[index % colors.length];
}
