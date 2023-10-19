$(document).ready(function () {
  $(".delete-button").click(function () {
    var departmentId = $(this).data("department-id");
    var confirmation = confirm("Are you sure you want to delete this user?");
    var button = $(this);

    if (confirmation) {
      $.ajax({
        type: "DELETE",
        url: "/api/file/department/" + departmentId + "/",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
        },
        success: function () {
          button.closest("tr").remove();
        },
        error: function () {
          alert("Error deleting department");
        },
      });
    }
  });

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = jQuery.trim(cookies[i]);
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
