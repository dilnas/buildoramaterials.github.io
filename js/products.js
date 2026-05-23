let searchInput, searchClear, searchCount, noResults, allCards, allSections;

function _init() {
  searchInput = document.getElementById('searchInput');
  searchClear = document.getElementById('searchClear');
  searchCount = document.getElementById('searchCount');
  noResults = document.getElementById('noResults');
  allCards = document.querySelectorAll('.item-card');
  allSections = document.querySelectorAll('.cat-section');

  allCards.forEach(card => {
    card.addEventListener('click', () => {
      const name = card.querySelector('.item-name');
      if (typeof fbq !== 'undefined' && name) {
        fbq('track', 'AddToCart', {
          content_name: name.textContent,
          content_category: 'Building Materials',
        });
      }
      const productName = name ? name.textContent : 'a building material';
      window.open(
        'https://wa.me/9710501018048?text=Hello%20Buildora%2C%20I%20would%20like%20a%20quote%20for%3A%20' +
          encodeURIComponent(productName),
        '_blank'
      );
    });
  });
}

function doSearch(q) {
  q = q.trim().toLowerCase();
  searchClear.style.display = q ? 'block' : 'none';

  if (q.length > 2 && typeof fbq !== 'undefined') {
    fbq('track', 'Search', { search_string: q });
  }

  if (!q) {
    allSections.forEach(s => s.classList.remove('hidden'));
    allCards.forEach(c => c.classList.remove('hidden'));
    searchCount.textContent = 'All Products';
    noResults.style.display = 'none';
    return;
  }

  let visibleCount = 0;
  allSections.forEach(section => {
    const cards = section.querySelectorAll('.item-card');
    let sectionVisible = 0;
    cards.forEach(card => {
      const text = (card.textContent || '').toLowerCase();
      if (text.includes(q)) {
        card.classList.remove('hidden');
        sectionVisible++;
        visibleCount++;
      } else {
        card.classList.add('hidden');
      }
    });
    if (sectionVisible > 0) {
      section.classList.remove('hidden');
    } else {
      section.classList.add('hidden');
    }
  });

  searchCount.textContent = visibleCount + ' result' + (visibleCount !== 1 ? 's' : '');
  noResults.style.display = visibleCount === 0 ? 'block' : 'none';
}

function clearSearch() {
  searchInput.value = '';
  doSearch('');
  searchInput.focus();
}

function filterCat(cat, btn) {
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');

  searchInput.value = '';
  searchClear.style.display = 'none';

  if (typeof fbq !== 'undefined' && cat !== 'all') {
    fbq('track', 'ViewContent', { content_name: cat, content_category: 'Product Filter' });
  }

  if (cat === 'all') {
    allSections.forEach(s => s.classList.remove('hidden'));
    allCards.forEach(c => c.classList.remove('hidden'));
    searchCount.textContent = 'All Products';
    noResults.style.display = 'none';
  } else {
    allSections.forEach(s => {
      if (s.dataset.cat === cat) {
        s.classList.remove('hidden');
        setTimeout(() => s.scrollIntoView({ behavior: 'smooth', block: 'start' }), 100);
      } else {
        s.classList.add('hidden');
      }
    });
    const catTitle = document.querySelector('#' + cat + ' .cat-title');
    searchCount.textContent = catTitle ? catTitle.textContent : 'Category';
    noResults.style.display = 'none';
    allCards.forEach(c => c.classList.remove('hidden'));
  }
}

function handleHashNavigation() {
  const hash = window.location.hash.replace('#', '');
  if (!hash) return;
  const btn = document.querySelector("[onclick*=\"'" + hash + "'\"]");
  if (btn) {
    filterCat(hash, btn);
  } else {
    const section = document.getElementById(hash);
    if (section) setTimeout(() => section.scrollIntoView({ behavior: 'smooth', block: 'start' }), 300);
  }
}

if (typeof module !== 'undefined') {
  module.exports = { _init, doSearch, clearSearch, filterCat, handleHashNavigation };
} else {
  _init();
  window.addEventListener('load', handleHashNavigation);
}
