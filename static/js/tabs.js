document.addEventListener("DOMContentLoaded", function () {
  const tabButtons = document.querySelectorAll(".nav-link");

  tabButtons.forEach((button) => {
    button.addEventListener("click", function () {
      // Remove 'active' class from all tabs
      tabButtons.forEach((tabButton) => {
        tabButton.classList.remove("active");
      });

      // Add 'active' class to the clicked tab
      this.classList.add("active");

      // Hide all tab contents
      document.querySelectorAll(".tab-pane").forEach((tabContent) => {
        tabContent.classList.remove("show", "active");
      });

      // Show the corresponding tab content
      const targetContentId = this.getAttribute("href");
      const targetContent = document.querySelector(targetContentId);

      if (targetContent) {
        targetContent.classList.add("show", "active");
      }
    });
  });
});
