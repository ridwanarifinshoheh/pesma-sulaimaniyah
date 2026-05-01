document.addEventListener("DOMContentLoaded", () => {

  const toggle = document.getElementById("themeToggle");
  const body = document.body;

  const updateToggleIcon = () => {
    toggle.textContent = body.classList.contains("light") ? "🌙" : "☀️";
  };

  const storedTheme = localStorage.getItem("theme");
  if (storedTheme === "light") {
    body.classList.add("light");
  } else if (storedTheme === "dark") {
    body.classList.remove("light");
  } else if (window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches) {
    body.classList.add("light");
  }

  updateToggleIcon();

  toggle.onclick = () => {
    body.classList.toggle("light");
    const theme = body.classList.contains("light") ? "light" : "dark";
    localStorage.setItem("theme", theme);
    updateToggleIcon();
  };

  const menu = document.getElementById("menuToggle");
  const nav = document.getElementById("navMenu");

  menu.onclick = () => nav.classList.toggle("active");

});