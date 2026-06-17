document.addEventListener("DOMContentLoaded", () => {
  const navToggle = document.querySelector(".nav-toggle");
  const navMenu = document.querySelector(".nav-menu");
  const navLinks = document.querySelectorAll(".nav-menu a");
  const backToTopBtn = document.querySelector(".back-to-top");
  const revealElements = document.querySelectorAll(".reveal");
  const filterButtons = document.querySelectorAll(".filter-btn");
  const filterCards = document.querySelectorAll(".showcase-card");
  const yearSpan = document.querySelector("#year");

  // Set current year in footer
  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  // Mobile navigation toggle
  if (navToggle && navMenu) {
    navToggle.addEventListener("click", () => {
      const isOpen = navMenu.classList.toggle("active");

      navToggle.classList.toggle("active", isOpen);
      navToggle.setAttribute("aria-expanded", String(isOpen));
      document.body.classList.toggle("nav-open", isOpen);
    });
  }

  // Close mobile nav after clicking a nav link
  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      if (!navMenu || !navToggle) return;

      navMenu.classList.remove("active");
      navToggle.classList.remove("active");
      navToggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("nav-open");
    });
  });

  // Close mobile nav with Escape key
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    if (!navMenu || !navToggle) return;

    navMenu.classList.remove("active");
    navToggle.classList.remove("active");
    navToggle.setAttribute("aria-expanded", "false");
    document.body.classList.remove("nav-open");
  });

  // Back to top button
  if (backToTopBtn) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 500) {
        backToTopBtn.classList.add("show");
      } else {
        backToTopBtn.classList.remove("show");
      }
    });

    backToTopBtn.addEventListener("click", () => {
      window.scrollTo({
        top: 0,
        behavior: "smooth"
      });
    });
  }

  // Scroll reveal animation
  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;

          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        });
      },
      {
        threshold: 0.12
      }
    );

    revealElements.forEach((element) => {
      revealObserver.observe(element);
    });
  } else {
    revealElements.forEach((element) => {
      element.classList.add("visible");
    });
  }

  // Filter buttons for Student Zone and Resource Library
  if (filterButtons.length && filterCards.length) {
    filterButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const selectedFilter = button.dataset.filter;

        filterButtons.forEach((btn) => btn.classList.remove("active"));
        button.classList.add("active");

        filterCards.forEach((card) => {
          const cardCategory = card.dataset.category;

          if (selectedFilter === "all" || selectedFilter === cardCategory) {
            card.classList.remove("hide");
          } else {
            card.classList.add("hide");
          }
        });
      });
    });
  }
});
