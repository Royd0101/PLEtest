document.addEventListener("DOMContentLoaded", function () {
  // Function to get cookies
  function getCookies() {
    const cookies = document.cookie.split(";").reduce((acc, cookie) => {
      const [key, value] = cookie.trim().split("=");
      acc[key] = value;
      return acc;
    }, {});
    return cookies;
  }

  fetch("/api/file/expired_documents/")
    .then((response) => response.json())
    .then((data) => {
      const numberOfExpiredFile = data.length;
      const numberOfExpiredFileElement = document.getElementById("expired");
      numberOfExpiredFileElement.innerText = `${numberOfExpiredFile}`;
    });

  fetch("/api/file/valid_documents/")
    .then((response) => response.json())
    .then((data) => {
      const numberOfValidFile = data.length;
      const numberOfValidFileElement = document.getElementById("valid");
      numberOfValidFileElement.innerText = `${numberOfValidFile}`;
    });

  fetch("/api/file/renewal_documents/")
    .then((response) => response.json())
    .then((data) => {
      const numberofToRenewFile = data.length;
      const numberofToRenewFileElement = document.getElementById("renew");
      numberofToRenewFileElement.innerText = `${numberofToRenewFile}`;
    });
});
