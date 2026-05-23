// jsdom does not implement IntersectionObserver or scrollIntoView
global.IntersectionObserver = class {
  constructor() {}
  observe() {}
  unobserve() {}
  disconnect() {}
};

Element.prototype.scrollIntoView = function () {};

// Suppress jsdom navigation warnings from window.open
global.open = () => null;
