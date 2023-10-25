const canvas = document.querySelector("#myCanvas");
const ctx = canvas.getContext("2d");

canvas.width = 500;
canvas.height = 300;

const chart = new Chart(ctx, {
  type: "line",
  data: {
    labels: ["File 1", "File 2", "File 3"],
    datasets: [
      {
        data: [
          "{{ num_valid_files }}",
          "{{ num_renew_files }}",
          "{{ num_expired_files }}",
        ],
        backgroundColor: "rgba(255, 0, 0, 0.5)",
        borderColor: "rgb(255, 0, 0)",
        borderWidth: 2,
      },
    ],
  },
  options: {
    title: {
      display: true,
      text: "File Expiry Dates",
    },
    legend: {
      display: false,
    },
  },
});
