document.addEventListener("DOMContentLoaded", function () {
  // Get the canvas element
  const canvasperson_pie = document.getElementById("person_pie");

  // Fetch data from the API
  fetch("http://127.0.0.1:8000/api/file/Person_log/")
    .then((response) => response.json())
    .then((data) => {
      // Get the current date and year
      const currentDate = new Date();
      const currentYear = currentDate.getFullYear();

      // Filter data for expired files based on the current year and date
      const expiredData = data.filter(
        (entry) =>
          new Date(entry.expiry_date).getFullYear() === currentYear &&
          new Date(entry.expiry_date) < currentDate
      );

      // Process the data to get monthly counts
      const monthlyCounts = {};
      expiredData.forEach((entry) => {
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
              label: "Monthly Expired Licenses",
              data: counts,
              backgroundColor: [
                "rgba(4, 102, 139, 1)", // Lighter blue
                "rgba(255, 99, 132, 0.4)", // Lighter red
                "rgba(255, 206, 86, 0.4)", // Lighter yellow
                "rgba(75, 192, 192, 0.4)", // Lighter green
                "rgba(153, 102, 255, 0.4)", // Lighter purple
                "rgba(255, 159, 64, 0.4)", // Lighter orange
                "rgba(0, 255, 0, 0.4)", // Lighter lime green
                "rgba(0, 0, 255, 0.4)", // Lighter navy blue
                "rgba(128, 0, 128, 0.4)", // Lighter purple
              ],
              borderWidth: 1,
            },
          ],
        },
        options: {
          title: {
            display: true,
            text: `Expired Licenses for Year ${currentYear}`,
          },
        },
      });
    })
    .catch((error) => console.error("Error fetching data:", error));
});
