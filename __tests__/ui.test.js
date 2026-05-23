'use strict';
const { openMob, closeMob, doSubmit } = require('../js/ui');

beforeEach(() => {
  document.body.innerHTML = '<div id="mob"></div>';
  delete global.fbq;
});

// ── openMob ────────────────────────────────────────────────────────────

describe('openMob', () => {
  test('adds "open" class to #mob', () => {
    openMob();
    expect(document.getElementById('mob').classList.contains('open')).toBe(true);
  });

  test('is idempotent when called twice', () => {
    openMob();
    openMob();
    expect(document.getElementById('mob').classList.contains('open')).toBe(true);
  });
});

// ── closeMob ───────────────────────────────────────────────────────────

describe('closeMob', () => {
  test('removes "open" class from #mob', () => {
    document.getElementById('mob').classList.add('open');
    closeMob();
    expect(document.getElementById('mob').classList.contains('open')).toBe(false);
  });

  test('is safe to call when menu is already closed', () => {
    expect(() => closeMob()).not.toThrow();
    expect(document.getElementById('mob').classList.contains('open')).toBe(false);
  });
});

describe('openMob / closeMob round-trip', () => {
  test('open then close leaves menu closed', () => {
    openMob();
    closeMob();
    expect(document.getElementById('mob').classList.contains('open')).toBe(false);
  });
});

// ── doSubmit ───────────────────────────────────────────────────────────

describe('doSubmit', () => {
  let btn;

  beforeEach(() => {
    jest.useFakeTimers();
    btn = document.createElement('button');
    btn.textContent = 'Send Inquiry →';
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  test('immediately changes button text to "✓ Sent!"', () => {
    doSubmit(btn);
    expect(btn.textContent).toBe('✓ Sent!');
  });

  test('applies non-empty background and color styles in sent state', () => {
    doSubmit(btn);
    // jsdom normalizes hex shorthand to rgb, so just assert styles are set
    expect(btn.style.background).not.toBe('');
    expect(btn.style.color).not.toBe('');
  });

  test('resets button text to original after 3000 ms', () => {
    doSubmit(btn);
    jest.advanceTimersByTime(3000);
    expect(btn.textContent).toBe('Send Inquiry →');
  });

  test('clears button inline styles after 3000 ms', () => {
    doSubmit(btn);
    jest.advanceTimersByTime(3000);
    expect(btn.style.background).toBe('');
    expect(btn.style.color).toBe('');
  });

  test('has not reset button text before 3000 ms elapses', () => {
    doSubmit(btn);
    jest.advanceTimersByTime(2999);
    expect(btn.textContent).toBe('✓ Sent!');
  });

  test('does not throw when fbq is not defined', () => {
    expect(() => doSubmit(btn)).not.toThrow();
  });

  test('calls fbq("track", "Lead", …) when fbq is defined', () => {
    const mockFbq = jest.fn();
    global.fbq = mockFbq;
    doSubmit(btn);
    expect(mockFbq).toHaveBeenCalledWith('track', 'Lead', {
      content_name: 'Contact Form Submission',
    });
  });

  test('calls fbq exactly once per submission', () => {
    const mockFbq = jest.fn();
    global.fbq = mockFbq;
    doSubmit(btn);
    expect(mockFbq).toHaveBeenCalledTimes(1);
  });
});
