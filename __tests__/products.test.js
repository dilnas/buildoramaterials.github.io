'use strict';
const { _init, doSearch, clearSearch, filterCat, handleHashNavigation } = require('../js/products');

function buildDOM() {
  document.body.innerHTML = `
    <input id="searchInput" type="text" />
    <button id="searchClear" style="display:none">Clear</button>
    <div id="searchCount">All Products</div>
    <div id="noResults" style="display:none"></div>

    <button class="filter-btn active" onclick="filterCat('all',this)">All</button>
    <button class="filter-btn" onclick="filterCat('electrical',this)">Electrical</button>
    <button class="filter-btn" onclick="filterCat('cables',this)">Cables</button>

    <div class="cat-section" id="electrical" data-cat="electrical">
      <div class="cat-title">ELECTRICAL</div>
      <div class="items-grid">
        <div class="item-card"><div class="item-name">Circuit Breaker</div><div class="item-detail">MCB for panels</div></div>
        <div class="item-card"><div class="item-name">Isolator Switch</div><div class="item-detail">Load break isolator</div></div>
      </div>
    </div>

    <div class="cat-section" id="cables" data-cat="cables">
      <div class="cat-title">CABLES</div>
      <div class="items-grid">
        <div class="item-card"><div class="item-name">XLPE Cable</div><div class="item-detail">Power cables</div></div>
        <div class="item-card"><div class="item-name">Fire Resistant Cable</div><div class="item-detail">LS0H cable</div></div>
      </div>
    </div>
  `;
  _init();
}

beforeEach(() => {
  buildDOM();
  delete global.fbq;
  jest.useFakeTimers();
});

afterEach(() => {
  jest.useRealTimers();
});

// ── doSearch — empty query ─────────────────────────────────────────────

describe('doSearch — empty query', () => {
  test('shows all sections', () => {
    doSearch('');
    document.querySelectorAll('.cat-section').forEach(s => {
      expect(s.classList.contains('hidden')).toBe(false);
    });
  });

  test('shows all cards', () => {
    doSearch('');
    document.querySelectorAll('.item-card').forEach(c => {
      expect(c.classList.contains('hidden')).toBe(false);
    });
  });

  test('sets count text to "All Products"', () => {
    doSearch('');
    expect(document.getElementById('searchCount').textContent).toBe('All Products');
  });

  test('hides the noResults element', () => {
    doSearch('');
    expect(document.getElementById('noResults').style.display).toBe('none');
  });

  test('hides the clear button', () => {
    doSearch('');
    expect(document.getElementById('searchClear').style.display).toBe('none');
  });
});

// ── doSearch — matching logic ──────────────────────────────────────────

describe('doSearch — with query', () => {
  test('shows the clear button when query is non-empty', () => {
    doSearch('cable');
    expect(document.getElementById('searchClear').style.display).toBe('block');
  });

  test('matching is case-insensitive (uppercase query)', () => {
    doSearch('XLPE');
    const xlpeCard = [...document.querySelectorAll('.item-card')].find(c =>
      c.textContent.includes('XLPE')
    );
    expect(xlpeCard.classList.contains('hidden')).toBe(false);
  });

  test('hides cards whose text does not contain the query', () => {
    doSearch('xlpe');
    const isolatorCard = [...document.querySelectorAll('.item-card')].find(c =>
      c.textContent.includes('Isolator')
    );
    expect(isolatorCard.classList.contains('hidden')).toBe(true);
  });

  test('hides an entire section when none of its cards match', () => {
    doSearch('xlpe');
    expect(document.getElementById('electrical').classList.contains('hidden')).toBe(true);
  });

  test('keeps a section visible when at least one of its cards matches', () => {
    doSearch('xlpe');
    expect(document.getElementById('cables').classList.contains('hidden')).toBe(false);
  });

  test('shows "1 result" (singular) for exactly one match', () => {
    doSearch('xlpe');
    expect(document.getElementById('searchCount').textContent).toBe('1 result');
  });

  test('shows "0 results" (plural) when no cards match', () => {
    doSearch('zzznomatch');
    expect(document.getElementById('searchCount').textContent).toBe('0 results');
  });

  test('shows "N results" (plural) for two or more matches', () => {
    doSearch('cable');
    expect(document.getElementById('searchCount').textContent).toMatch(/^[2-9]\d* results$/);
  });

  test('shows noResults element when no cards match', () => {
    doSearch('zzznomatch');
    expect(document.getElementById('noResults').style.display).toBe('block');
  });

  test('hides noResults element when at least one card matches', () => {
    doSearch('cable');
    expect(document.getElementById('noResults').style.display).toBe('none');
  });
});

