document.addEventListener('DOMContentLoaded', () => {
  const SLOTS = 11;
  const loadout = Array(SLOTS).fill(null);
  let dragData = null;
  let activeCard = null;
  let ghostEl = null;

  function saveLoadout() {
    localStorage.setItem('hd2_loadout', JSON.stringify(loadout));
    fetch('/loadout', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(loadout) }).catch(() => {});
  }

  function loadSaved() {
    try {
      const saved = JSON.parse(localStorage.getItem('hd2_loadout'));
      if (saved) saved.forEach((s, i) => { if (s) loadout[i] = s; });
    } catch {}
    renderSlots();
    fetch('/loadout', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(loadout) }).catch(() => {});
  }

  function renderSlots() {
    document.querySelectorAll('.slot').forEach(slot => {
      const i = +slot.dataset.slot;
      const data = loadout[i];
      slot.innerHTML = '<span class="remove">✕</span>';
      
      const removeBtn = slot.querySelector('.remove');
      removeBtn.addEventListener('touchend', e => {
        e.preventDefault();
        e.stopPropagation();
        loadout[i] = null;
        renderSlots();
        saveLoadout();
      });

      if (data) {
        slot.classList.add('filled');
        const img = document.createElement('img');
        img.src = data.img;
        slot.appendChild(img);
      } else {
        slot.classList.remove('filled');
        const lbl = document.createElement('span');
        lbl.textContent = window._slotEmpty || 'vazio';
        slot.appendChild(lbl);
      }
    });
  }

  document.querySelectorAll('.slot').forEach(slot => {
    slot.addEventListener('click', e => {
      const i = +slot.dataset.slot;
      if (e.target.closest('.remove')) {
        loadout[i] = null;
        renderSlots();
        saveLoadout();
        return;
      }
      if (!loadout[i]) { openModal(i); return; }
      triggerStratagem(loadout[i].id, loadout[i].name, slot);
    });
  });

  async function triggerStratagem(id, name, slotEl) {
    if (slotEl) { 
      slotEl.classList.add('active-glow'); 
      setTimeout(() => slotEl.classList.remove('active-glow'), 400); 
    }
    showToast(name);
    try {
      await fetch('/stratagem/' + id, { method: 'POST' });
    } catch {}
  }

  /* --- ARRASTAR E SOLTAR (DRAG & DROP) --- */
  function createGhost(card) {
    ghostEl = card.cloneNode(true);
    ghostEl.style.cssText = 'position:fixed;opacity:0.9;pointer-events:none;z-index:999;width:65px;height:65px;background:#161c27;border:2px solid #ffe800;padding:6px;display:flex;flex-direction:column;align-items:center;clip-path:polygon(0 0, 88% 0, 100% 12%, 100% 100%, 0 100%);box-shadow:0 0 15px rgba(255,232,0,0.5);';
    ghostEl.querySelector('img').style.cssText = 'width:80%;height:80%;object-fit:contain;';
    const label = ghostEl.querySelector('span');
    if (label) label.remove();
    document.body.appendChild(ghostEl);
  }

  function moveGhost(x, y) {
    if (!ghostEl) return;
    ghostEl.style.left = (x - 32) + 'px';
    ghostEl.style.top = (y - 32) + 'px';
  }

  function removeGhost() {
    if (ghostEl) { ghostEl.remove(); ghostEl = null; }
  }

  function slotAtPoint(x, y) {
    const els = document.elementsFromPoint(x, y);
    return els.find(e => e.classList.contains('slot')) || null;
  }

  function startDrag(card, x, y) {
    activeCard = card;
    dragData = { id: card.dataset.id, name: card.dataset.name, img: card.querySelector('img').src };
    card.classList.add('dragging');
    createGhost(card);
    moveGhost(x, y);
  }

  function moveDrag(x, y) {
    if (!dragData) return;
    moveGhost(x, y);
    document.querySelectorAll('.slot').forEach(s => s.classList.remove('drag-over'));
    const target = slotAtPoint(x, y);
    if (target) target.classList.add('drag-over');
  }

  function endDrag(x, y) {
    if (!dragData) return;
    const target = slotAtPoint(x, y);
    if (target) {
      loadout[+target.dataset.slot] = dragData;
      renderSlots();
      saveLoadout();
    }
    document.querySelectorAll('.slot').forEach(s => s.classList.remove('drag-over'));
    if (activeCard) activeCard.classList.remove('dragging');
    removeGhost();
    dragData = null;
    activeCard = null;
  }

  function initCardEvents(card) {
    let longPressTimer = null;
    let touchMoved = false;

    card.addEventListener('mousedown', e => {
      if (e.button !== 0) return;
      e.preventDefault();
      startDrag(card, e.clientX, e.clientY);
    });

    card.addEventListener('touchstart', e => {
      touchMoved = false;
      const touch = e.touches[0];
      longPressTimer = setTimeout(() => {
        if (!touchMoved) {
          startDrag(card, touch.clientX, touch.clientY);
          if (navigator.vibrate) navigator.vibrate(40);
        }
      }, 350);
    }, { passive: true });

    card.addEventListener('touchmove', e => {
      if (!dragData) {
        touchMoved = true;
        clearTimeout(longPressTimer);
        return;
      }
      e.preventDefault();
      const touch = e.touches[0];
      moveDrag(touch.clientX, touch.clientY);
    }, { passive: false });

    card.addEventListener('touchend', e => {
      clearTimeout(longPressTimer);
      if (!dragData) return;
      const touch = e.changedTouches[0];
      endDrag(touch.clientX, touch.clientY);
    });

    card.addEventListener('touchcancel', () => {
      clearTimeout(longPressTimer);
      if (dragData) endDrag(-1, -1);
    });
  }

  document.querySelectorAll('main .card').forEach(initCardEvents);

  document.addEventListener('mousemove', e => {
    if (!dragData) return;
    moveDrag(e.clientX, e.clientY);
  });

  document.addEventListener('mouseup', e => {
    if (!dragData) return;
    endDrag(e.clientX, e.clientY);
  });

  let toastTimer;
  function showToast(msg) {
    const t = document.getElementById('toast');
    t.textContent = msg;
    t.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => t.classList.remove('show'), 1500);
  }

  /* --- TRADUÇÃO E SERVIDOR --- */
  async function applyLang() {
    try {
      const res = await fetch('/lang', { cache: 'no-store' });
      const t = await res.json();

      document.querySelector('header p').textContent = t.tagline;
      document.querySelector('.loadout-label').textContent = t.loadout_label;
      document.getElementById('modal-input').placeholder = t.search_placeholder;
      document.getElementById('modal-close').textContent = t.modal_cancel;
      document.getElementById('offline-screen').querySelector('h2').textContent = t.offline_title;
      document.getElementById('offline-screen').querySelector('p').innerHTML = t.offline_body.replace('\n', '<br>');
      document.getElementById('offline-retry').textContent = t.offline_retry;
      document.querySelector('footer').innerHTML = t.footer;

      const sectionKeys = [
        'section_eagle', 'section_orbital', 'section_sentries', 'section_defense',
        'section_weapons', 'section_backpacks', 'section_exo', 'section_essentials', 'section_mission'
      ];
      document.querySelectorAll('.section-title').forEach((el, i) => {
        if (sectionKeys[i]) el.childNodes[0].textContent = t[sectionKeys[i]];
      });

      document.querySelectorAll('.slot:not(.filled) span:last-child').forEach(el => {
        el.textContent = t.slot_empty;
      });
      window._slotEmpty = t.slot_empty;
    } catch {}
  }

  async function checkServer() {
    try {
      const res = await fetch('/ping', { method: 'GET', cache: 'no-store' });
      if (!res.ok) throw new Error();
      document.getElementById('offline-screen').classList.remove('show');
    } catch {
      document.getElementById('offline-screen').classList.add('show');
    }
  }

  /* --- BUSCA NO MODAL --- */
  let targetSlot = null;
  const overlay = document.getElementById('modal-overlay');
  const modalInput = document.getElementById('modal-input');
  const modalResults = document.getElementById('modal-results');

  document.querySelectorAll('main .card').forEach(card => {
    const clone = card.cloneNode(true);
    clone.addEventListener('click', () => {
      if (targetSlot === null) return;
      loadout[targetSlot] = { id: card.dataset.id, name: card.dataset.name, img: card.querySelector('img').src };
      renderSlots();
      saveLoadout();
      closeModal();
    });
    modalResults.appendChild(clone);
  });

  function openModal(i) {
    targetSlot = i;
    modalInput.value = '';
    modalResults.querySelectorAll('.card').forEach(c => c.style.display = '');
    overlay.classList.add('open');
    setTimeout(() => modalInput.focus(), 100);
  }

  function closeModal() {
    overlay.classList.remove('open');
    targetSlot = null;
  }

  modalInput.addEventListener('input', function() {
    const q = this.value.trim().toLowerCase();
    modalResults.querySelectorAll('.card').forEach(c => {
      c.style.display = (!q || c.dataset.name.toLowerCase().includes(q)) ? '' : 'none';
    });
  });

  document.getElementById('modal-close').addEventListener('click', closeModal);
  overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(); });
  document.getElementById('offline-retry').addEventListener('click', checkServer);

  // Inicializações
  loadSaved();
  applyLang();
  checkServer();
});