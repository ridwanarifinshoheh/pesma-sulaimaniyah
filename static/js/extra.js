// Preloader
window.addEventListener("load", () => {
  const preloader = document.getElementById("preloader");
  if (preloader) preloader.style.display = "none";
});

// Dark mode toggle
const toggle = document.getElementById("toggleTheme");

if (toggle) {
  toggle.onclick = () => {
    document.body.classList.toggle("light-mode");
  };
}

// Parallax
window.addEventListener("scroll", () => {
  const hero = document.querySelector(".hero");
  if (hero) {
    hero.style.backgroundPositionY = window.scrollY * 0.5 + "px";
  }
});