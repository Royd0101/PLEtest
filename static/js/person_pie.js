document.addEventListener("DOMContentLoaded", function () {
  // Get the canvas element
  const canvasperson_pie = document.getElementById("person_pie");

  // Fetch data from the API
  fetch("http://127.0.0.1:8000/api/file/Person_log/")
    .then((response) => response.json())
    .then((data) => {
      // Filter data for the current year and renewed files
      const currentYear = new Date().getFullYear();
      const filteredData = data.filter(
        (entry) =>
          entry.action === "Renewed" &&
          new Date(entry.expiry_date).getFullYear() === currentYear
      );

      // Process the data to get monthly counts
      const monthlyCounts = {};
      filteredData.forEach((entry) => {
        const month = new Date(entry.expiry_date).getMonth(); // Month is 0-indexed
        const monthName = new Date(entry.expiry_date).toLocaleString(
          "default",
          { month: "long" }
        );
        monthlyCounts[monthName] = (monthlyCounts[monthName] || 0) + 1;
      });

      // Create an array of labels and data for the chart
      const labels = Object.keys(monthlyCounts);
      const counts = Object.values(monthlyCounts);

      // Create the pie chart
      const PersonPieChart = new Chart(canvasperson_pie, {
        type: "doughnut",
        data: {
          labels: labels,
          datasets: [
            {
              label: "Monthly Renewed Licenses",
              data: counts,
              backgroundColor: [
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)",
                "rgba(255, 159, 64, 0.2)",
                "rgba(255, 99, 132, 0.2)",
                "rgba(54, 162, 235, 0.2)",
                "rgba(255, 206, 86, 0.2)",
                "rgba(75, 192, 192, 0.2)",
                "rgba(153, 102, 255, 0.2)",
                "rgba(255, 159, 64, 0.2)",
              ],
              borderColor: [
                "rgba(255, 99, 132, 1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
                "rgba(255, 159, 64, 1)",
                "rgba(255, 99, 132, 1)",
                "rgba(54, 162, 235, 1)",
                "rgba(255, 206, 86, 1)",
                "rgba(75, 192, 192, 1)",
                "rgba(153, 102, 255, 1)",
                "rgba(255, 159, 64, 1)",
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          title: {
            display: true,
            text: "Monthly Renewed Licenses for " + currentYear,
          },
        },
      });
    })
    .catch((error) => console.error("Error fetching data:", error));
});
