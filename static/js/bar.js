const barCanvas = document.querySelector("#bar");

// Fetch data from the API
fetch("/api/receipts/")
  .then((response) => response.json())
  .then((data) => {
    // Group data by company and year of invoice_date
    const groupedData = groupDataByCompanyAndYear(data);

    // Extract labels and total fines for each company and year
    const labels = [];
    const totalFines = [];
    const companyColors = {}; // Store colors for each company

    Object.keys(groupedData).forEach((company, index) => {
      // Use the same color logic as the pie chart
      const color = getRandomColor(index);
      companyColors[company] = color;

      Object.keys(groupedData[company]).forEach((invoiceDate) => {
        const yearData = groupedData[company][invoiceDate];
        labels.push(`${company} - ${invoiceDate}`);
        totalFines.push(
          yearData.reduce((sum, entry) => sum + parseFloat(entry.fined), 0)
        );
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

// Helper function to group data by company and year of invoice_date
function groupDataByCompanyAndYear(data) {
  return data.reduce((result, entry) => {
    const company = entry.company_name;
    const invoiceDate = new Date(entry.invoice_date).getFullYear();

    if (!result[company]) {
      result[company] = {};
    }

    if (!result[company][invoiceDate]) {
      result[company][invoiceDate] = [];
    }

    result[company][invoiceDate].push(entry);
    return result;
  }, {});
}

// Helper function to generate a random color
function getRandomColor(index) {
  const colors = [
    "rgba(255, 99, 132, 0.4)", // Lighter red
    "rgba(4, 102, 139, 1)", // Lighter blue
    // ... (other colors)
  ];

  return colors[index % colors.length];
}
