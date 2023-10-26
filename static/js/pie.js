var ctx = document.getElementById("barChart").getContext("2d");

// Fetch data from API endpoints
Promise.all([
  fetch("/api/file/valid_documents"),
  fetch("/api/file/renewal_documents"),
  fetch("/api/file/expired_documents"),
])
  .then((responses) =>
    Promise.all(responses.map((response) => response.json()))
  )
  .then((data) => {
    var barChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["Valid", "For Renewal", "Expired"],
        datasets: [
          {
            label: "Documents",
            data: [data[0].length, data[1].length, data[2].length],
            backgroundColor: [
              "rgba(54, 162, 235, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(255, 99, 132, 0.2)",
            ],
            borderColor: [
              "rgba(54, 162, 235, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(255, 99, 132, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
      options: {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      },
    });
  })
  .catch((error) => console.error("Error fetching data:", error));
