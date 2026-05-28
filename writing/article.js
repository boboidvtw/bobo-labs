/* Bobo Labs — article enhancement layer.
   Provides: auto TOC from h2/h3, scroll-spy active highlight, reading progress bar.
   Zero dependency. Activates only when <main class="article--enhanced"> is present.
*/
(function () {
  'use strict';

  const main = document.querySelector('.article--enhanced');
  if (!main) return;

  const article = main.querySelector('.article-wrap');
  if (!article) return;

  // ----------------------------------------------------------------
  // 1. Slugify (Chinese-safe): keep Chinese chars, strip punctuation
  // ----------------------------------------------------------------
  function slugify(text) {
    return text
      .trim()
      .replace(/[\s　]+/g, '-')
      .replace(/[，。、；：「」『』（）()！？!?,.;:'"#]/g, '')
      .toLowerCase();
  }

  // ----------------------------------------------------------------
  // 2. Assign id + anchor link to every h2/h3 (skip if already has)
  // ----------------------------------------------------------------
  const body = article.querySelector('.article-body');
  const headings = body
    ? body.querySelectorAll('h2, h3')
    : article.querySelectorAll('.article-body h2, .article-body h3');

  const tocItems = [];
  const usedIds = new Set();

  headings.forEach((h) => {
    let id = h.id;
    if (!id) {
      const base = slugify(h.textContent || '');
      id = base;
      let i = 2;
      while (usedIds.has(id) || document.getElementById(id)) {
        id = `${base}-${i++}`;
      }
      h.id = id;
    }
    usedIds.add(id);

    // anchor link (# on hover)
    if (!h.querySelector('.anchor-link')) {
      const a = document.createElement('a');
      a.className = 'anchor-link';
      a.href = `#${id}`;
      a.setAttribute('aria-label', 'Permalink to section');
      a.textContent = '#';
      h.insertBefore(a, h.firstChild);
    }

    tocItems.push({ id, text: (h.textContent || '').replace(/^#\s*/, ''), level: h.tagName });
  });

  // ----------------------------------------------------------------
  // 3. Build TOC
  // ----------------------------------------------------------------
  const tocAside = article.querySelector('.article-toc');
  if (tocAside && tocItems.length > 0) {
    const tocList = document.createElement('ul');
    tocList.className = 'article-toc-list';

    tocItems.forEach((item) => {
      const li = document.createElement('li');
      if (item.level === 'H3') li.style.paddingLeft = '0.85rem';
      const a = document.createElement('a');
      a.href = `#${item.id}`;
      a.textContent = item.text;
      a.dataset.tocTarget = item.id;
      li.appendChild(a);
      tocList.appendChild(li);
    });

    tocAside.appendChild(tocList);
  }

  // ----------------------------------------------------------------
  // 4. Scroll-spy (IntersectionObserver, top 30% gate)
  // ----------------------------------------------------------------
  if (tocAside && tocItems.length > 0 && 'IntersectionObserver' in window) {
    const tocLinks = Array.from(tocAside.querySelectorAll('a[data-toc-target]'));
    const linkById = new Map(tocLinks.map((a) => [a.dataset.tocTarget, a]));

    const visible = new Set();
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) visible.add(entry.target.id);
          else visible.delete(entry.target.id);
        });

        let activeId = null;
        for (const item of tocItems) {
          if (visible.has(item.id)) {
            activeId = item.id;
            break;
          }
        }
        tocLinks.forEach((a) => a.classList.remove('is-active'));
        if (activeId && linkById.has(activeId)) {
          linkById.get(activeId).classList.add('is-active');
        }
      },
      { rootMargin: '-72px 0px -65% 0px', threshold: 0 }
    );
    headings.forEach((h) => observer.observe(h));
  }

  // ----------------------------------------------------------------
  // 5. Reading progress bar (scroll position 0-100%)
  // ----------------------------------------------------------------
  const progressBar = document.querySelector('.reading-progress');
  if (progressBar) {
    const update = () => {
      const rect = article.getBoundingClientRect();
      const top = window.scrollY + rect.top;
      const total = rect.height - window.innerHeight;
      const scrolled = Math.min(Math.max(window.scrollY - top + window.innerHeight * 0.2, 0), total);
      const pct = total > 0 ? (scrolled / total) * 100 : 0;
      progressBar.style.setProperty('--progress', `${pct.toFixed(1)}%`);
    };
    let ticking = false;
    const onScroll = () => {
      if (!ticking) {
        requestAnimationFrame(() => {
          update();
          ticking = false;
        });
        ticking = true;
      }
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', update, { passive: true });
    update();
  }

  // ----------------------------------------------------------------
  // 6. Auto-fill [data-reading-time] from word count (rough)
  //    Chinese: 1 char ≈ 1 word; ASCII: split by whitespace
  // ----------------------------------------------------------------
  const timeEl = document.querySelector('[data-reading-time]');
  if (timeEl && body) {
    const text = body.textContent || '';
    const cjk = (text.match(/[一-鿿]/g) || []).length;
    const asciiWords = (text.replace(/[一-鿿]/g, '').match(/\S+/g) || []).length;
    const total = cjk + asciiWords;
    // 約 350 字/分（中文閱讀速度）
    const min = Math.max(1, Math.round(total / 350));
    timeEl.textContent = `${min} min read`;
  }
})();
