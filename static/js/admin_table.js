document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/file/expired_documents/")
    .then((response) => response.json())
    .then((data) => {
      const table = $("#expired").DataTable({
        lengthMenu: [5, 10, 25, 50, 75, 100],
        searching: true,
      });

      table.clear().draw();

      data.forEach((item, index) => {
        const cells = [
          "company_name",
          "department_name",
          "document_type",
          "agency",
          "upload_file", // Assuming this is where the file URL is stored
          "renewal_date",
          "expiry_date",
          "user_fullname",
        ];

        const fileName = item.upload_file.split("/").pop(); // Extract file name

        const rowData = cells.map((key) =>
          key === "user_fullname"
            ? `${item.user_firstname} ${item.user_lastname}`
            : key === "upload_file"
            ? `<a href="${item.upload_file}" target="_blank"><i class="fas fa-file-alt" style="font-size: 30px; color: #000;"></i></a>`
            : item[key]
        );

        table.row.add([index + 1, ...rowData]).draw();
      });
    });
});

document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/file/renewal_documents/")
    .then((response) => response.json())
    .then((data) => {
      const table = $("#renew").DataTable({
        lengthMenu: [5, 10, 25, 50, 75, 100],
        searching: true,
      });

      table.clear().draw();

      data.forEach((item, index) => {
        const cells = [
          "company_name",
          "department_name",
          "document_type",
          "agency",
          "upload_file", // Assuming this is where the file URL is stored
          "renewal_date",
          "expiry_date",
          "user_fullname",
        ];

        const fileName = item.upload_file.split("/").pop(); // Extract file name

        const rowData = cells.map((key) =>
          key === "user_fullname"
            ? `${item.user_firstname} ${item.user_lastname}`
            : key === "upload_file"
            ? `<a href="${item.upload_file}" target="_blank"><i class="fas fa-file-alt" style="font-size: 30px; color: #000;"></i></a>`
            : item[key]
        );

        table.row.add([index + 1, ...rowData]).draw();
      });
    });
});

document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/file/valid_documents/")
    .then((response) => response.json())
    .then((data) => {
      const table = $("#valid").DataTable({
        lengthMenu: [5, 10, 25, 50, 75, 100],
        searching: true,
      });

      table.clear().draw();

      data.forEach((item, index) => {
        const cells = [
          "company_name",
          "department_name",
          "document_type",
          "agency",
          "upload_file", // Assuming this is where the file URL is stored
          "renewal_date",
          "expiry_date",
          "user_fullname",
        ];

        const fileName = item.upload_file.split("/").pop(); // Extract file name

        const rowData = cells.map((key) =>
          key === "user_fullname"
            ? `${item.user_firstname} ${item.user_lastname}`
            : key === "upload_file"
            ? `<a href="${item.upload_file}" target="_blank"><i class="fas fa-file-alt" style="font-size: 30px; color: #000;"></i></a>`
            : item[key]
        );

        table.row.add([index + 1, ...rowData]).draw();
      });
    });
});
