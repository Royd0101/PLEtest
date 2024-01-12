document.addEventListener("DOMContentLoaded", function () {
  var person_canvas_pie = document
    .getElementById("user_person_pie")
    .getContext("2d");

  fetch("http://127.0.0.1:8000/yearly_expired_files_by_month/")
    .then((response) => response.json())
    .then((data) => {
      if ("monthly_expired_counts" in data) {
        const monthlyCounts = data.monthly_expired_counts;

        const months = Object.keys(monthlyCounts);
        const counts = Object.values(monthlyCounts);

        months.forEach((month, index) => {
          console.log(`Month: ${month}, Total: ${counts[index]}`);
        });

        const currentYear = new Date().getFullYear();

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
              text: "Expired Licenses for Year " + currentYear,
            },
          },
        });
      } else {
        console.error("Unexpected data structure:", data);
      }
    })
    .catch((error) => console.error("Error fetching data:", error));
});
