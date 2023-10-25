document.addEventListener("DOMContentLoaded", function () {
  console.log("Fetching data...");
  fetch("/api/file/expired_documents/")
    .then((response) => response.json())
    .then((data1) => {
      console.log("Data 1:", data1);
      fetch("/api/file/valid_documents/")
        .then((response) => response.json())
        .then((data2) => {
          console.log("Data 2:", data2);
          fetch("/api/file/renewal_documents/")
            .then((response) => response.json())
            .then((data3) => {
              console.log("Data 3:", data3);
              createGraph(data1, data2, data3);
            });
        });
    });
});

function createGraph(data1, data2, data3) {
  var ctx = document.getElementById("bar-chart").getContext("2d");

  var chart = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["Label 1", "Label 2", "Label 3"],
      datasets: [
        {
          label: "Expired",
          data: data1,
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
        {
          label: "Valid",
          data: data2,
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255,99,132,1)",
          borderWidth: 1,
        },
        {
          label: "Due for Renewal",
          data: data3,
          backgroundColor: "rgba(255, 206, 86, 0.2)",
          borderColor: "rgba(255, 206, 86, 1)",
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
}
