;(async function () {
  const container = document.getElementById('projects-list');
  if (!container) return;

  const type = document.body.dataset.pageType;
  const key = document.body.dataset.pageKey;

  if (!type || !key) {
    container.textContent = 'Configuration error: projects filter is not specified.';
    return;
  }

  const baseUrl = 'https://ai-avatar-103512681014.us-central1.run.app';
  const params = new URLSearchParams();

  if (type === 'industry') {
    params.set('industry', key);
  } else if (type === 'domain') {
    params.set('domain', key);
  } else if (type === 'role') {
    params.set('role', key);
  }

  container.textContent = 'Loading projects...';

  try {
    const resp = await fetch(`${baseUrl}/api/projects?${params.toString()}`);
    if (!resp.ok) {
      throw new Error('API error: ' + resp.status);
    }

    const data = await resp.json();
    const items = data.items || [];

    if (!items.length) {
      container.textContent = 'No projects found yet.';
      return;
    }

    const list = document.createElement('div');
    list.className = 'projects-list';

    items.forEach((p) => {
      const card = document.createElement('article');
      card.className = 'project-card';

      const title = document.createElement('h3');
      title.textContent = p.title || (p.num ? `Project ${p.num}` : 'Project');
      card.appendChild(title);

      if (p.key_result) {
        const kr = document.createElement('p');
        kr.className = 'project-key-result';
        kr.textContent = p.key_result;
        card.appendChild(kr);
      }

      const metaParts = [];
      if (p.industry) metaParts.push(`Industry: ${p.industry}`);
      if (p.domain) metaParts.push(`Domain: ${p.domain}`);
      if (p.role) metaParts.push(`Role: ${p.role}`);
      if (p.year_start) {
        const end = p.year_end || '';
        metaParts.push(`Years: ${p.year_start}${end ? '–' + end : ''}`);
      }

      if (metaParts.length) {
        const meta = document.createElement('p');
        meta.className = 'project-meta';
        meta.textContent = metaParts.join(' | ');
        card.appendChild(meta);
      }

      list.appendChild(card);
    });

    container.innerHTML = '';
    container.appendChild(list);
  } catch (e) {
    console.error(e);
    container.textContent = 'Failed to load projects. Please try again later.';
  }
})();
