const PieCanvas = document.querySelector("#user_pie");

// Fetch data from the API
fetch("/api/receipts/receipt/")
  .then((response) => response.json())
  .then((data) => {
    // Group data by department
    const groupedData = groupDataByDepartment(data);

    // Extract labels and total fines for each department
    const labels = [];
    const totalFines = [];
    const departmentColors = {}; // Store colors for each department

    Object.keys(groupedData).forEach((department, index) => {
      const color = getRandomColor(index); // Generate a random color for each department
      departmentColors[department] = color;

      const departmentData = groupedData[department];
      labels.push(department);
      totalFines.push(
        departmentData.reduce((sum, entry) => sum + parseFloat(entry.fined), 0)
      );
    });

    // Create the bar chart
    const myChart = new Chart(PieCanvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Total Fine",
            data: totalFines,
            backgroundColor: labels.map((label) => departmentColors[label]),
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

// Helper function to group data by department
function groupDataByDepartment(data) {
  return data.reduce((result, entry) => {
    const department = entry.department_name;

    if (!result[department]) {
      result[department] = [];
    }

    result[department].push(entry);
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
