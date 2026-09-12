/* =========================================================
   Conceito Odontológico — interações do site
   JS puro, sem dependências.
   ========================================================= */
(function () {
  'use strict';

  /* =======================================================
     1) DEPOIMENTOS
     -------------------------------------------------------
     IMPORTANTE: este array deve conter APENAS avaliações
     reais, copiadas na íntegra do perfil do Google (ou de
     outra plataforma onde o paciente publicou).
     NÃO preencher com texto inventado.

     Formato de cada item:
     {
       nome:  'João S.',                  // como aparece publicado, abreviado
       nota:  5,                          // 1 a 5, conforme a avaliação real
       texto: 'Texto integral da avaliação, sem resumir.',
       fonte: 'Google'                    // plataforma de origem
     }

     Enquanto o array estiver vazio, a seção exibe o bloco
     honesto de "depoimentos em curadoria" já presente no HTML.
     ======================================================= */
  var DEPOIMENTOS = [];

  /* =======================================================
     2) HORÁRIO DE FUNCIONAMENTO
     0 = domingo ... 6 = sábado. null = fechado.
     Fonte: site oficial (Seg–Sex 08:00–18:00).
     ======================================================= */
  var HORARIOS = {
    0: null,
    1: { abre: '08:00', fecha: '18:00' },
    2: { abre: '08:00', fecha: '18:00' },
    3: { abre: '08:00', fecha: '18:00' },
    4: { abre: '08:00', fecha: '18:00' },
    5: { abre: '08:00', fecha: '18:00' },
    6: null
  };
  var TZ = 'America/Sao_Paulo';
  var DIAS = ['domingo', 'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado'];

  var $  = function (sel, ctx) { return (ctx || document).querySelector(sel); };
  var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

  /* ------------------- Menu mobile ------------------- */
  function initNav() {
    var toggle = $('#navToggle');
    var menu = $('#navMenu');
    if (!toggle || !menu) return;

    function close() {
      menu.classList.remove('is-open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', 'Abrir menu de navegação');
    }
    function open() {
      menu.classList.add('is-open');
      toggle.setAttribute('aria-expanded', 'true');
      toggle.setAttribute('aria-label', 'Fechar menu de navegação');
    }

    toggle.addEventListener('click', function () {
      if (menu.classList.contains('is-open')) { close(); } else { open(); }
    });

    $$('a', menu).forEach(function (link) {
      link.addEventListener('click', close);
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && menu.classList.contains('is-open')) {
        close();
        toggle.focus();
      }
    });

    window.addEventListener('resize', function () {
      if (window.innerWidth >= 860) close();
    });
  }

  /* ------------------- Header ao rolar ------------------- */
  function initHeader() {
    var header = $('.site-header');
    if (!header) return;
    var ticking = false;
    function update() {
      header.classList.toggle('is-stuck', window.scrollY > 8);
      ticking = false;
    }
    window.addEventListener('scroll', function () {
      if (!ticking) { window.requestAnimationFrame(update); ticking = true; }
    }, { passive: true });
    update();
  }

  /* ------------------- Link ativo na navegação ------------------- */
  function initScrollSpy() {
    var links = $$('.nav-list a');
    if (!links.length || !('IntersectionObserver' in window)) return;

    var map = {};
    var sections = [];
    links.forEach(function (link) {
      var id = link.getAttribute('href');
      if (!id || id.charAt(0) !== '#') return;
      var section = document.querySelector(id);
      if (section) { map[section.id] = link; sections.push(section); }
    });

    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        links.forEach(function (l) { l.classList.remove('is-active'); });
        var active = map[entry.target.id];
        if (active) active.classList.add('is-active');
      });
    }, { rootMargin: '-45% 0px -50% 0px', threshold: 0 });

    sections.forEach(function (s) { observer.observe(s); });
  }

  /* ------------------- Scroll reveal ------------------- */
  function initReveal() {
    var items = $$('.reveal');
    if (!items.length) return;

    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced || !('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }

    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry, i) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        window.setTimeout(function () { el.classList.add('is-visible'); }, Math.min(i * 70, 350));
        obs.unobserve(el);
      });
    }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });

    items.forEach(function (el) { observer.observe(el); });
  }

  /* ------------------- Contadores ------------------- */
  function initCounters() {
    var nums = $$('.stat-num[data-count]');
    if (!nums.length) return;

    var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (reduced || !('IntersectionObserver' in window)) return;

    var observer = new IntersectionObserver(function (entries, obs) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        var target = parseInt(el.getAttribute('data-count'), 10) || 0;
        var suffix = el.getAttribute('data-suffix') || '';
        var start = null;
        var dur = 1100;
        function step(ts) {
          if (start === null) start = ts;
          var p = Math.min((ts - start) / dur, 1);
          var eased = 1 - Math.pow(1 - p, 3);
          el.textContent = Math.round(target * eased) + suffix;
          if (p < 1) window.requestAnimationFrame(step);
        }
        el.textContent = '0' + suffix;
        window.requestAnimationFrame(step);
        obs.unobserve(el);
      });
    }, { threshold: 0.5 });

    nums.forEach(function (el) { observer.observe(el); });
  }

  /* ------------------- Aberto agora ------------------- */
  function agoraEmSaoPaulo() {
    var fmt = new Intl.DateTimeFormat('pt-BR', {
      timeZone: TZ, weekday: 'short', hour: '2-digit', minute: '2-digit', hour12: false
    });
    var partes = {};
    fmt.formatToParts(new Date()).forEach(function (p) { partes[p.type] = p.value; });

    var mapaDias = { dom: 0, seg: 1, ter: 2, qua: 3, qui: 4, sex: 5, sáb: 6, sab: 6 };
    var chave = String(partes.weekday || '').toLowerCase().replace('.', '').slice(0, 3);
    var dia = mapaDias[chave];
    if (dia === undefined) dia = new Date().getDay();

    var h = parseInt(partes.hour, 10);
    if (h === 24) h = 0;
    return { dia: dia, minutos: h * 60 + parseInt(partes.minute, 10) };
  }

  function paraMinutos(hhmm) {
    var p = hhmm.split(':');
    return parseInt(p[0], 10) * 60 + parseInt(p[1], 10);
  }

  function proximaAbertura(diaAtual) {
    for (var i = 1; i <= 7; i++) {
      var d = (diaAtual + i) % 7;
      if (HORARIOS[d]) {
        return { dia: d, abre: HORARIOS[d].abre, amanha: i === 1 };
      }
    }
    return null;
  }

  function initStatus() {
    var badge = $('#statusBadge');
    var texto = $('#statusText');
    var detalhe = $('#statusDetail');
    if (!badge || !texto) return;

    var agora = agoraEmSaoPaulo();
    var hoje = HORARIOS[agora.dia];

    // Destaca a linha de hoje na tabela
    var linhaHoje = document.querySelector('.hours-table tr[data-day="' + agora.dia + '"]');
    if (linhaHoje) linhaHoje.classList.add('is-today');

    badge.classList.remove('status-unknown');

    if (hoje && agora.minutos >= paraMinutos(hoje.abre) && agora.minutos < paraMinutos(hoje.fecha)) {
      badge.classList.add('status-open');
      texto.textContent = 'Aberto agora';
      if (detalhe) detalhe.textContent = 'Fecha às ' + hoje.fecha + ' (horário de Brasília).';
      return;
    }

    badge.classList.add('status-closed');
    texto.textContent = 'Fechado agora';

    if (detalhe) {
      if (hoje && agora.minutos < paraMinutos(hoje.abre)) {
        detalhe.textContent = 'Abre hoje às ' + hoje.abre + ' (horário de Brasília).';
      } else {
        var prox = proximaAbertura(agora.dia);
        detalhe.textContent = prox
          ? 'Abre ' + (prox.amanha ? 'amanhã' : DIAS[prox.dia]) + ' às ' + prox.abre + ' (horário de Brasília).'
          : 'Consulte os horários abaixo.';
      }
    }
  }

  /* ------------------- Depoimentos ------------------- */
  function initDepoimentos() {
    var grid = $('#depoimentosGrid');
    var vazio = $('#depoimentosVazio');
    if (!grid) return;

    if (!DEPOIMENTOS.length) {
      grid.hidden = true;
      return;
    }

    if (vazio) vazio.hidden = true;
    grid.hidden = false;

    DEPOIMENTOS.forEach(function (dep) {
      var nota = Math.max(0, Math.min(5, Math.round(Number(dep.nota) || 0)));

      var card = document.createElement('figure');
      card.className = 'testimonial reveal';

      var estrelas = document.createElement('div');
      estrelas.className = 'testimonial-stars';
      estrelas.textContent = '★★★★★'.slice(0, nota) + '☆☆☆☆☆'.slice(0, 5 - nota);
      estrelas.setAttribute('role', 'img');
      estrelas.setAttribute('aria-label', 'Avaliação de ' + nota + ' de 5 estrelas');

      var quote = document.createElement('blockquote');
      quote.className = 'testimonial-text';
      quote.textContent = '“' + dep.texto + '”';

      var caption = document.createElement('figcaption');
      caption.className = 'testimonial-author';
      caption.textContent = dep.nome;
      if (dep.fonte) {
        var fonte = document.createElement('span');
        fonte.className = 'testimonial-source';
        fonte.textContent = ' · ' + dep.fonte;
        caption.appendChild(fonte);
      }

      card.appendChild(estrelas);
      card.appendChild(quote);
      card.appendChild(caption);
      grid.appendChild(card);
    });
  }

  /* ------------------- Ano no rodapé ------------------- */
  function initAno() {
    var el = $('#ano');
    if (el) el.textContent = String(new Date().getFullYear());
  }

  /* ------------------- Boot ------------------- */
  function boot() {
    initNav();
    initHeader();
    initScrollSpy();
    initStatus();
    initDepoimentos();
    initAno();
    initReveal();
    initCounters();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
