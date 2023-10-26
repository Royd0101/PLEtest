async function generatePieChart() {
  const validFileCount = await fetchFileCount("/api/file/valid_documents/");
  const expiredFileCount = await fetchFileCount("/api/file/expired_documents/");
  const toBeRenewedFileCount = await fetchFileCount(
    "/api/file/renewal_documents/"
  );

  const data = {
    labels: ["Valid Files", "Expired Files", "To Be Renewed Files"],
    datasets: [
      {
        data: [validFileCount, expiredFileCount, toBeRenewedFileCount],
        backgroundColor: [
          "rgb(0, 128, 0)",
          "rgb(255, 165, 0)",
          "rgb(255, 0, 0)",
        ],
        backgroundColor: [
          "rgb(0, 128, 0)",
          "rgb(255, 165, 0)",
          "rgb(255, 0, 0)",
        ],
        borderWidth: 3,
      },
    ],
    options: {
      legend: {
        display: false,
      },
    },
  };

  const ctx = document.getElementById("pieChart").getContext("2d");
  const config = {
    type: "pie",
    data: data,
  };
  new Chart(ctx, config);
}

async function fetchFileCount(endpoint) {
  try {
    const response = await fetch(endpoint);
    const data = await response.json();
    return data.length;
  } catch (error) {
    console.error(`Error fetching file count from ${endpoint}:`, error);
    return 0;
  }
}

generatePieChart();
