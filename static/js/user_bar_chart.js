document.addEventListener("DOMContentLoaded", function () {
  function updateBarChart() {
    var ctx = document.getElementById("barChart").getContext("2d");

    // Define the URLs for your endpoints
    var expiredEndpoint = "/api/file/expired/";
    var validEndpoint = "/api/file/valid_file/";
    var toBeRenewEndpoint = "/api/file/to_be_renew/";

    function fetchData(endpoint) {
      return $.ajax({
        url: endpoint,
        method: "GET",
        success: function (data) {
          return data;
        },
      });
    }

    Promise.all([
      fetchData(expiredEndpoint),
      fetchData(validEndpoint),
      fetchData(toBeRenewEndpoint),
    ]).then(function (data) {
      var totalExpired = data[0].length;
      var totalValid = data[1].length;
      var totalToBeRenew = data[2].length;

      var chartData = {
        labels: ["Expired", "Valid", "To Be Renewed"],
        datasets: [
          {
            label: "Total",
            data: [totalExpired, totalValid, totalToBeRenew],
            backgroundColor: [
              "rgba(255, 99, 132, 0.5)",
              "rgba(75, 192, 192, 0.5)",
              "rgba(255, 205, 86, 0.5)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(255, 205, 86, 1)",
            ],
            borderWidth: 1,
          },
        ],
      };

      var options = {
        scales: {
          y: {
            beginAtZero: true,
          },
        },
      };

      var barChart = new Chart(ctx, {
        type: "bar",
        data: chartData,
        options: options,
      });
    });
  }

  updateBarChart();
});
