// Preloader
window.addEventListener("load", () => {
  document.getElementById("preloader").style.display = "none";
});

// Dark mode toggle
const toggle = document.getElementById("toggleTheme");

toggle.onclick = () => {
  document.body.classList.toggle("light-mode");
};

// Parallax effect
window.addEventListener("scroll", () => {
  document.querySelector(".hero").style.backgroundPositionY =
    window.scrollY * 0.5 + "px";
});