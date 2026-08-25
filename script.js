document.addEventListener("DOMContentLoaded", () => {
  const isProductPage = window.location.pathname.includes("/products/");
  const rootPrefix = isProductPage ? "../" : "";

  function ensureBrandStyles() {
    if (document.querySelector('link[href$="brand.css"]')) return;
    const link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = `${rootPrefix}brand.css`;
    document.head.appendChild(link);
  }

  function normalizeGlobalChrome() {
    document.querySelectorAll('.nav-menu a[href$="resources.html"]').forEach((link) => {
      link.textContent = "Shop & Resources";
      link.classList.add("nav-shop");
    });

    document.querySelectorAll('.nav-menu a[href$="contact.html"]').forEach((link) => {
      link.classList.remove("nav-cta");
    });

    document.querySelectorAll('.footer-links a[href$="resources.html"]').forEach((link) => {
      link.textContent = "Shop & Resources";
    });

    document.querySelectorAll(".site-footer").forEach((footer) => {
      if (!footer.querySelector(".footer-social")) {
        const social = document.createElement("div");
        social.className = "footer-social";
        social.setAttribute("aria-label", "Social links");
        social.innerHTML = '<span>TikTok</span>';
        const copy = footer.querySelector(".footer-copy");
        footer.insertBefore(social, copy || null);
      }
    });
  }

  ensureBrandStyles();
  normalizeGlobalChrome();

  const navToggle = document.querySelector(".nav-toggle");
  const navMenu = document.querySelector(".nav-menu");
  const navLinks = document.querySelectorAll(".nav-menu a");
  const backToTopBtn = document.querySelector(".back-to-top");
  const revealElements = document.querySelectorAll(".reveal");
  const filterButtons = document.querySelectorAll(".filter-btn[data-filter]");
  const filterCards = document.querySelectorAll(".showcase-card");
  const yearSpan = document.querySelector("#year");
  const products = Array.isArray(window.CJ_STEM_PRODUCTS) ? window.CJ_STEM_PRODUCTS : [];

  if (yearSpan) yearSpan.textContent = new Date().getFullYear();

  if (navToggle && navMenu) {
    navToggle.addEventListener("click", () => {
      const isOpen = navMenu.classList.toggle("active");
      navToggle.classList.toggle("active", isOpen);
      navToggle.setAttribute("aria-expanded", String(isOpen));
      document.body.classList.toggle("nav-open", isOpen);
    });
  }

  navLinks.forEach((link) => {
    link.addEventListener("click", () => {
      if (!navMenu || !navToggle) return;
      navMenu.classList.remove("active");
      navToggle.classList.remove("active");
      navToggle.setAttribute("aria-expanded", "false");
      document.body.classList.remove("nav-open");
    });
  });

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape" || !navMenu || !navToggle) return;
    navMenu.classList.remove("active");
    navToggle.classList.remove("active");
    navToggle.setAttribute("aria-expanded", "false");
    document.body.classList.remove("nav-open");
  });

  if (backToTopBtn) {
    window.addEventListener("scroll", () => {
      backToTopBtn.classList.toggle("show", window.scrollY > 500);
    });
    backToTopBtn.addEventListener("click", () => window.scrollTo({ top: 0, behavior: "smooth" }));
  }

  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries, instance) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("visible");
        instance.unobserve(entry.target);
      });
    }, { threshold: 0.12 });
    revealElements.forEach((element) => observer.observe(element));
  } else {
    revealElements.forEach((element) => element.classList.add("visible"));
  }

  if (filterButtons.length && filterCards.length) {
    filterButtons.forEach((button) => {
      button.addEventListener("click", () => {
        const selectedFilter = button.dataset.filter;
        filterButtons.forEach((item) => item.classList.remove("active"));
        button.classList.add("active");
        filterCards.forEach((card) => {
          card.classList.toggle("hide", !(selectedFilter === "all" || selectedFilter === card.dataset.category));
        });
      });
    });
  }

  function getProductById(id) {
    return products.find((product) => product.id === id) || null;
  }

  function resolveProductPath(path) {
    return isProductPage ? `../${path}` : path;
  }

  function createProductCard(product) {
    const card = document.createElement("article");
    const accentCategory = product.categories[0] || "general";
    card.className = `product-card product-card--${accentCategory} reveal visible`;
    card.dataset.categories = product.categories.join(" ");

    const badges = product.badges.map((badge) => `<span class="product-badge">${badge}</span>`).join("");
    const price = product.price ? `<p class="product-price">${product.price}</p>` : "";

    card.innerHTML = `
      <div class="product-image-wrap">
        <img src="${resolveProductPath(product.thumbnail)}" alt="Preview of ${product.title}" loading="lazy">
        <div class="product-badges">${badges}</div>
      </div>
      <div class="product-card-body">
        <p class="product-grade">${product.gradeRange}</p>
        <h3>${product.title}</h3>
        <p>${product.description}</p>
        <p class="product-meta">${product.details} • ${product.format}</p>
        ${price}
        <a class="btn btn-product" href="${resolveProductPath(product.detailUrl)}">View Resource</a>
      </div>`;
    return card;
  }

  function renderProductGrid(container, productList) {
    if (!container) return;
    if (!productList.length) {
      container.innerHTML = '<div class="empty-product-state"><strong>Nothing here yet.</strong><p>New CJ STEM Lab resources will be added as they are released.</p></div>';
      return;
    }
    container.replaceChildren(...productList.map(createProductCard));
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

    document.querySelectorAll("[data-product-filter]").forEach((button) => {
      button.addEventListener("click", () => {
        const filter = button.dataset.productFilter;
        document.querySelectorAll("[data-product-filter]").forEach((item) => item.classList.remove("active"));
        button.classList.add("active");
        const filtered = filter === "all" ? products : products.filter((product) => product.categories.includes(filter));
        renderProductGrid(container, filtered);
      });
    });
  }

  function renderPurchaseLinks() {
    document.querySelectorAll("[data-purchase-links]").forEach((container) => {
      const product = getProductById(container.dataset.purchaseLinks);
      if (!product) return;
      const links = [];
      if (product.etsyUrl) links.push(`<a class="btn marketplace-btn marketplace-btn--etsy" href="${product.etsyUrl}" target="_blank" rel="noopener">Buy on Etsy</a>`);
      if (product.tptUrl) links.push(`<a class="btn marketplace-btn marketplace-btn--tpt" href="${product.tptUrl}" target="_blank" rel="noopener">Buy on TPT</a>`);
      container.innerHTML = links.length ? links.join("") : '<p class="purchase-note">Purchase links are being verified. This page is ready for Etsy, TPT, and future direct CJ STEM Lab checkout.</p>';
    });
  }

  renderFeaturedProducts();
  renderShopProducts();
  renderPurchaseLinks();
});
