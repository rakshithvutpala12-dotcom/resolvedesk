document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('[data-confirm]').forEach(el => el.addEventListener('click', e => {
    if (!window.confirm(el.dataset.confirm || 'Are you sure?')) e.preventDefault();
  }));
});
