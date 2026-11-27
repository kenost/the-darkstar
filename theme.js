(() => {
  const button = document.querySelector('.theme-toggle');
  if (!button) return;
  const meta = document.querySelector('meta[name="theme-color"]');
  const update = () => {
    const dark = document.documentElement.dataset.theme === 'dark';
    button.setAttribute('aria-pressed', String(dark));
    button.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
    button.innerHTML = dark ? '☀ <span>Light mode</span>' : '☾ <span>Dark mode</span>';
    if (meta) meta.content = dark ? '#111a20' : '#eee9df';
  };
  button.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme !== 'dark';
    if (dark) document.documentElement.dataset.theme = 'dark';
    else delete document.documentElement.dataset.theme;
    try { localStorage.setItem('darkstar-theme', dark ? 'dark' : 'light'); } catch (_) {}
    update();
  });
  update();
})();
