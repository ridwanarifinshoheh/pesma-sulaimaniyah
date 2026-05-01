document.addEventListener("DOMContentLoaded", () => {
  const slides = document.querySelectorAll(".slide");
  let currentIndex = 0;
  let autoPlayInterval;

  const setActiveSlide = (index) => {
    slides.forEach((slide, idx) => {
      slide.classList.toggle("active", idx === index);
    });
    currentIndex = index;
  };

  const nextSlide = () => {
    setActiveSlide((currentIndex + 1) % slides.length);
  };

  const startAutoPlay = () => {
    autoPlayInterval = setInterval(nextSlide, 5000);
  };

  if (slides.length) {
    setActiveSlide(0);
    startAutoPlay();
  }
});