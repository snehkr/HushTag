document.addEventListener("DOMContentLoaded", function () {
  // Flash message auto-dismiss
  const flashMessages = document.querySelectorAll(".alert");
  flashMessages.forEach((msg) => {
    setTimeout(() => {
      msg.style.transition = "opacity 0.5s";
      msg.style.opacity = "0";
      setTimeout(() => msg.remove(), 500);
    }, 5000);
  });

  // File input labels
  const fileInputs = document.querySelectorAll('input[type="file"]');
  fileInputs.forEach((input) => {
    const label = document.createElement("span");
    label.className = "file-label";
    label.textContent = "Choose file...";
    input.insertAdjacentElement("afterend", label);

    input.addEventListener("change", function () {
      if (this.files.length > 0) {
        label.textContent = this.files[0].name;
      } else {
        label.textContent = "Choose file...";
      }
    });
  });
});