// ── doSearch — Meta Pixel tracking ────────────────────────────────────

describe('doSearch — Meta Pixel', () => {
  test('does not call fbq when query length is exactly 2 (boundary)', () => {
    const mockFbq = jest.fn();
    global.fbq = mockFbq;
    doSearch('ab');
    expect(mockFbq).not.toHaveBeenCalledWith('track', 'Search', expect.anything());
  });

  test('calls fbq Search event when query length is 3 or more', () => {
    const mockFbq = jest.fn();
    global.fbq = mockFbq;
    doSearch('cable');
    expect(mockFbq).toHaveBeenCalledWith('track', 'Search', { search_string: 'cable' });
  });

  test('passes the lowercased query to fbq', () => {
    const mockFbq = jest.fn();
    global.fbq = mockFbq;
    doSearch('XLPE');
    expect(mockFbq).toHaveBeenCalledWith('track', 'Search', { search_string: 'xlpe' });
  });

  test('does not throw when fbq is undefined', () => {
    expect(() => doSearch('cable')).not.toThrow();
  });
});

// ── clearSearch ────────────────────────────────────────────────────────

describe('clearSearch', () => {
  beforeEach(() => {
    doSearch('xlpe');
  });

  test('resets the search input value to empty string', () => {
    document.getElementById('searchInput').value = 'xlpe';
    clearSearch();
    expect(document.getElementById('searchInput').value).toBe('');
  });

  test('makes all sections visible again', () => {
    clearSearch();
    document.querySelectorAll('.cat-section').forEach(s => {
      expect(s.classList.contains('hidden')).toBe(false);
    });
  });

  test('makes all cards visible again', () => {
    clearSearch();
    document.querySelectorAll('.item-card').forEach(c => {
      expect(c.classList.contains('hidden')).toBe(false);
    });
  });

  test('resets count text to "All Products"', () => {
    clearSearch();
    expect(document.getElementById('searchCount').textContent).toBe('All Products');
  });

  test('hides the clear button', () => {
    clearSearch();
    expect(document.getElementById('searchClear').style.display).toBe('none');
  });
});

// ── filterCat — "all" ─────────────────────────────────────────────────

describe('filterCat("all")', () => {
  let allBtn;

  beforeEach(() => {
    allBtn = document.querySelector('.filter-btn');
    // Pre-hide everything so we can verify the reset
    doSearch('xlpe');
    filterCat('all', allBtn);
  });

  test('shows all sections', () => {
    document.querySelectorAll('.cat-section').forEach(s => {
      expect(s.classList.contains('hidden')).toBe(false);
    });
  });

  test('shows all cards', () => {
    document.querySelectorAll('.item-card').forEach(c => {
      expect(c.classList.contains('hidden')).toBe(false);
    });
  });

  test('sets count text to "All Products"', () => {
    expect(document.getElementById('searchCount').textContent).toBe('All Products');
  });

  test('hides the noResults element', () => {
    expect(document.getElementById('noResults').style.display).toBe('none');
  });

  test('clears the search input value', () => {
    document.getElementById('searchInput').value = 'something';
    filterCat('all', allBtn);
    expect(document.getElementById('searchInput').value).toBe('');
  });

  test('sets the active class on the "all" button', () => {
    expect(allBtn.classList.contains('active')).toBe(true);
  });

  test('does not call fbq for "all" category', () => {
    const mockFbq = jest.fn();
    global.fbq = mockFbq;
    filterCat('all', allBtn);
    expect(mockFbq).not.toHaveBeenCalledWith('track', 'ViewContent', expect.anything());
  });
});

// ── filterCat — specific category ─────────────────────────────────────

