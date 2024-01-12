document.addEventListener("DOMContentLoaded", function () {
  fetch("/department_total_fine/")
    .then((response) => response.json())
    .then((data) => {
      let pieCanvas = document.querySelector("#myPieChart");
      let labels = Object.keys(data);
      let values = Object.values(data);
      let currentYear = new Date().getFullYear();

      // Filter data for the current year
      let currentYearData = labels.reduce((result, label, index) => {
        let year = parseInt(label.split(" - ")[1]);
        if (year === currentYear) {
          result[label] = values[index];
        }
        return result;
      }, {});

      let pieLabels = Object.keys(currentYearData);
      let pieValues = Object.values(currentYearData);

      let companyColors = {};
      pieLabels.forEach((label, index) => {
        companyColors[label] = getRandomColor(index);
      });

      let legendList = document.getElementById("UserlegendList");
      legendList.innerHTML = ""; // Clear the previous legend items

      let myPieChart = new Chart(pieCanvas, {
        type: "doughnut",
        data: {
          labels: pieLabels,
          datasets: [
            {
              data: pieValues,
              backgroundColor: pieLabels.map((label) => companyColors[label]),
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              display: false, // Hide the default legend
            },
          },
          title: {
            display: true,
            text: `Total Penalty for ${currentYear}`,
            fontSize: 20,
          },
          tooltips: {
            callbacks: {
              label: function (tooltipItem, data) {
                let label = pieLabels[tooltipItem.index];
                let totalValue = pieValues[tooltipItem.index];

                // Extract the department name without the year
                let departmentName = label.split(" ")[0];

                return `${departmentName}: ${totalValue}`;
              },
            },
          },
        },
      });

      // Generate legend items dynamically
      pieLabels.forEach((label, index) => {
        let totalValue = pieValues[index];
        let percentage = (
          (totalValue / pieValues.reduce((acc, val) => acc + val, 0)) *
          100
        ).toFixed(2);

        // Remove the year from the label
        let departmentName = label.split(" ")[0];

        // Append legend item to the list
        let listItem = document.createElement("li");
        listItem.textContent = `${departmentName}: ${percentage}%`;
        legendList.appendChild(listItem);
      });
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
});

// Helper function to generate a random color
function getRandomColor(index) {
  const colors = [
    "rgba(255, 99, 132, 0.4)",
    "rgba(4, 102, 139, 1)",
    "rgba(255, 206, 86, 0.4)",
    "rgba(75, 192, 192, 0.4)",
    "rgba(153, 102, 255, 0.4)",
    "rgba(255, 159, 64, 0.4)",
    "rgba(0, 255, 0, 0.4)",
    "rgba(0, 0, 255, 0.4)",
    "rgba(128, 0, 128, 0.4)",
  ];

  return colors[index % colors.length];
}
