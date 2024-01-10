document.addEventListener("DOMContentLoaded", function () {
  // Get the 2D context of the canvas
  var canvas_bar_person = document
    .getElementById("person_bar")
    .getContext("2d");

  // Fetch data from the API
  fetch("http://127.0.0.1:8000/api/file/Person_log/")
    .then((response) => response.json())
    .then((data) => {
      // Log the fetched data for debugging
      console.log("Fetched data:", data);

      // Process the data to get yearly counts for renewed files
      const renewedCounts = {};
      data.forEach((entry) => {
        if (entry.action === "Renewed") {
          // Extract the year from the 'expiry_date' property
          const year = new Date(entry.expiry_date).getFullYear();
          // Increment the count for renewed files in the corresponding year
          renewedCounts[year] = (renewedCounts[year] || 0) + 1;
        }
      });

      // Log the renewed counts for debugging
      console.log("Renewed Counts:", renewedCounts);

      // Create an array of years and counts for the chart
      const years = Object.keys(renewedCounts);
      const counts = Object.values(renewedCounts);

      // Create the bar chart
      new Chart(canvas_bar_person, {
        type: "bar",
        data: {
          labels: years,
          datasets: [
            {
              label: "Expired License",
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
    })
    .catch((error) => console.error("Error fetching data:", error));
});
