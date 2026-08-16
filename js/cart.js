/*
 * Buildora Materials — Quote Cart
 * Lets visitors collect multiple products, then send one WhatsApp message
 * requesting a quote for everything at once. No prices, no payment —
 * this mirrors the existing single-product "Request a Quote" flow.
 * Self-contained: injects its own styles and DOM into every page that
 * includes this script (nav cart icon, add-to-cart buttons, drawer).
 */
(function () {
  'use strict';

  var STORAGE_KEY = 'buildoraCart';
  var WA_NUMBER = '971501018048';
  var CART_ICON_SVG =
    '<svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" ' +
    'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
    '<circle cx="9" cy="21" r="1"></circle><circle cx="20" cy="21" r="1"></circle>' +
    '<path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path></svg>';

  var cart = readCart();

  function readCart() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      var parsed = raw ? JSON.parse(raw) : [];
      return Array.isArray(parsed) ? parsed : [];
    } catch (e) {
      return [];
    }
  }

  function writeCart() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(cart));
    } catch (e) {
      /* localStorage unavailable (private mode, quota) — cart stays in-memory for this page view */
    }
  }

  function slugify(name) {
    return name
      .toLowerCase()
      .replace(/&/g, 'and')
      .replace(/[^a-z0-9]+/g, '-')
      .replace(/^-+|-+$/g, '');
  }

  function esc(s) {
    var d = document.createElement('div');
    d.textContent = s;
    return d.innerHTML;
  }

  function totalCount() {
    return cart.reduce(function (sum, i) { return sum + i.qty; }, 0);
  }

  function saveAndRender() {
    writeCart();
    renderBadge();
    renderDrawer();
  }

  window.addToCart = function (name, category) {
    name = (name || '').trim();
    if (!name) return;
    var id = slugify(name);
    var existing = cart.filter(function (i) { return i.id === id; })[0];
    if (existing) {
      existing.qty += 1;
    } else {
      cart.push({ id: id, name: name, category: category || '', qty: 1 });
    }
    saveAndRender();
    showToast(name + ' added to cart');
    if (typeof fbq !== 'undefined') {
      fbq('track', 'AddToCart', { content_name: name, content_category: category || 'Building Materials' });
    }
  };

  window.removeFromCart = function (id) {
    cart = cart.filter(function (i) { return i.id !== id; });
    saveAndRender();
  };

  window.changeCartQty = function (id, delta) {
    var item = cart.filter(function (i) { return i.id === id; })[0];
    if (!item) return;
    item.qty += delta;
    if (item.qty <= 0) {
      cart = cart.filter(function (i) { return i.id !== id; });
    }
    saveAndRender();
  };

  window.clearCart = function () {
    cart = [];
    saveAndRender();
  };

  window.openCart = function () {
    var overlay = document.getElementById('cartOverlay');
    var drawer = document.getElementById('cartDrawer');
    if (!overlay || !drawer) return;
    overlay.classList.add('open');
    drawer.classList.add('open');
    document.body.style.overflow = 'hidden';
    var mobileMenu = document.getElementById('mobile-menu');
    var hamburger = document.getElementById('hamburger-btn');
    if (mobileMenu) mobileMenu.classList.remove('open');
    if (hamburger) hamburger.classList.remove('open');
  };

  window.closeCart = function () {
    var overlay = document.getElementById('cartOverlay');
    var drawer = document.getElementById('cartDrawer');
    if (!overlay || !drawer) return;
    overlay.classList.remove('open');
    drawer.classList.remove('open');
    document.body.style.overflow = '';
  };

  window.sendCartQuote = function () {
    if (!cart.length) return;
    var lines = cart.map(function (i, idx) {
      return (idx + 1) + '. ' + i.name + ' (Qty: ' + i.qty + ')';
    });
    var msg = 'Hello Buildora, I would like a quote for the following:\n\n' + lines.join('\n');
    window.open('https://wa.me/' + WA_NUMBER + '?text=' + encodeURIComponent(msg), '_blank', 'noopener');
    if (typeof fbq !== 'undefined') {
      fbq('track', 'InitiateCheckout', { num_items: cart.length, value: totalCount(), currency: 'AED' });
    }
  };

  function renderBadge() {
    var n = totalCount();
    var badges = document.querySelectorAll('.cart-badge');
    for (var i = 0; i < badges.length; i++) {
      badges[i].textContent = String(n);
      badges[i].style.display = n > 0 ? 'flex' : 'none';
    }
  }

  function renderDrawer() {
    var body = document.getElementById('cartDrawerBody');
    var footer = document.getElementById('cartDrawerFooter');
    if (!body || !footer) return;
    if (!cart.length) {
      body.innerHTML = '<div class="cart-empty">Your cart is empty.<br>Browse products and tap the <strong>+</strong> button to add items.</div>';
      footer.style.display = 'none';
      return;
    }
    footer.style.display = 'flex';
    var html = '';
    for (var i = 0; i < cart.length; i++) {
      var item = cart[i];
      html +=
        '<div class="cart-item">' +
          '<div class="cart-item-name">' + esc(item.name) + '</div>' +
          '<div class="cart-item-qty">' +
            '<button type="button" onclick="changeCartQty(\'' + item.id + '\', -1)" aria-label="Decrease quantity">−</button>' +
            '<span>' + item.qty + '</span>' +
            '<button type="button" onclick="changeCartQty(\'' + item.id + '\', 1)" aria-label="Increase quantity">+</button>' +
          '</div>' +
          '<button type="button" class="cart-item-remove" onclick="removeFromCart(\'' + item.id + '\')" aria-label="Remove ' + esc(item.name) + '">&times;</button>' +
        '</div>';
    }
    body.innerHTML = html;
  }

  var toastTimer;
  function showToast(text) {
    var toast = document.getElementById('cartToast');
    if (!toast) return;
    toast.textContent = text;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { toast.classList.remove('show'); }, 2200);
  }

  function injectStyles() {
    if (document.getElementById('cart-inline-styles')) return;
    var css =
      '.cart-trigger-btn{position:relative;display:inline-flex;align-items:center;justify-content:center;' +
      'width:40px;height:40px;border-radius:50%;border:2px solid var(--green,#1A5C50);background:transparent;' +
      'color:var(--green,#1A5C50);cursor:pointer;flex-shrink:0;transition:background .18s,color .18s;}' +
      '.cart-trigger-btn:hover{background:var(--green,#1A5C50);color:#fff;}' +
      '.cart-trigger-btn-mobile{width:100%;border-radius:var(--radius-sm,4px);gap:8px;}' +
      '.cart-badge{position:absolute;top:-6px;right:-6px;min-width:18px;height:18px;padding:0 4px;' +
      'border-radius:9px;background:var(--orange,#F5A020);color:#fff;font-family:"Barlow Condensed",sans-serif;' +
      'font-size:11px;font-weight:700;align-items:center;justify-content:center;display:none;}' +
      '.cart-trigger-btn-mobile .cart-badge{position:static;margin-left:4px;display:inline-flex;}' +
      '.item-cart-btn{position:absolute;top:8px;right:8px;width:30px;height:30px;border-radius:50%;' +
      'border:none;background:#fff;color:var(--green,#1A5C50);box-shadow:0 2px 8px rgba(0,0,0,0.18);' +
      'font-size:18px;line-height:1;cursor:pointer;display:flex;align-items:center;justify-content:center;' +
      'z-index:2;transition:background .18s,color .18s,transform .18s;}' +
      '.item-cart-btn:hover{background:var(--orange,#F5A020);color:#fff;transform:scale(1.08);}' +
      '.item-cart-btn.added{background:var(--green,#1A5C50);color:#fff;}' +
      '.pd-cart-btn{margin-left:10px;}' +
      '.cart-overlay{position:fixed;inset:0;background:rgba(0,0,0,0.45);opacity:0;visibility:hidden;' +
      'transition:opacity .25s;z-index:100000;}' +
      '.cart-overlay.open{opacity:1;visibility:visible;}' +
      '.cart-drawer{position:fixed;top:0;right:0;height:100vh;width:min(400px,92vw);background:#fff;' +
      'box-shadow:-8px 0 32px rgba(0,0,0,0.18);transform:translateX(100%);transition:transform .3s ease;' +
      'z-index:100001;display:flex;flex-direction:column;font-family:"Inter",sans-serif;}' +
      '.cart-drawer.open{transform:translateX(0);}' +
      '.cart-drawer-header{display:flex;align-items:center;justify-content:space-between;padding:20px 22px;' +
      'border-bottom:1px solid var(--border,#e0e0e0);}' +
      '.cart-drawer-header h3{font-family:"Barlow Condensed",sans-serif;font-size:20px;font-weight:800;' +
      'color:var(--green,#1A5C50);text-transform:uppercase;letter-spacing:.03em;}' +
      '.cart-drawer-close{background:none;border:none;font-size:26px;line-height:1;color:#666;cursor:pointer;padding:4px 8px;}' +
      '.cart-drawer-close:hover{color:var(--orange,#F5A020);}' +
      '.cart-drawer-body{flex:1;overflow-y:auto;padding:10px 22px;}' +
      '.cart-empty{padding:40px 0;text-align:center;color:var(--grey-text,#666);font-size:14px;line-height:1.6;}' +
      '.cart-item{display:flex;align-items:center;gap:10px;padding:14px 0;border-bottom:1px solid var(--border,#e0e0e0);}' +
      '.cart-item-name{flex:1;font-size:14px;font-weight:600;color:#222;line-height:1.35;}' +
      '.cart-item-qty{display:flex;align-items:center;gap:8px;flex-shrink:0;}' +
      '.cart-item-qty button{width:24px;height:24px;border-radius:50%;border:1px solid var(--border,#e0e0e0);' +
      'background:#fff;cursor:pointer;font-size:14px;line-height:1;display:flex;align-items:center;justify-content:center;}' +
      '.cart-item-qty button:hover{border-color:var(--orange,#F5A020);color:var(--orange,#F5A020);}' +
      '.cart-item-qty span{min-width:16px;text-align:center;font-weight:700;font-size:14px;}' +
      '.cart-item-remove{background:none;border:none;font-size:20px;color:#bbb;cursor:pointer;flex-shrink:0;padding:2px 4px;}' +
      '.cart-item-remove:hover{color:#e53935;}' +
      '.cart-drawer-footer{display:flex;flex-direction:column;gap:10px;padding:18px 22px 22px;' +
      'border-top:1px solid var(--border,#e0e0e0);}' +
      '.cart-drawer-footer .btn{width:100%;}' +
      '.cart-toast{position:fixed;bottom:24px;left:50%;transform:translateX(-50%) translateY(20px);' +
      'background:var(--green,#1A5C50);color:#fff;padding:12px 22px;border-radius:6px;font-size:14px;' +
      'font-weight:600;box-shadow:0 6px 20px rgba(0,0,0,0.2);opacity:0;pointer-events:none;' +
      'transition:opacity .25s,transform .25s;z-index:100002;}' +
      '.cart-toast.show{opacity:1;transform:translateX(-50%) translateY(0);}';
    var style = document.createElement('style');
    style.id = 'cart-inline-styles';
    style.textContent = css;
    document.head.appendChild(style);
  }

  function buildTriggerButton(mobile) {
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = mobile ? 'btn btn-green-outline cart-trigger-btn cart-trigger-btn-mobile' : 'cart-trigger-btn';
    btn.setAttribute('aria-label', 'Open cart');
    btn.addEventListener('click', window.openCart);
    if (mobile) {
      btn.innerHTML = CART_ICON_SVG + ' View Cart <span class="cart-badge">0</span>';
    } else {
      btn.innerHTML = CART_ICON_SVG + '<span class="cart-badge">0</span>';
    }
    return btn;
  }

  function injectTriggers() {
    var navActions = document.querySelectorAll('.nav-actions');
    for (var i = 0; i < navActions.length; i++) {
      if (navActions[i].querySelector('.cart-trigger-btn')) continue;
      navActions[i].insertBefore(buildTriggerButton(false), navActions[i].firstChild);
    }
    var mobileBtns = document.querySelectorAll('.mobile-btns');
    for (var j = 0; j < mobileBtns.length; j++) {
      if (mobileBtns[j].querySelector('.cart-trigger-btn')) continue;
      mobileBtns[j].insertBefore(buildTriggerButton(true), mobileBtns[j].firstChild);
    }
  }

  function injectItemCardButtons() {
    var cards = document.querySelectorAll('.item-card');
    for (var i = 0; i < cards.length; i++) {
      var card = cards[i];
      if (card.querySelector('.item-cart-btn')) continue;
      var nameEl = card.querySelector('.item-name');
      if (!nameEl) continue;
      var name = nameEl.textContent.trim();
      if (!name) continue;
      var btn = document.createElement('button');
      btn.type = 'button';
      btn.className = 'item-cart-btn';
      btn.title = 'Add to cart';
      btn.setAttribute('aria-label', 'Add ' + name + ' to cart');
      btn.textContent = '+';
      (function (btn, name) {
        btn.addEventListener('click', function (e) {
          e.preventDefault();
          e.stopPropagation();
          window.addToCart(name);
          btn.textContent = '✓';
          btn.classList.add('added');
          setTimeout(function () {
            btn.textContent = '+';
            btn.classList.remove('added');
          }, 900);
        });
      })(btn, name);
      card.appendChild(btn);
    }
  }

  function injectPdCtaButton() {
    var pdCta = document.querySelector('.pd-cta');
    if (!pdCta || pdCta.querySelector('.pd-cart-btn')) return;
    var waBtn = pdCta.querySelector('button[onclick*="openWA"]');
    var name = '';
    if (waBtn) {
      var m = waBtn.getAttribute('onclick').match(/openWA\('([^']+)'\)/);
      if (m) name = m[1].replace(/&amp;/g, '&');
    }
    if (!name) {
      var h1 = document.querySelector('.page-h1');
      if (h1) name = h1.textContent.trim();
    }
    if (!name) return;
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'btn btn-green-outline pd-cart-btn';
    btn.textContent = '+ Add to Cart';
    btn.addEventListener('click', function () { window.addToCart(name); });
    pdCta.appendChild(btn);
  }

  function injectDrawer() {
    if (document.getElementById('cartOverlay')) return;

    var overlay = document.createElement('div');
    overlay.id = 'cartOverlay';
    overlay.className = 'cart-overlay';
    overlay.addEventListener('click', window.closeCart);
    document.body.appendChild(overlay);

    var drawer = document.createElement('div');
    drawer.id = 'cartDrawer';
    drawer.className = 'cart-drawer';
    drawer.setAttribute('role', 'dialog');
    drawer.setAttribute('aria-modal', 'true');
    drawer.setAttribute('aria-label', 'Quote cart');
    drawer.innerHTML =
      '<div class="cart-drawer-header">' +
        '<h3>Your Quote Cart</h3>' +
        '<button type="button" class="cart-drawer-close" onclick="closeCart()" aria-label="Close cart">&times;</button>' +
      '</div>' +
      '<div class="cart-drawer-body" id="cartDrawerBody"></div>' +
      '<div class="cart-drawer-footer" id="cartDrawerFooter">' +
        '<button type="button" class="btn btn-green-outline" onclick="clearCart()">Clear Cart</button>' +
        '<button type="button" class="btn btn-orange" onclick="sendCartQuote()">Send Quote Request via WhatsApp</button>' +
      '</div>';
    document.body.appendChild(drawer);

    var toast = document.createElement('div');
    toast.id = 'cartToast';
    toast.className = 'cart-toast';
    document.body.appendChild(toast);

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') window.closeCart();
    });
  }

  function init() {
    injectStyles();
    injectTriggers();
    injectItemCardButtons();
    injectPdCtaButton();
    injectDrawer();
    renderBadge();
    renderDrawer();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();

/* Register the caching service worker (see /sw.js) after the page has
   finished loading, so it never competes with the initial page load. */
if ('serviceWorker' in navigator) {
  window.addEventListener('load', function () {
    navigator.serviceWorker.register('/sw.js').catch(function () {});
  });
}
