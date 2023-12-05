var data = {
  labels: ["Category 1", "Category 2", "Category 3"],
  datasets: [
    {
      data: [30, 50, 20],
      backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
      hoverBackgroundColor: ["#FF6384", "#36A2EB", "#FFCE56"],
    },
  ],
};

// Get the canvas element
var ctx = document.getElementById("#myPieChart").getContext("2d");

// Create a pie chart
var myPieChart = new Chart(ctx, {
  type: "pie",
  data: data,
  options: {
    tooltips: {
      callbacks: {
        label: function (tooltipItem, data) {
          var dataset = data.datasets[tooltipItem.datasetIndex];
          var total = dataset.data.reduce(function (
            previousValue,
            currentValue,
            currentIndex,
            array
          ) {
            return previousValue + currentValue;
          });
          var currentValue = dataset.data[tooltipItem.index];
          var percentage = ((currentValue / total) * 100).toFixed(2);
          return currentValue + " (" + percentage + "%)";
        },
      },
    },
  },
});
