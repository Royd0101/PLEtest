const pieCanvas = document.querySelector("#pie");
const chartTitleElement = document.querySelector("#chartTitle");
const chartYearElement = document.querySelector("#chartYear");

fetch("/api/receipts/")
  .then((response) => response.json())
  .then((data) => {
    console.log("Fetched data:", data);

    const currentYear = new Date().getFullYear();

    const currentYearData = data.filter((entry) => {
      const entryYear = new Date(entry.invoice_date).getFullYear();
      return entryYear === currentYear;
    });

    const groupedData = groupDataByCompany(currentYearData);

    const labels = Object.keys(groupedData).sort();

    const totalFines = labels.map((company) =>
      groupedData[company].reduce((sum, entry) => {
        return sum + parseFloat(entry.fined);
      }, 0)
    );

    console.log(totalFines);
    const totalFine = totalFines.reduce((sum, amount) => sum + amount, 0);

    labels.forEach((company, index) => {
      const companyPercentage = ((totalFines[index] / totalFine) * 100).toFixed(
        2
      );
    });

    const companyColors = {};
    labels.forEach((company, index) => {
      companyColors[company] = getRandomColor(index);
    });

    const myPieChart = new Chart(pieCanvas, {
      type: "doughnut",
      data: {
        labels: labels,
        datasets: [
          {
            data: totalFines,
            backgroundColor: labels.map((company) => companyColors[company]),
            datalabels: {
              display: false,
            },
          },
        ],
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false,
          },
          tooltip: {
            callbacks: {
              label: (context) => {
                const label = context.label || "";
                const value = context.parsed || 0;
                const companyIndex = labels.indexOf(label);
                const companyPercentage = (
                  (totalFines[companyIndex] / totalFine) *
                  100
                ).toFixed(2);
                const amount = value.toFixed(0);

                return `${label}: ${companyPercentage}% (${amount})`;
              },
            },
          },
          datalabels: {
            color: "white",
            font: {
              weight: "bold",
              size: 14,
              display: false,
            },
            formatter: (value, context) => {
              const companyIndex = labels.indexOf(
                context.chart.data.labels[context.dataIndex]
              );
              const companyPercentage = (
                (totalFines[companyIndex] / totalFine) *
                100
              ).toFixed(2);
              return `${companyPercentage}%`;
            },
          },
        },
        title: {
          display: true,
          text: `Total Penalty for ${currentYear}`,
          fontSize: 16,
        },
      },
    });

    // Populate the legend
    const legendList = document.querySelector("#legendList");

    labels.forEach((company, index) => {
      const companyPercentage = ((totalFines[index] / totalFine) * 100).toFixed(
        2
      );
      const amount = totalFines[index].toFixed(0);

      // Create legend item
      const legendItem = document.createElement("li");
      legendItem.innerHTML = `
            <span style="background-color: ${companyColors[company]};"></span>
            <span>${company}</span>
            <span>${companyPercentage}%</span>
          `;

      // Append the legend item to the legend list
      legendList.appendChild(legendItem);
    });
  })
  .catch((error) => {
    console.error("Error fetching data:", error);
  });

function groupDataByCompany(data) {
  return data.reduce((result, entry) => {
    const company = entry.company_name;

    if (!result[company]) {
      result[company] = [];
    }

    result[company].push(entry);
    return result;
  }, {});
}

function getRandomColor(index) {
  const colors = [
    "rgba(255, 99, 132, 0.4)", // Lighter red
    "rgba(4, 102, 139, 1)", // Lighter blue
    "rgba(255, 206, 86, 0.4)", // Lighter yellow
    "rgba(75, 192, 192, 0.4)", // Lighter green
    "rgba(153, 102, 255, 0.4)", // Lighter purple
    "rgba(255, 159, 64, 0.4)", // Lighter orange
    "rgba(0, 255, 0, 0.4)", // Lighter lime green
    "rgba(0, 0, 255, 0.4)", // Lighter navy blue
    "rgba(128, 0, 128, 0.4)", // Lighter purple
  ];

  return colors[index % colors.length];
}
