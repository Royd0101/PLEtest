document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/file/expired_documents/")
    .then((response) => response.json())
    .then((data1) => {
      fetch("/api/file/valid_documents/")
        .then((response) => response.json())
        .then((data2) => {
          fetch("/api/file/renewal_documents/")
            .then((response) => response.json())
            .then((data3) => {
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
      labels: ["Label 1", "Label 2", "Label 3", "Label 4", "Label 5"],
      datasets: [
        {
          label: "Data 1",
          data: data1,
          backgroundColor: "rgba(75, 192, 192, 0.2)",
          borderColor: "rgba(75, 192, 192, 1)",
          borderWidth: 1,
        },
        {
          label: "Data 2",
          data: data2,
          backgroundColor: "rgba(255, 99, 132, 0.2)",
          borderColor: "rgba(255,99,132,1)",
          borderWidth: 1,
        },
        {
          label: "Data 3",
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
