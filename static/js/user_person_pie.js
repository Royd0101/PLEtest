document.addEventListener("DOMContentLoaded", function () {
  var person_canvas_pie = document
    .getElementById("user_person_pie")
    .getContext("2d");

  fetch("http://127.0.0.1:8000/yearly_expired_files_by_month/")
    .then((response) => response.json())
    .then((data) => {
      // Check if the data has the expected structure
      if ("monthly_expired_counts" in data) {
        // Process the data to get monthly counts
        const monthlyCounts = data.monthly_expired_counts;

        // Create an array of months and counts for the chart
        const months = Object.keys(monthlyCounts);
        const counts = Object.values(monthlyCounts);

        // Create the pie chart
        new Chart(person_canvas_pie, {
          type: "doughnut",
          data: {
            labels: months,
            datasets: [
              {
                label: "Monthly Expired Files",
                data: counts,
                backgroundColor: [
                  "rgba(255, 99, 132, 0.4)", // Lighter red
                  "rgba(4, 102, 139, 1)", // Lighter blue
                  "rgba(255, 206, 86, 0.4)", // Lighter yellow
                  "rgba(75, 192, 192, 0.4)", // Lighter green
                  "rgba(153, 102, 255, 0.4)", // Lighter purple
                  "rgba(255, 159, 64, 0.4)", // Lighter orange
                  "rgba(0, 255, 0, 0.4)", // Lighter lime green
                  "rgba(0, 0, 255, 0.4)", // Lighter navy blue
                  "rgba(128, 0, 128, 0.4)", // Lighter purple
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
        });
      } else {
        console.error("Unexpected data structure:", data);
      }
    })
    .catch((error) => console.error("Error fetching data:", error));
});
