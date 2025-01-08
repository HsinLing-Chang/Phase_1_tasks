const toggleBtn = document.querySelector(".toggle-btn");
const navBar = document.querySelector(".nav-bar");

toggleBtn.addEventListener("click", () => {
  navBar.classList.toggle("active");
  toggleBtn.classList.toggle("active");
});
