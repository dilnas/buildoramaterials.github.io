function openMob() {
  document.getElementById('mob').classList.add('open');
}

function closeMob() {
  document.getElementById('mob').classList.remove('open');
}

function doSubmit(b) {
  if (typeof fbq !== 'undefined') {
    fbq('track', 'Lead', { content_name: 'Contact Form Submission' });
  }
  b.textContent = '✓ Sent!';
  b.style.background = '#111';
  b.style.color = '#fff';
  setTimeout(() => {
    b.textContent = 'Send Inquiry →';
    b.style.background = '';
    b.style.color = '';
  }, 3000);
}

if (typeof module !== 'undefined') {
  module.exports = { openMob, closeMob, doSubmit };
}