describe('filterCat(specific category)', () => {
  let cablesBtn;

  beforeEach(() => {
    cablesBtn = document.querySelectorAll('.filter-btn')[2];
    filterCat('cables', cablesBtn);
  });

  test('shows only the matching section', () => {
    expect(document.getElementById('cables').classList.contains('hidden')).toBe(false);
  });

  test('hides non-matching sections', () => {
    expect(document.getElementById('electrical').classList.contains('hidden')).toBe(true);
  });

  test('sets the active class on the clicked button', () => {
    expect(cablesBtn.classList.contains('active')).toBe(true);
  });

  test('removes the active class from all other buttons', () => {
    document.querySelectorAll('.filter-btn').forEach(b => {
      if (b !== cablesBtn) {
        expect(b.classList.contains('active')).toBe(false);
      }
    });
  });

  test('clears the search input value', () => {
    document.getElementById('searchInput').value = 'xlpe';
    filterCat('cables', cablesBtn);
    expect(document.getElementById('searchInput').value).toBe('');
  });

  test('sets count text to the matched category title', () => {
    expect(document.getElementById('searchCount').textContent).toBe('CABLES');
  });

  test('hides the noResults element', () => {
    expect(document.getElementById('noResults').style.display).toBe('none');
  });

  test('restores all cards in the matched section even if previously hidden by search', () => {
    // First, hide a card via search
    doSearch('xlpe');
    // Fire Resistant Cable is now hidden
    const fireCard = [...document.querySelectorAll('#cables .item-card')].find(c =>
      c.textContent.includes('Fire Resistant')
    );
    expect(fireCard.classList.contains('hidden')).toBe(true);

    // filterCat should un-hide it
    filterCat('cables', cablesBtn);
    expect(fireCard.classList.contains('hidden')).toBe(false);
  });

  test('falls back count text to "Category" when cat-title element is absent', () => {
    document.querySelector('#cables .cat-title').remove();
    filterCat('cables', cablesBtn);
    expect(document.getElementById('searchCount').textContent).toBe('Category');
  });
});

// ── filterCat — Meta Pixel ─────────────────────────────────────────────

describe('filterCat — Meta Pixel', () => {
  test('calls fbq ViewContent for a specific category', () => {
    const mockFbq = jest.fn();
    global.fbq = mockFbq;
    filterCat('cables', document.querySelectorAll('.filter-btn')[2]);
    expect(mockFbq).toHaveBeenCalledWith('track', 'ViewContent', {
      content_name: 'cables',
      content_category: 'Product Filter',
    });
  });

  test('does not throw when fbq is undefined', () => {
    expect(() =>
      filterCat('cables', document.querySelectorAll('.filter-btn')[2])
    ).not.toThrow();
  });
});

// ── handleHashNavigation ───────────────────────────────────────────────

describe('handleHashNavigation', () => {
  beforeEach(() => {
    delete window.location;
    window.location = { hash: '' };
  });

  test('does nothing and does not throw when hash is empty', () => {
    window.location.hash = '';
    expect(() => handleHashNavigation()).not.toThrow();
  });

  test('activates the matching filter button when hash is a known category', () => {
    window.location.hash = '#cables';
    handleHashNavigation();
    const cablesBtn = document.querySelectorAll('.filter-btn')[2];
    expect(cablesBtn.classList.contains('active')).toBe(true);
  });

  test('hides non-matching sections when navigating via hash', () => {
    window.location.hash = '#cables';
    handleHashNavigation();
    expect(document.getElementById('electrical').classList.contains('hidden')).toBe(true);
  });

  test('scrolls to a section when the hash has no matching filter button', () => {
    const extra = document.createElement('div');
    extra.id = 'earthing';
    const spy = jest.fn();
    extra.scrollIntoView = spy;
    document.body.appendChild(extra);

    window.location.hash = '#earthing';
    handleHashNavigation();
    jest.advanceTimersByTime(300);
    expect(spy).toHaveBeenCalled();
  });

  test('does not throw for an unknown hash with no matching element', () => {
    window.location.hash = '#doesnotexist';
    expect(() => handleHashNavigation()).not.toThrow();
  });
});
