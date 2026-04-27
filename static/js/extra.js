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

// Parallax with throttling for better performance
function throttle(func, limit) {
  let inThrottle;
  return function() {
    const args = arguments;
    const context = this;
    if (!inThrottle) {
      func.apply(context, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  }
}

window.addEventListener("scroll", throttle(() => {
  const hero = document.querySelector(".hero");
  if (hero) {
    hero.style.backgroundPositionY = window.scrollY * 0.5 + "px";
  }
}, 16)); // ~60fps

// TOGGLE MENU
document.addEventListener("DOMContentLoaded", function () {

  const toggle = document.getElementById("menuToggle");
  const nav = document.getElementById("navMenu");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      nav.classList.toggle("active");
    });
  }

});

document.addEventListener("DOMContentLoaded", () => {

  const toggle = document.getElementById("themeToggle");
  const icon = toggle.querySelector(".icon");
  const body = document.body;

  // 1. Cek preferensi user
  const savedTheme = localStorage.getItem("theme");

  // 2. Auto detect OS (Apple-like)
  const prefersLight = window.matchMedia("(prefers-color-scheme: light)").matches;

  if (savedTheme === "light" || (!savedTheme && prefersLight)) {
    body.classList.add("light");
    icon.textContent = "☀️";
  } else {
    icon.textContent = "🌙";
  }

  // 3. Toggle click
  toggle.addEventListener("click", () => {
    body.classList.toggle("light");

    if (body.classList.contains("light")) {
      localStorage.setItem("theme", "light");
      icon.textContent = "☀️";
    } else {
      localStorage.setItem("theme", "dark");
      icon.textContent = "🌙";
    }
  });

});