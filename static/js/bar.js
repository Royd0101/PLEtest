const barCanvas = document.querySelector("#bar");

// Fetch data from the API
fetch("/api/receipts/")
  .then((response) => response.json())
  .then((data) => {
    // Group data by company and agency
    const groupedData = groupDataByCompanyAndAgency(data);

    // Extract labels, total fines, and document counts for each company and agency
    const labels = [];
    const totalFines = [];
    const documentCounts = [];
    const companyColors = {}; // Store colors for each company

    Object.keys(groupedData).forEach((company, index) => {
      const color = getRandomColor(index); // Generate a random color for each company
      companyColors[company] = color;

      Object.keys(groupedData[company]).forEach((agency) => {
        const agencyData = groupedData[company][agency];
        labels.push(`${company} - ${agency}`);
        totalFines.push(
          agencyData.reduce((sum, entry) => sum + parseFloat(entry.fined), 0)
        );
        documentCounts.push(agencyData.length);
      });
    });

    // Create the bar chart
    const myChart = new Chart(barCanvas, {
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
          {
            label: "Document Count",
            data: documentCounts,
            backgroundColor: "rgba(173, 216, 230, 0.4)", // Lighter blue
            borderColor: "rgba(70, 130, 180, 1)", // Steel blue
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

// Helper function to group data by company and agency
function groupDataByCompanyAndAgency(data) {
  return data.reduce((result, entry) => {
    const company = entry.company_name;
    const agency = entry.agency;

    if (!result[company]) {
      result[company] = {};
    }

    if (!result[company][agency]) {
      result[company][agency] = [];
    }

    result[company][agency].push(entry);
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
