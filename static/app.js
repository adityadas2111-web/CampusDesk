const description = document.querySelector('#description');
description?.addEventListener('input', () => {
  document.querySelector('#counter').textContent = `${description.value.length} / 1000 characters`;
});
document.querySelectorAll('.delete-form').forEach(form => form.addEventListener('submit', event => {
  if (!confirm('Permanently delete this request?')) event.preventDefault();
}));
