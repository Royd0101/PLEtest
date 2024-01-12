document.addEventListener("DOMContentLoaded", function () {
  fetch("/department_total_fine/")
    .then((response) => response.json())
    .then((data) => {
      let barCanvas = document.querySelector("#myChart");
      let labels = Object.keys(data);
      let values = Object.values(data);

      let companyColors = {};
      labels.forEach((company, index) => {
        companyColors[company] = getRandomColor(index);
      });

      let myChart = new Chart(barCanvas, {
        type: "bar",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Total Penalty",
              data: values,
              backgroundColor: labels.map((label) => companyColors[label]),
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
});

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
