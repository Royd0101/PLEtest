document.addEventListener("DOMContentLoaded", function () {
  var user_person_bar = document
    .getElementById("user_person_bar")
    .getContext("2d");

  fetch("http://127.0.0.1:8000/yearly_expired_license/")
    .then((response) => response.json())
    .then((data) => {
      // Check if the data has the expected structure
      if (typeof data.yearly_expired_counts === "object") {
        // Process the data to get yearly counts
        const yearlyCounts = {};
        Object.entries(data.yearly_expired_counts).forEach(
          ([year, totalExpired]) => {
            // Adjust based on actual property names
            year = year || totalExpired.expiry_date__year;
            yearlyCounts[year] = totalExpired;
          }
        );

        // Create an array of years and counts for the chart
        const years = Object.keys(yearlyCounts);
        const counts = Object.values(yearlyCounts);

        // Create the bar chart
        new Chart(user_person_bar, {
          type: "bar",
          data: {
            labels: years,
            datasets: [
              {
                label: "Total Expired Files",
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
      } else {
        console.error("Unexpected data structure:", data);
      }
    })
    .catch((error) => console.error("Error fetching data:", error));
});
