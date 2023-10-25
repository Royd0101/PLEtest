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
          // Change these colors to fit the black background
          "rgba(144, 238, 144, 0.8)",
          "rgba(255, 102, 102, 0.8)",
          "rgba(255, 230, 0, 0.8)",
        ],
        borderColor: [
          // Change these colors to fit the black background
          "rgba(144, 238, 144, 0.8)",
          "rgba(255, 102, 102, 0.8)",
          "rgba(255, 230, 0, 0.8)",
        ],
        borderWidth: 3,
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
