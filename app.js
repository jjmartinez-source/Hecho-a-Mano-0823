'use strict';

(() => {
  // All order links are real anchors, so WhatsApp also works without JavaScript.
  const WHATSAPP_NUMBER = '50489235110';
  const whatsappUrl = message => `https://wa.me/${WHATSAPP_NUMBER}?text=${encodeURIComponent(message)}`;
  let language = 'es';
  try {
    if (localStorage.getItem('hecho-language') === 'en') language = 'en';
  } catch { /* Browsing and ordering also work when storage is unavailable. */ }

  const languageButton = document.getElementById('language-button');
  const customType = document.getElementById('custom-type');
  const customIdea = document.getElementById('custom-idea');
  const customOrder = document.getElementById('custom-order');
  const dialog = document.getElementById('product-dialog');
  const catalogData = document.getElementById('catalog-data');
  const products = catalogData ? JSON.parse(catalogData.textContent) : [];
  let selectedProduct = null;
  let photoIndex = 0;

  function updateCustomOrder() {
    if (!customOrder || !customType || !customIdea) return;
    const selection = customType.selectedOptions[0].textContent;
    const idea = customIdea.value.trim();
    const intro = language === 'es'
      ? `¡Hola, Hecho a Mano! Me gustaría cotizar: ${selection}.`
      : `Hello, Hecho a Mano! I'd like a quote for: ${selection}.`;
    customOrder.href = whatsappUrl(`${intro}${idea ? `\n\n${idea}` : ''}`);
  }

  function renderDialog() {
    if (!selectedProduct || !dialog) return;
    const name = selectedProduct.name[language];
    const image = document.getElementById('dialog-image');
    const unit = selectedProduct.unit ? (language === 'es' ? ' c/u' : ' each') : '';
    document.getElementById('dialog-title').textContent = name;
    document.getElementById('dialog-price').textContent = selectedProduct.price === null
      ? (language === 'es' ? 'Cotiza tu idea' : 'Ask for a quote')
      : `L. ${selectedProduct.price.toLocaleString('en-US')}${unit}`;
    document.getElementById('dialog-description').textContent = selectedProduct.description[language];
    document.getElementById('dialog-order').href = whatsappUrl(selectedProduct.message[language]);
    image.src = selectedProduct.images[photoIndex];
    image.alt = `${name} — ${language === 'es' ? 'foto' : 'photo'} ${photoIndex + 1}`;
    document.getElementById('dialog-count').textContent = `${photoIndex + 1} / ${selectedProduct.images.length}`;
    document.getElementById('dialog-controls').hidden = selectedProduct.images.length < 2;
  }

  function applyLanguage() {
    document.documentElement.lang = language;
    document.querySelectorAll('[data-es][data-en]').forEach(element => {
      element.textContent = element.dataset[language];
    });
    document.querySelectorAll('[data-alt-es]').forEach(element => {
      element.alt = element.getAttribute(`data-alt-${language}`);
    });
    document.querySelectorAll('[data-aria-es]').forEach(element => {
      element.setAttribute('aria-label', element.getAttribute(`data-aria-${language}`));
    });
    document.querySelectorAll('[data-placeholder-es]').forEach(element => {
      element.placeholder = element.getAttribute(`data-placeholder-${language}`);
    });
    document.querySelectorAll('[data-whatsapp-es]').forEach(element => {
      element.href = whatsappUrl(element.getAttribute(`data-whatsapp-${language}`));
    });
    languageButton.querySelector('[lang="es"]').classList.toggle('chosen', language === 'es');
    languageButton.querySelector('[lang="en"]').classList.toggle('chosen', language === 'en');
    languageButton.setAttribute('aria-label', language === 'es' ? 'Switch to English' : 'Cambiar a español');
    const titles = {
      home: {es: 'Crochet con corazón', en: 'Crochet with heart'},
      tulipanes: {es: 'Tulipanes', en: 'Tulips'},
      llaveros: {es: 'Llaveros', en: 'Keychains'},
      munecas: {es: 'Muñecas', en: 'Dolls'},
      cupcakes: {es: 'Cupcakes', en: 'Cupcakes'},
    };
    const title = titles[document.body.dataset.page];
    if (title) document.title = `${title[language]} · Hecho a Mano`;
    updateCustomOrder();
    renderDialog();
  }

  languageButton.addEventListener('click', () => {
    language = language === 'es' ? 'en' : 'es';
    try { localStorage.setItem('hecho-language', language); } catch { /* Optional preference. */ }
    applyLanguage();
  });
  customType?.addEventListener('change', updateCustomOrder);
  customIdea?.addEventListener('input', updateCustomOrder);

  const menuButton = document.getElementById('menu-toggle');
  const menu = document.getElementById('main-nav');
  const closeMenu = () => {
    menu.classList.remove('open');
    menuButton.setAttribute('aria-expanded', 'false');
  };
  menuButton.addEventListener('click', () => {
    const open = menu.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(open));
  });
  menu.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') closeMenu();
  });
  document.addEventListener('click', event => {
    if (!event.target.closest('.site-header')) closeMenu();
  });
  const header = document.getElementById('site-header');
  const updateHeader = () => header.classList.toggle('scrolled', window.scrollY > 12);
  window.addEventListener('scroll', updateHeader, {passive: true});
  updateHeader();

  if (dialog) {
    document.querySelectorAll('[data-product]').forEach(button => {
      button.addEventListener('click', () => {
        selectedProduct = products.find(product => product.id === button.dataset.product);
        if (!selectedProduct) return;
        photoIndex = 0;
        renderDialog();
        dialog.showModal();
        document.body.classList.add('dialog-open');
      });
    });
    const changePhoto = delta => {
      if (!selectedProduct) return;
      photoIndex = (photoIndex + delta + selectedProduct.images.length) % selectedProduct.images.length;
      renderDialog();
    };
    document.getElementById('dialog-close').addEventListener('click', () => dialog.close());
    document.getElementById('dialog-prev').addEventListener('click', () => changePhoto(-1));
    document.getElementById('dialog-next').addEventListener('click', () => changePhoto(1));
    dialog.addEventListener('keydown', event => {
      if (event.key === 'ArrowRight' || event.key === 'ArrowLeft') {
        event.preventDefault();
        changePhoto(event.key === 'ArrowRight' ? 1 : -1);
      }
    });
    dialog.addEventListener('click', event => {
      if (event.target !== dialog) return;
      const rect = dialog.getBoundingClientRect();
      if (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom) dialog.close();
    });
    dialog.addEventListener('close', () => {
      document.body.classList.remove('dialog-open');
    });
  }

  document.getElementById('catalog-sort')?.addEventListener('change', event => {
    const grid = document.getElementById('product-grid');
    const order = event.target.value;
    const cards = [...grid.children];
    cards.sort((a, b) => {
      if (order === 'featured') return Number(a.dataset.originalOrder) - Number(b.dataset.originalOrder);
      const left = Number(a.dataset.price);
      const right = Number(b.dataset.price);
      // Unpriced reference models stay at the end in either price direction.
      if (!Number.isFinite(left)) return Number.isFinite(right) ? 1 : 0;
      if (!Number.isFinite(right)) return -1;
      return order === 'price-asc' ? left - right : right - left;
    });
    grid.append(...cards);
  });

  document.querySelectorAll('[data-year]').forEach(element => {
    element.textContent = new Date().getFullYear();
  });
  applyLanguage();

  // Enhance only after the complete page is functional. Never hide content if
  // IntersectionObserver is unavailable or the visitor prefers less motion.
  document.documentElement.classList.add('js');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('entered');
          observer.unobserve(entry.target);
        }
      });
    }, {threshold: 0.08});
    document.querySelectorAll('.reveal').forEach(element => {
      if (element.getBoundingClientRect().top > window.innerHeight) {
        observer.observe(element);
      }
    });
  }
})();
