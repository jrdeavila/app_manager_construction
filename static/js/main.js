const btnNewQuotation = document.querySelectorAll(".btn-delete");
if (btnNewQuotation) {
  const btnArray = Array.from(btnNewQuotation);
  btnArray.forEach((button) => {
    button.addEventListener("click", (e) => {
      if (!confirm("Are you sure you want delete it?")) {
        e.preventDefault();
      }
    });
  });
}

const btnDeleteService = document.getElementById("btn-delete-service");
btnDeleteService.addEventListener("click", (e) => {
  if (!confirm("Are you sure you want delete this service?")) {
    e.preventDefault();
  }
});
