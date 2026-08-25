document.addEventListener("DOMContentLoaded", () => {
  const navToggle = document.querySelector(".nav-toggle");
  const navMenu = document.querySelector(".nav-menu");
  const backToTopBtn = document.querySelector(".back-to-top");
  const revealElements = document.querySelectorAll(".reveal");
  const filterButtons = document.querySelectorAll(".filter-btn[data-filter]");
  const filterCards = document.querySelectorAll(".showcase-card");
  const yearSpan = document.querySelector("#year");
  const products = Array.isArray(window.CJ_STEM_PRODUCTS)
    ? window.CJ_STEM_PRODUCTS
    : [];

  function normalizeSharedNavigation() {
    document.querySelectorAll('a[href$="resources.html"]').forEach((link) => {
      link.textContent = "Shop & Resources";
      if (link.closest(".nav-menu")) {
        link.classList.add("nav-shop");
      }
    });

    document.querySelectorAll(".nav-menu .nav-cta").forEach((link) => {
      if (!link.href.endsWith("resources.html")) {
        link.classList.remove("nav-cta");
      }
    });

    document.querySelectorAll(".site-footer").forEach((footer) => {
      if (footer.querySelector(".footer-social")) return;
      const social = document.createElement("div");
      social.className = "footer-social";
      social.setAttribute("aria-label", "Social links");
      social.innerHTML = "<span>TikTok</span>";
      const copy = footer.querySelector(".footer-copy");
      footer.insertBefore(social, copy || null);
    });
  }

  function getProductById(id) {
    return products.find((product) => product.id === id) || null;
  }

  function createProductCard(product) {
    const card = document.createElement("article");
    card.className = `product-card product-card--${product.categories[0] || "general"}`;
    card.dataset.categories = product.categories.join(" ");

    const badges = product.badges
      .map((badge) => `<span class="product-badge">${badge}</span>`)
      .join("");

    const price = product.price
      ? `<p class="product-price">${product.price}</p>`
      : "";

    card.innerHTML = `
      <div class="product-image-wrap">
        <img src="${product.thumbnail}" alt="Preview of ${product.title}" loading="lazy">
        <div class="product-badges">${badges}</div>
      </div>
      <div class="product-card-body">
        <p class="product-grade">${product.gradeRange}</p>
        <h3>${product.title}</h3>
        <p>${product.description}</p>
        <p class="product-meta">${product.details} • ${product.format}</p>
        ${price}
        <a class="btn btn-product" href="${product.detailUrl}">View Resource</a>
      </div>
    `;

    return card;
  }

  function renderProductGrid(container, productList) {
    if (!container) return;
    container.replaceChildren(...productList.map(createProductCard));

    if (!productList.length) {
      const emptyState = document.createElement("p");
      emptyState.className = "product-empty-state";
      emptyState.textContent = "Nothing in this category yet — more CJ STEM Lab resources are on the way.";
      container.append(emptyState);
    }
  }

  function renderFeaturedProducts() {
    const container = document.querySelector('[data-product-grid="featured"]');
    if (!container) return;
    renderProductGrid(container, products.filter((product) => product.featured));
  }

  function renderShopProducts() {
    const container = document.querySelector('[data-product-grid="shop"]');
    if (!container) return;

    renderProductGrid(container, products);

    const buttons = document.querySelectorAll("[data-product-filter]");
    buttons.forEach((button) => {
      button.addEventListener("click", () => {
        const filter = button.dataset.productFilter;
        buttons.forEach((item) => item.classList.remove("active"));
        button.classList.add("active");

        const filtered = filter === "all"
          ? products
          : products.filter((product) => product.categories.includes(filter));

        renderProductGrid(container, filtered);
      });
    });
  }

  function renderPurchaseLinks() {
    document.querySelectorAll("[data-purchase-links]").forEach((container) => {
      const product = getProductById(container.dataset.purchaseLinks);
      if (!product) return;

      const links = [
        product.etsyUrl
          ? `<a class="btn marketplace-btn marketplace-btn--etsy" href="${product.etsyUrl}" target="_blank" rel="noopener">Buy on Etsy</a>`
          : "",
        product.tptUrl
          ? `<a class="btn marketplace-btn marketplace-btn--tpt" href="${product.tptUrl}" target="_blank" rel="noopener">Buy on TPT</a>`
          : ""
      ].filter(Boolean);

      container.innerHTML = links.length
        ? links.join("")
        : '<p class="purchase-note">Marketplace purchase links are being verified.</p>';
    });
  }

  normalizeSharedNavigation();

  if (yearSpan) {
    yearSpan.textContent = new Date().getFullYear();
  }

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", () => {
      const isOpen = navMenu.classList.toggle("active");
      navToggle.classList.toggle("active", isOpen);
      navToggle.setAttribute("aria-expanded", String(isOpen));
      document.body.classList.toggle("nav-open", isOpen);
    });
  }

  document.querySelectorAll(".nav-menu a").forEach((link) => {
    link.addEventListener("click", () => {
      if (!navMenu || !navToggle) return;
      navMenu.classList.remove("active");
      navToggle.classList.remove("active");
      navToggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("nav-open");
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    if (!navMenu || !navToggle) return;
    navMenu.classList.remove("active");
    navToggle.classList.remove("active");
    navToggle.setAttribute("aria-expanded", "false");
    document.body.classList.remove("nav-open");
  });

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

  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach((entry) => {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        });
      },
      { threshold: 0.12 }
    );

    revealElements.forEach((element) => {
      revealObserver.observe(element);
    });
  } else {
    revealElements.forEach((element) => {
      element.classList.add("visible");
    });
  }

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

  renderFeaturedProducts();
  renderShopProducts();
  renderPurchaseLinks();
});
