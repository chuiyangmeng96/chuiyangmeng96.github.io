document.documentElement.classList.add('js');
const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();
const menu = document.querySelector('.menu-toggle');
const nav = document.querySelector('.site-nav');
if (menu && nav) {
  menu.hidden = false;
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('is-open', open);
  });
  nav.addEventListener('click', event => {
    if (event.target.closest('a')) {
      nav.classList.remove('is-open');
      menu.setAttribute('aria-expanded', 'false');
    }
  });
}
const dialog = document.querySelector('.figure-dialog');
let previewTrigger;
if (dialog && typeof dialog.showModal === 'function') {
  document.querySelectorAll('[data-preview]').forEach(trigger => {
    trigger.addEventListener('click', event => {
      const template = document.getElementById(`preview-${trigger.dataset.preview}`);
      if (!template) return;
      event.preventDefault();
      previewTrigger = trigger;
      dialog.querySelector('.preview-body').replaceChildren(template.content.cloneNode(true));
      dialog.showModal();
      document.body.classList.add('modal-open');
      dialog.querySelector('.close-preview').focus();
    });
  });
  dialog.querySelector('.close-preview').addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    const rect = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
  });
  dialog.addEventListener('close', () => {
    document.body.classList.remove('modal-open');
    if (previewTrigger?.isConnected) previewTrigger.focus({ preventScroll: true });
  });
}
const controls = document.querySelector('.publication-controls');
if (controls) {
  controls.hidden = false;
  const papers = [...document.querySelectorAll('#publication-list .paper')];
  const status = document.querySelector('.publication-status');
  status.hidden = false;
  let selection = 'all';
  let topic = 'all';
  function applyFilters() {
    let visible = 0;
    papers.forEach(paper => {
      const show = (selection === 'all' || paper.dataset.selected === 'true') && (topic === 'all' || paper.dataset.topic === topic);
      paper.hidden = !show;
      if (show) visible++;
      if (!show) paper.querySelectorAll('details').forEach(details => { details.open = false; });
    });
    document.querySelectorAll('.publication-year').forEach(group => {
      group.hidden = ![...group.querySelectorAll('.paper')].some(paper => !paper.hidden);
    });
    controls.querySelectorAll('[data-selection]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.selection === selection)));
    controls.querySelectorAll('[data-topic-filter]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.topicFilter === topic)));
    status.textContent = `Showing ${visible} ${selection === 'selected' ? 'selected ' : ''}${visible === 1 ? 'paper' : 'papers'}.`;
    document.querySelector('.no-results').hidden = visible !== 0;
  }
  function revealLinkedPaper() {
    let id;
    try { id = decodeURIComponent(location.hash.slice(1)); } catch { return; }
    const target = papers.find(paper => paper.id === id);
    if (!target) return;
    selection = 'all'; topic = 'all'; applyFilters();
    requestAnimationFrame(() => target.scrollIntoView({ block: 'start' }));
  }
  controls.addEventListener('click', event => {
    const button = event.target.closest('button');
    if (!button) return;
    if (button.dataset.selection) selection = button.dataset.selection;
    if (button.dataset.topicFilter) {
      topic = button.dataset.topicFilter;
      selection = 'all';
    }
    applyFilters();
  });
  document.querySelector('.reset-filters').addEventListener('click', () => { selection = 'all'; topic = 'all'; applyFilters(); });
  window.addEventListener('hashchange', revealLinkedPaper);
  applyFilters(); revealLinkedPaper();
}
document.querySelectorAll('.copy-citation').forEach(button => {
  if (!navigator.clipboard) return;
  button.hidden = false;
  button.addEventListener('click', async () => {
    try {
      await navigator.clipboard.writeText(button.parentElement.querySelector('pre').textContent);
      button.textContent = 'Copied';
      setTimeout(() => { button.textContent = 'Copy citation'; }, 1800);
    } catch { button.textContent = 'Select and copy the citation above'; }
  });
});
document.addEventListener('click', event => {
  document.querySelectorAll('.citation[open]').forEach(details => { if (!details.contains(event.target)) details.open = false; });
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') document.querySelectorAll('.citation[open]').forEach(details => { details.open = false; });
});
