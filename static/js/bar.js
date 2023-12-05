const barCanvas = document.querySelector("#bar");

fetch("/api/receipts/")
  .then((response) => response.json())
  .then((data) => {
    const groupedData = groupDataByCompanyAndYear(data);

    const labels = [];
    const totalFines = [];
    const companyColors = {};

    Object.keys(groupedData).forEach((company, index) => {
      const color = getRandomColor(index);
      companyColors[company] = color;

      Object.keys(groupedData[company]).forEach((year) => {
        const yearData = groupedData[company][year];
        labels.push(`${company} - ${year}`);
        totalFines.push(
          yearData.reduce((sum, entry) => sum + parseFloat(entry.fined), 0)
        );
      });
    });

    const options = {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    };

    console.log("Options:", options);

    const myChart = new Chart(barCanvas, {
      type: "bar",
      data: {
        labels: labels,
        datasets: [
          {
            label: "Total Fine",
            data: totalFines,
            backgroundColor: labels.map(
              (label) => companyColors[label.split(" - ")[0]]
            ),
            borderWidth: 1,
          },
        ],
      },
      options: options,
    });
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });

function groupDataByCompanyAndYear(data) {
  return data.reduce((result, entry) => {
    const company = entry.company_name;
    const expiryYear = new Date(entry.expiry_date).getFullYear();

    if (!result[company]) {
      result[company] = {};
    }

    if (!result[company][expiryYear]) {
      result[company][expiryYear] = [];
    }

    result[company][expiryYear].push(entry);
    return result;
  }, {});
}

function getRandomColor(index) {
  const colors = [
    "rgba(255, 99, 132, 0.4)",
    "rgba(54, 162, 235, 0.4)",
    "rgba(255, 206, 86, 0.4)",
    "rgba(75, 192, 192, 0.4)",
    "rgba(153, 102, 255, 0.4)",
    "rgba(255, 159, 64, 0.4)",
    "rgba(0, 255, 0, 0.4)",
    "rgba(0, 0, 255, 0.4)",
    "rgba(128, 0, 128, 0.4)",
  ];

  return colors[index % colors.length];
}
