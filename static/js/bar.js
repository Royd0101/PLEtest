const barCanvas = document.querySelector("#bar");

// Fetch data from APIs
Promise.all([
  fetch("/api/file/valid_documents"),
  fetch("/api/file/renewal_documents"),
  fetch("/api/file/expired_documents"),
])
  .then((responses) => Promise.all(responses.map((res) => res.json())))
  .then((data) => {
    const myChart = new Chart(barCanvas, {
      type: "bar",
      data: {
        labels: ["Valid", "For Renewal", "Expired"],
        datasets: [
          {
            label: "Documents",
            data: data.map((apiData) => apiData.length),
            backgroundColor: [
              "rgba(0, 128, 0, 0.2)", // Lighter green
              "rgba(255, 165, 0, 0.2)", // Lighter orange for warning
              "rgba(255, 0, 0, 0.2)", // Lighter red for danger
            ],
            borderColor: [
              "rgba(0, 128, 0, 1)", // Full green
              "rgba(255, 165, 0, 1)", // Full orange for warning
              "rgba(255, 0, 0, 1)", // Full red for danger
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
  .catch((error) => {
    console.error("Error fetching data:", error);
  });
