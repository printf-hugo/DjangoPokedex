document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('search-input');
  const btn = document.getElementById('search-btn');
  const result = document.getElementById('result');
  const favsDiv = document.getElementById('favorites');

  btn.addEventListener('click', async () => {
    const q = input.value.trim();
    if (!q) return alert('Digite nome ou ID');
    result.innerHTML = 'Carregando...';
    try {
      const res = await fetch(`/pokemon/${encodeURIComponent(q)}/`);
      if (!res.ok) {
        result.innerHTML = 'Pokémon não encontrado';
        return;
      }
      const data = await res.json();
      renderResult(data);
    } catch (e) {
      result.innerHTML = 'Erro na requisição';
      console.error(e);
    }
  });

  function renderResult(p) {
    result.innerHTML = `
      <div>
        <h3>${p.name} (#${p.id})</h3>
        <img src="${p.sprite || ''}" alt="${p.name}">
        <p>Tipos: ${p.types.join(', ')}</p>
        <p>Abilities: ${p.abilities.join(', ')}</p>
        <button id="add-fav">Adicionar aos favoritos</button>
      </div>
    `;
    document.getElementById('add-fav').addEventListener('click', async () => {
      const payload = {
        pokemon_id: p.id,
        name: p.name,
        note: '',
        tags: p.types
      };
      const r = await fetch('/api/favorites/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      if (r.ok) {
        await loadFavorites();
        alert('Adicionado aos favoritos');
      } else {
        alert('Erro ao adicionar');
      }
    });
  }

  async function loadFavorites() {
    favsDiv.innerHTML = 'Carregando favoritos...';
    const res = await fetch('/api/favorites/');
    if (!res.ok) { favsDiv.innerHTML = 'Erro'; return; }
    const data = await res.json();
    favsDiv.innerHTML = '';
    data.favorites.forEach(f => {
      const el = document.createElement('div');
      el.className = 'fav';
      el.innerHTML = `
        <strong>${f.name} (#${f.pokemon_id})</strong>
        <p>Nota: ${f.note || '-'}</p>
        <p>Tags: ${f.tags.join(', ')}</p>
        <button class="edit" data-id="${f.fav_id}">Editar</button>
        <button class="delete" data-id="${f.fav_id}">Remover</button>
      `;
      favsDiv.appendChild(el);
    });

    document.querySelectorAll('.delete').forEach(btn => {
      btn.addEventListener('click', async (ev) => {
        const id = ev.target.dataset.id;
        if (!confirm('Remover favorito?')) return;
        const r = await fetch(`/api/favorites/${id}/`, { method: 'DELETE' });
        if (r.ok) loadFavorites();
      });
    });

    document.querySelectorAll('.edit').forEach(btn => {
      btn.addEventListener('click', async (ev) => {
        const id = ev.target.dataset.id;
        const note = prompt('Nova nota:');
        const tags = prompt('Tags (vírgula separe):');
        const payload = { note: note || '', tags: tags ? tags.split(',').map(s => s.trim()) : [] };
        await fetch(`/api/favorites/${id}/`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        loadFavorites();
      });
    });
  }
  loadFavorites();
});
