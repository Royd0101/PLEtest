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
          "rgba(75, 192, 192, 0.2)",
          "rgba(255, 99, 132, 0.2)",
          "rgba(255, 206, 86, 0.2)",
        ],
        borderColor: [
          "rgba(75, 192, 192, 1)",
          "rgba(255, 99, 132, 1)",
          "rgba(255, 206, 86, 1)",
        ],
        borderWidth: 1,
      },
    ],
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
