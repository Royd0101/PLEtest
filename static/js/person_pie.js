const personPieCanvas = document.querySelector("#person_pie");
const chartTitleElement = document.querySelector("#chartTitle");
const chartYearElement = document.querySelector("#chartYear");

fetch("/api/receipts/person_receipt/")
  .then((response) => response.json())
  .then((data) => {
    console.log("Fetched data:", data);

    const currentYear = new Date().getFullYear();

    const currentYearData = data.filter((entry) => {
      const entryYear = new Date(entry.timestamp).getFullYear();
      return entryYear === currentYear;
    });

    const groupedData = groupDataByCompany(currentYearData);

    const companyLabels = Object.keys(groupedData).sort();

    const totalFines = companyLabels.map((company) =>
      groupedData[company].reduce((sum, entry) => {
        return sum + parseFloat(entry.fined);
      }, 0)
    );

    console.log(totalFines);
    const totalFine = totalFines.reduce((sum, amount) => sum + amount, 0);

    companyLabels.forEach((company, index) => {
      const companyPercentage = ((totalFines[index] / totalFine) * 100).toFixed(
        2
      );
    });

    const companyColors = {};
    companyLabels.forEach((company, index) => {
      companyColors[company] = getRandomColor(index);
    });

    const myPieChart = new Chart(personPieCanvas, {
      type: "doughnut",
      data: {
        labels: companyLabels,
        datasets: [
          {
            data: totalFines,
            backgroundColor: companyLabels.map(
              (company) => companyColors[company]
            ),
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
                const companyIndex = companyLabels.indexOf(label);
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
              const companyIndex = companyLabels.indexOf(
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

    companyLabels.forEach((company, index) => {
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
