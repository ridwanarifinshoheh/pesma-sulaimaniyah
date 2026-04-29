document.addEventListener("DOMContentLoaded", () => {

  const toggle = document.getElementById("themeToggle");
  const body = document.body;

  if (localStorage.getItem("theme") === "light") {
    body.classList.add("light");
  }

  toggle.onclick = () => {
    body.classList.toggle("light");

    localStorage.setItem("theme",
      body.classList.contains("light") ? "light" : "dark"
    );
  };

  const menu = document.getElementById("menuToggle");
  const nav = document.getElementById("navMenu");

  menu.onclick = () => nav.classList.toggle("active");

});