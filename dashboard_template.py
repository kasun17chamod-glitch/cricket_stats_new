"""
Dashboard HTML template — exact replica of the original cricket-dashboard-modern
index.html, with two Streamlit hosting adjustments and the final dashboard font update:

1. Vendor-bundled libraries (Tailwind, Chart.js, Lucide) are swapped for CDN
   builds so no static files need to be served.
2. The font has been changed to **Manrope** (loaded from Google Fonts),
   applied uniformly across headings, body text, labels, buttons, inputs,
   tables, badges, numbers and chart text. Italic styling has been removed.

Everything else — the layout, colours, gradients, glass cards, charts,
animations, filter drawer, mobile bottom-tab bar, sortable match log — is
preserved 1:1 from the original.
"""

import json


def build_dashboard_html(cricket_data: list, profile_img_src: str) -> str:
    """Return the full self-contained dashboard HTML.

    Parameters
    ----------
    cricket_data : list[dict]
        The same shape as ``window.CRICKET_DATA`` in the original ``data.js``.
    profile_img_src : str
        URL or ``data:`` URI for the player photo.
    """

    # Inject data as JSON (json.dumps emits valid JS literal; json's `null` is
    # valid in JS and Python's True/False are converted to true/false).
    data_json = json.dumps(cricket_data)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover" />
<meta name="theme-color" content="#0a0e1a" />
<title>Kasun Chamod · Cricket Stats</title>



<!-- Tailwind via play CDN -->
<script src="https://cdn.tailwindcss.com"></script>
<script>
  // Custom palette — re-implements the colours the original vendor/tailwind
  // build had baked in (ink/bat/bowl/mint), so all `text-bat-400`, `bg-ink-900`,
  // `from-bowl-500` etc. classes in the markup keep working unchanged.
  tailwind.config = {{
    theme: {{
      extend: {{
        colors: {{
          ink:  {{ 0:'#000000', 900:'#0a0e1a' }},
          bat:  {{ 200:'#a5f3fc', 400:'#22d3ee', 500:'#06b6d4' }},
          bowl: {{ 200:'#fde68a', 400:'#fbbf24', 500:'#f59e0b' }},
          mint: {{ 400:'#34d399' }},
        }},
        boxShadow: {{
          glow: '0 0 24px -4px rgba(34,211,238,.45)',
          card: '0 30px 60px -30px rgba(0,0,0,.6)',
        }}
      }}
    }}
  }}
</script>

<!-- Chart.js & Lucide icons -->
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
<script src="https://unpkg.com/lucide@latest/dist/umd/lucide.min.js"></script>

<style>
  :root {{
    --grain-opacity: .035;
  }}

  html, body {{ background: #0a0e1a; }}
  body {{
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif;
    color: #e5e7eb;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    overflow-x: hidden;
    margin: 0;
  }}

  /* Final font pass — Manrope everywhere, no italic styling. */
  body, button, input, select, option, textarea, label, table, th, td,
  thead, tbody, tr, nav, header, footer, p, span, div, small, strong,
  em, a, li, ul, ol, code, h1, h2, h3, h4, h5, h6 {{
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif !important;
  }}
  .font-serif, .num-display, .font-mono, .num {{
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif !important;
  }}
  .italic, i:not([data-lucide]) {{
    font-style: normal !important;
  }}
  .font-serif {{
    font-weight: 700;
  }}
  .num-display {{
    font-weight: 700;
    letter-spacing: -0.03em;
  }}
  .font-mono, .num {{
    font-variant-numeric: tabular-nums;
  }}

  /* Atmospheric background — gradient mesh + soft grain */
  .app-bg {{
    position: fixed; inset: 0; z-index: -2;
    background:
      radial-gradient(70% 50% at 8% -5%,  rgba(34,211,238,.18) 0%, transparent 60%),
      radial-gradient(50% 40% at 95% 12%, rgba(245,158,11,.12) 0%, transparent 60%),
      radial-gradient(50% 60% at 60% 110%, rgba(59,130,246,.18) 0%, transparent 60%),
      linear-gradient(180deg, #060912 0%, #0a0e1a 60%, #0a0e1a 100%);
  }}
  .app-grain {{
    position: fixed; inset: 0; z-index: -1; pointer-events: none;
    opacity: var(--grain-opacity);
    background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='200' height='200'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .6 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  }}

  /* Glass card */
  .glass {{
    background: linear-gradient(180deg, rgba(255,255,255,.04) 0%, rgba(255,255,255,.015) 100%);
    border: 1px solid rgba(255,255,255,.08);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border-radius: 22px;
  }}
  .glass-strong {{
    background: linear-gradient(180deg, rgba(20,28,48,.7) 0%, rgba(10,14,26,.7) 100%);
    border: 1px solid rgba(255,255,255,.08);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border-radius: 24px;
  }}

  /* Stat card hover */
  .stat-card {{ transition: transform .35s cubic-bezier(.2,.7,.2,1), border-color .35s, box-shadow .35s; }}
  .stat-card:hover {{ transform: translateY(-3px); border-color: rgba(34,211,238,.35); box-shadow: 0 20px 40px -20px rgba(34,211,238,.25); }}
  .stat-card--bowl:hover {{ border-color: rgba(251,191,36,.45); box-shadow: 0 20px 40px -20px rgba(251,191,36,.25); }}

  /* Numbers */
  .num {{ font-variant-numeric: tabular-nums; letter-spacing: -0.02em; }}
  .num-display {{ letter-spacing: -0.02em; }}

  /* Animated reveal */
  @keyframes rise {{ from {{ opacity: 0; transform: translateY(14px); }} to {{ opacity: 1; transform: translateY(0); }} }}
  .reveal {{ animation: rise .7s cubic-bezier(.2,.7,.2,1) both; }}

  /* Profile ring pulse */
  @keyframes ringPulse {{
    0%,100% {{ box-shadow: 0 0 0 0 rgba(34,211,238,.35), inset 0 0 0 1px rgba(34,211,238,.4); }}
    50%     {{ box-shadow: 0 0 0 12px rgba(34,211,238,0), inset 0 0 0 1px rgba(34,211,238,.4); }}
  }}
  .profile-ring {{ animation: ringPulse 3s ease-in-out infinite; }}

  /* Tab underline indicator */
  .tab-btn {{ position: relative; transition: color .25s; background: transparent; border: 0; cursor: pointer; color: inherit; }}
  .tab-btn[data-active="true"] {{ color: #fff; }}
  .tab-btn[data-active="true"]::after {{
    content: ""; position: absolute; left: 12px; right: 12px; bottom: -1px; height: 2px;
    background: linear-gradient(90deg, #22d3ee, #f59e0b);
    border-radius: 2px;
  }}

  /* Filter chip */
  .chip {{
    display: inline-flex; align-items: center; gap: 6px;
    padding: 6px 12px; border-radius: 999px;
    border: 1px solid rgba(255,255,255,.1);
    background: rgba(255,255,255,.04);
    font-size: 13px; color: #cbd5e1;
    transition: all .2s;
    cursor: pointer; user-select: none;
    white-space: nowrap;
  }}
  .chip:hover {{ border-color: rgba(255,255,255,.25); color: #fff; }}
  .chip[data-active="true"] {{
    background: linear-gradient(180deg, rgba(34,211,238,.18), rgba(34,211,238,.06));
    border-color: rgba(34,211,238,.45);
    color: #ecfeff;
  }}
  .chip[data-active="true"][data-color="bowl"] {{
    background: linear-gradient(180deg, rgba(245,158,11,.18), rgba(245,158,11,.06));
    border-color: rgba(245,158,11,.45);
    color: #fffbeb;
  }}
  .chip[data-active="true"][data-color="mint"] {{
    background: linear-gradient(180deg, rgba(52,211,153,.18), rgba(52,211,153,.06));
    border-color: rgba(52,211,153,.45);
    color: #ecfdf5;
  }}

  /* Form pill */
  .form-pill {{
    width: 28px; height: 28px; border-radius: 8px;
    display: inline-flex; align-items: center; justify-content: center;
    font-size: 11px; font-weight: 700; color: #fff;
    font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif;
  }}

  /* Subtle scrollbar */
  ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
  ::-webkit-scrollbar-track {{ background: transparent; }}
  ::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,.08); border-radius: 10px; }}
  ::-webkit-scrollbar-thumb:hover {{ background: rgba(255,255,255,.18); }}

  .scroll-x {{ -ms-overflow-style: none; scrollbar-width: none; }}
  .scroll-x::-webkit-scrollbar {{ display: none; }}

  .mobile-tabbar {{ padding-bottom: max(0.5rem, env(safe-area-inset-bottom)); }}

  section[id] {{ scroll-margin-top: 80px; }}

  .accent-line {{
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(34,211,238,.6), rgba(245,158,11,.6), transparent);
  }}

  /* Table */
  .ctable {{ width: 100%; border-collapse: separate; border-spacing: 0; }}
  .ctable th {{ font-size: 11px; text-transform: uppercase; letter-spacing: .08em; color: #94a3b8; font-weight: 600; padding: 10px 14px; text-align: left; background: rgba(255,255,255,.02); border-bottom: 1px solid rgba(255,255,255,.06); }}
  .ctable td {{ padding: 12px 14px; border-bottom: 1px solid rgba(255,255,255,.05); font-size: 14px; }}
  .ctable tr:last-child td {{ border-bottom: none; }}
  .ctable tr:hover td {{ background: rgba(34,211,238,.04); }}
  .ctable th.sortable {{ cursor: pointer; user-select: none; }}
  .ctable th.sortable:hover {{ color: #fff; }}

  /* Badges */
  .badge {{
    display: inline-block; padding: 2px 8px; border-radius: 6px; font-size: 11px; font-weight: 600;
    border: 1px solid rgba(255,255,255,.1); background: rgba(255,255,255,.04); color: #cbd5e1;
  }}
  .badge-bat  {{ color: #a5f3fc; border-color: rgba(34,211,238,.3); background: rgba(34,211,238,.08); }}
  .badge-bowl {{ color: #fde68a; border-color: rgba(245,158,11,.3); background: rgba(245,158,11,.08); }}
  .badge-100  {{ color: #fff;    background: linear-gradient(135deg,#06b6d4,#0891b2); border-color: transparent; }}
  .badge-50   {{ color: #082f49; background: linear-gradient(135deg,#a5f3fc,#67e8f9); border-color: transparent; }}
  .badge-5w   {{ color: #fff;    background: linear-gradient(135deg,#d97706,#92400e); border-color: transparent; }}
  .badge-3w   {{ color: #422006; background: linear-gradient(135deg,#fde68a,#fbbf24); border-color: transparent; }}

  .hr-soft {{ height: 1px; background: linear-gradient(90deg, transparent, rgba(255,255,255,.12), transparent); }}

  button:focus-visible, [role="tab"]:focus-visible, .chip:focus-visible {{
    outline: 2px solid #22d3ee; outline-offset: 2px; border-radius: 12px;
  }}

  canvas {{ max-width: 100%; }}
  .glass canvas {{ width: 100% !important; height: 100% !important; display: block; }}

  /* Donut center label */
  .donut-wrap {{ position: relative; }}
  .donut-wrap canvas {{ width: 100% !important; height: 100% !important; display: block; }}
  .donut-center {{
    position: absolute; inset: 0; display: flex; flex-direction: column;
    align-items: center; justify-content: center; pointer-events: none; text-align: center;
  }}

  .empty {{
    color: #64748b; font-size: 13px; padding: 20px; text-align: center;
    border: 1px dashed rgba(255,255,255,.1); border-radius: 14px;
  }}

  .search-input {{
    background: rgba(255,255,255,.04);
    border: 1px solid rgba(255,255,255,.1);
    color: #e5e7eb;
    padding: 10px 14px 10px 38px;
    border-radius: 12px;
    width: 100%;
    font-size: 14px;
    transition: all .2s;
  }}
  .search-input:focus {{ outline: none; border-color: rgba(34,211,238,.5); background: rgba(255,255,255,.06); }}
  .search-input::placeholder {{ color: #64748b; }}

  @media (max-width: 640px) {{
    .num-display {{ letter-spacing: -0.03em; }}
    section[id] {{ scroll-margin-top: 64px; }}
  }}

  .tab-mob {{ color: #64748b; transition: color .2s; background: transparent; border: 0; cursor: pointer; }}
  .tab-mob[data-active="true"] {{ color: #22d3ee; }}
  .tab-mob[data-active="true"] i {{ filter: drop-shadow(0 0 8px rgba(34,211,238,.5)); }}
</style>
</head>

<body>
<!-- Background layers -->
<div class="app-bg"></div>
<div class="app-grain"></div>

<!-- ============= TOP NAV ============= -->
<header class="sticky top-0 z-40 backdrop-blur-xl bg-ink-900/70 border-b border-white/5">
  <div class="max-w-7xl mx-auto px-4 sm:px-6 h-14 sm:h-16 flex items-center justify-between gap-4">
    <div class="flex items-center gap-2.5 min-w-0">
      <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-bat-400 to-bowl-500 grid place-items-center shadow-glow shrink-0">
        <i data-lucide="trophy" class="w-4 h-4 text-ink-900"></i>
      </div>
      <div class="leading-tight min-w-0">
        <div class="text-[11px] uppercase tracking-[0.2em] text-slate-400">Player Stats</div>
        <div class="text-sm font-semibold truncate">Kasun Chamod</div>
      </div>
    </div>

    <nav id="topTabs" class="hidden md:flex items-center gap-1 text-sm text-slate-400 font-medium" role="tablist">
      <button class="tab-btn px-3 py-2"   data-tab="overview" data-active="true"  role="tab">Overview</button>
      <button class="tab-btn px-3 py-2"   data-tab="batting"  data-active="false" role="tab">Batting</button>
      <button class="tab-btn px-3 py-2"   data-tab="bowling"  data-active="false" role="tab">Bowling</button>
      <button class="tab-btn px-3 py-2"   data-tab="matches"  data-active="false" role="tab">Matches</button>
    </nav>

    <button id="openFilters" class="flex items-center gap-2 text-sm font-medium px-3 py-2 rounded-lg border border-white/10 hover:border-white/25 hover:bg-white/5 transition shrink-0" style="color:#e5e7eb;background:transparent;">
      <i data-lucide="sliders-horizontal" class="w-4 h-4"></i>
      <span class="hidden sm:inline">Filters</span>
      <span id="activeFilterCount" class="hidden text-[11px] px-1.5 py-0.5 rounded-md bg-bat-400 text-ink-900 font-bold"></span>
    </button>
  </div>
</header>

<!-- ============= MAIN ============= -->
<main class="max-w-7xl mx-auto px-4 sm:px-6 pb-32 md:pb-12">

  <!-- HERO -->
  <section class="pt-6 sm:pt-10 reveal">
    <div class="glass-strong shadow-card overflow-hidden relative">
      <svg class="absolute inset-0 w-full h-full opacity-[.05] pointer-events-none" aria-hidden="true">
        <defs>
          <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
            <path d="M 40 0 L 0 0 0 40" fill="none" stroke="white" stroke-width="0.5"/>
          </pattern>
        </defs>
        <rect width="100%" height="100%" fill="url(#grid)"/>
      </svg>

      <div class="relative grid grid-cols-1 md:grid-cols-[auto,1fr] gap-6 md:gap-10 p-6 sm:p-8 md:p-10 items-center">
        <div class="flex md:block items-center gap-5">
          <div class="relative w-24 h-24 sm:w-32 sm:h-32 md:w-44 md:h-44 shrink-0">
            <div class="absolute inset-0 rounded-full bg-gradient-to-br from-bat-400 via-blue-500 to-bowl-500 blur-2xl opacity-50"></div>
            <div class="relative w-full h-full rounded-full p-[3px] bg-gradient-to-br from-bat-400 via-blue-500 to-bowl-500 profile-ring">
              <img src="{profile_img_src}" alt="Kasun Chamod" class="w-full h-full rounded-full object-cover" loading="eager"/>
            </div>
          </div>

          <div class="md:hidden">
            <div class="text-[11px] uppercase tracking-[0.2em] text-bat-400 font-semibold">All-Rounder</div>
            <h1 class="font-serif text-3xl leading-tight mt-1">Kasun Chamod</h1>
          </div>
        </div>

        <div>
          <div class="hidden md:flex items-center gap-3">
            <span class="text-[11px] uppercase tracking-[0.25em] text-bat-400 font-semibold">All-Rounder</span>
            <div class="h-3 w-px bg-white/15"></div>
            <span class="text-[11px] uppercase tracking-[0.25em] text-slate-400">Career 2024 — 2026</span>
          </div>

          <h1 class="hidden md:block font-serif text-5xl lg:text-6xl leading-[1.05] mt-2 text-white">
            Kasun Chamod
          </h1>

          <p class="mt-2 sm:mt-3 text-slate-300 text-sm sm:text-base flex flex-wrap items-center gap-x-3 gap-y-1">
            <span class="inline-flex items-center gap-1.5"><i data-lucide="circle-dot" class="w-3.5 h-3.5 text-bat-400"></i>Right-hand Bat</span>
            <span class="text-slate-600">·</span>
            <span class="inline-flex items-center gap-1.5"><i data-lucide="rotate-ccw" class="w-3.5 h-3.5 text-bowl-400"></i>Left-arm Orthodox</span>
          </p>

          <div class="accent-line mt-5"></div>

          <div class="grid grid-cols-2 sm:grid-cols-4 gap-3 sm:gap-4 mt-5">
            <div>
              <div class="text-[11px] uppercase tracking-[0.15em] text-slate-400">Matches</div>
              <div class="num-display num text-4xl sm:text-5xl mt-1 text-white" id="kpi-matches">—</div>
            </div>
            <div>
              <div class="text-[11px] uppercase tracking-[0.15em] text-slate-400">Runs</div>
              <div class="num-display num text-4xl sm:text-5xl mt-1 text-bat-400" id="kpi-runs">—</div>
            </div>
            <div>
              <div class="text-[11px] uppercase tracking-[0.15em] text-slate-400">Wickets</div>
              <div class="num-display num text-4xl sm:text-5xl mt-1 text-bowl-400" id="kpi-wickets">—</div>
            </div>
            <div>
              <div class="text-[11px] uppercase tracking-[0.15em] text-slate-400">Catches</div>
              <div class="num-display num text-4xl sm:text-5xl mt-1 text-mint-400" id="kpi-catches">—</div>
            </div>
          </div>

          <div class="mt-6 flex flex-col sm:flex-row sm:items-center gap-3 sm:gap-6">
            <div class="flex items-center gap-3">
              <span class="text-[11px] uppercase tracking-[0.15em] text-slate-400">Recent Form</span>
              <div id="recentFormPills" class="flex items-center gap-1.5"></div>
            </div>
            <div id="recentFormSummary" class="text-sm text-slate-300"></div>
          </div>
        </div>
      </div>
    </div>
  </section>

  <!-- ACTIVE FILTERS -->
  <section id="activeFiltersBar" class="mt-4 hidden">
    <div class="flex items-center gap-2 flex-wrap">
      <span class="text-[11px] uppercase tracking-[0.15em] text-slate-400 mr-1">Active filters</span>
      <div id="activeFiltersChips" class="flex flex-wrap gap-2"></div>
      <button id="clearAllFilters" class="text-xs text-bat-400 hover:text-bat-200 underline underline-offset-4 ml-2" style="background:transparent;border:0;cursor:pointer;">Clear all</button>
    </div>
  </section>

  <!-- OVERVIEW -->
  <div data-tab-pane="overview">
    <section class="mt-8 reveal">
      <div class="flex items-end justify-between mb-4">
        <div>
          <h2 class="font-serif text-3xl sm:text-4xl text-white">Career at a glance</h2>
          <p class="text-sm text-slate-400 mt-1">A quick read of every format</p>
        </div>
      </div>
      <div id="formatGrid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"></div>
    </section>

    <section class="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-4 reveal">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-lg bg-bat-400/15 grid place-items-center"><i data-lucide="circle-dot" class="w-4 h-4 text-bat-400"></i></div>
            <h3 class="text-lg font-semibold">Batting</h3>
          </div>
          <button class="text-xs text-bat-400 hover:text-bat-200 inline-flex items-center gap-1" data-jump="batting" style="background:transparent;border:0;cursor:pointer;">Details <i data-lucide="arrow-right" class="w-3 h-3"></i></button>
        </div>
        <div class="grid grid-cols-3 gap-3 text-center" id="overviewBattingMini"></div>
      </div>

      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-lg bg-bowl-500/15 grid place-items-center"><i data-lucide="rotate-ccw" class="w-4 h-4 text-bowl-400"></i></div>
            <h3 class="text-lg font-semibold">Bowling</h3>
          </div>
          <button class="text-xs text-bowl-400 hover:text-bowl-200 inline-flex items-center gap-1" data-jump="bowling" style="background:transparent;border:0;cursor:pointer;">Details <i data-lucide="arrow-right" class="w-3 h-3"></i></button>
        </div>
        <div class="grid grid-cols-3 gap-3 text-center" id="overviewBowlingMini"></div>
      </div>
    </section>

    <section class="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-4 reveal">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Runs by year</h3>
            <p class="text-xs text-slate-400">Yearly batting output</p>
          </div>
          <i data-lucide="bar-chart-3" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-56 sm:h-64"><canvas id="chart-runs-year"></canvas></div>
      </div>

      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Wickets by year</h3>
            <p class="text-xs text-slate-400">Yearly bowling output</p>
          </div>
          <i data-lucide="bar-chart-3" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-56 sm:h-64"><canvas id="chart-wickets-year"></canvas></div>
      </div>
    </section>

    <section class="mt-10 reveal">
      <h2 class="font-serif text-3xl text-white">Milestones</h2>
      <p class="text-sm text-slate-400 mt-1">Notable performances</p>
      <div id="milestonesGrid" class="mt-5 grid grid-cols-2 md:grid-cols-4 gap-3"></div>
    </section>
  </div>

  <!-- BATTING -->
  <div data-tab-pane="batting" class="hidden">
    <section class="mt-8 reveal">
      <div class="flex items-end justify-between mb-4">
        <div>
          <h2 class="font-serif text-3xl sm:text-4xl text-white">Batting</h2>
          <p class="text-sm text-slate-400 mt-1">Every metric, every milestone</p>
        </div>
      </div>
      <div id="battingStatGrid" class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4"></div>
    </section>

    <section class="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-4 reveal">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Average progression</h3>
            <p class="text-xs text-slate-400">Cumulative average per innings</p>
          </div>
          <i data-lucide="trending-up" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bat-avg"></canvas></div>
      </div>

      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Strike rate progression</h3>
            <p class="text-xs text-slate-400">Cumulative strike rate per innings</p>
          </div>
          <i data-lucide="zap" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bat-sr"></canvas></div>
      </div>

      <div class="glass p-5 sm:p-6 lg:col-span-2">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Runs per innings</h3>
            <p class="text-xs text-slate-400">Each bar is one innings · highest score highlighted</p>
          </div>
          <i data-lucide="bar-chart-3" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bat-perInnings"></canvas></div>
      </div>
    </section>

    <section class="mt-10 grid grid-cols-1 lg:grid-cols-[1fr,1.4fr] gap-4 reveal">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">How got out</h3>
            <p class="text-xs text-slate-400">Dismissal breakdown</p>
          </div>
          <i data-lucide="pie-chart" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="donut-wrap h-56 sm:h-64">
          <canvas id="chart-dismissals"></canvas>
          <div class="donut-center">
            <div class="text-[11px] uppercase tracking-[0.15em] text-slate-400">Total outs</div>
            <div id="dismissTotal" class="num-display num text-4xl mt-0.5">0</div>
          </div>
        </div>
        <div id="dismissLegend" class="mt-4 grid grid-cols-2 gap-2"></div>
      </div>

      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Best knocks</h3>
            <p class="text-xs text-slate-400">All scores 30 and above</p>
          </div>
          <i data-lucide="award" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div id="bestKnocksList" class="space-y-2"></div>
      </div>
    </section>
  </div>

  <!-- BOWLING -->
  <div data-tab-pane="bowling" class="hidden">
    <section class="mt-8 reveal">
      <h2 class="font-serif text-3xl sm:text-4xl text-white">Bowling</h2>
      <p class="text-sm text-slate-400 mt-1">Wickets, control and consistency</p>
      <div id="bowlingStatGrid" class="mt-4 grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-3 sm:gap-4"></div>
    </section>

    <section class="mt-10 grid grid-cols-1 lg:grid-cols-2 gap-4 reveal">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Bowling average</h3>
            <p class="text-xs text-slate-400">Cumulative · lower is better</p>
          </div>
          <i data-lucide="trending-down" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bowl-avg"></canvas></div>
      </div>

      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Economy</h3>
            <p class="text-xs text-slate-400">Cumulative runs per over</p>
          </div>
          <i data-lucide="gauge" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bowl-econ"></canvas></div>
      </div>

      <div class="glass p-5 sm:p-6 lg:col-span-2">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Wickets per match</h3>
            <p class="text-xs text-slate-400">Each bar is one bowling innings</p>
          </div>
          <i data-lucide="bar-chart-3" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div class="h-64 sm:h-72"><canvas id="chart-bowl-perInnings"></canvas></div>
      </div>
    </section>

    <section class="mt-10 reveal">
      <div class="glass p-5 sm:p-6">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h3 class="text-lg font-semibold">Best bowling spells</h3>
            <p class="text-xs text-slate-400">3-wicket hauls and better</p>
          </div>
          <i data-lucide="flame" class="w-4 h-4 text-slate-500"></i>
        </div>
        <div id="bestSpellsList" class="space-y-2"></div>
      </div>
    </section>
  </div>

  <!-- MATCHES -->
  <div data-tab-pane="matches" class="hidden">
    <section class="mt-8 reveal">
      <div class="flex flex-col sm:flex-row sm:items-end sm:justify-between gap-3 mb-4">
        <div>
          <h2 class="font-serif text-3xl sm:text-4xl text-white">Match log</h2>
          <p class="text-sm text-slate-400 mt-1">Every game, every contribution</p>
        </div>
        <div class="relative w-full sm:max-w-xs">
          <i data-lucide="search" class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"></i>
          <input id="matchSearch" type="text" placeholder="Search opponent…" class="search-input"/>
        </div>
      </div>

      <div class="glass overflow-hidden">
        <div class="hidden md:block overflow-x-auto">
          <table class="ctable">
            <thead>
              <tr>
                <th class="sortable" data-sort="matchId">#</th>
                <th class="sortable" data-sort="Year">Year</th>
                <th class="sortable" data-sort="Match_Type">Format</th>
                <th class="sortable" data-sort="Opponent">Opponent</th>
                <th class="sortable text-right" data-sort="Runs">Bat</th>
                <th class="sortable" data-sort="Dismissal">Dismissal</th>
                <th class="sortable text-right" data-sort="Wickets">Bowl</th>
                <th class="text-right">Notes</th>
              </tr>
            </thead>
            <tbody id="matchTableBody"></tbody>
          </table>
        </div>
        <div id="matchCardList" class="md:hidden divide-y divide-white/5"></div>
      </div>

      <div id="matchEmpty" class="empty mt-3 hidden">No matches match the current filters.</div>
    </section>
  </div>

  <footer class="mt-16 pt-8 border-t border-white/5 text-center text-xs text-slate-500">
    <p>Career stats · Updated <span id="lastUpdated"></span></p>
    <p class="mt-1">Built with care · Hosted on Streamlit · Edit <code class="text-slate-400">data.py</code> to add new matches.</p>
  </footer>
</main>

<!-- MOBILE BOTTOM TAB BAR -->
<nav class="md:hidden fixed bottom-0 left-0 right-0 z-40 bg-ink-900/90 backdrop-blur-xl border-t border-white/10 mobile-tabbar">
  <div class="grid grid-cols-4 max-w-md mx-auto" id="mobileTabs" role="tablist">
    <button class="tab-mob flex flex-col items-center gap-1 py-2.5 text-[11px] font-medium" data-tab="overview" data-active="true">
      <i data-lucide="layout-dashboard" class="w-5 h-5"></i><span>Overview</span>
    </button>
    <button class="tab-mob flex flex-col items-center gap-1 py-2.5 text-[11px] font-medium" data-tab="batting" data-active="false">
      <i data-lucide="circle-dot" class="w-5 h-5"></i><span>Batting</span>
    </button>
    <button class="tab-mob flex flex-col items-center gap-1 py-2.5 text-[11px] font-medium" data-tab="bowling" data-active="false">
      <i data-lucide="rotate-ccw" class="w-5 h-5"></i><span>Bowling</span>
    </button>
    <button class="tab-mob flex flex-col items-center gap-1 py-2.5 text-[11px] font-medium" data-tab="matches" data-active="false">
      <i data-lucide="list" class="w-5 h-5"></i><span>Matches</span>
    </button>
  </div>
</nav>

<!-- FILTER DRAWER -->
<div id="filterDrawer" class="fixed inset-0 z-50 hidden">
  <div id="filterBackdrop" class="absolute inset-0 bg-black/60 backdrop-blur-sm"></div>

  <aside class="absolute right-0 top-0 bottom-0 w-full sm:max-w-md bg-ink-900 border-l border-white/10 overflow-y-auto p-5 sm:p-6">
    <div class="flex items-center justify-between mb-6">
      <div>
        <div class="text-[11px] uppercase tracking-[0.2em] text-slate-400">Filters</div>
        <h3 class="text-2xl font-serif mt-0.5">Refine stats</h3>
      </div>
      <button id="closeFilters" class="w-9 h-9 grid place-items-center rounded-lg border border-white/10 hover:border-white/30 transition" style="background:transparent;color:inherit;cursor:pointer;">
        <i data-lucide="x" class="w-4 h-4"></i>
      </button>
    </div>

    <div class="mb-6">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-sm font-semibold text-bat-400 flex items-center gap-2">
          <i data-lucide="calendar" class="w-4 h-4"></i> Year
        </h4>
        <button class="text-xs text-slate-400 hover:text-white" data-toggle-all="years" style="background:transparent;border:0;cursor:pointer;">Toggle all</button>
      </div>
      <div id="yearFilters" class="flex flex-wrap gap-2"></div>
    </div>

    <div class="mb-6">
      <div class="flex items-center justify-between mb-3">
        <h4 class="text-sm font-semibold text-bowl-400 flex items-center gap-2">
          <i data-lucide="trophy" class="w-4 h-4"></i> Format
        </h4>
        <button class="text-xs text-slate-400 hover:text-white" data-toggle-all="types" style="background:transparent;border:0;cursor:pointer;">Toggle all</button>
      </div>
      <div id="typeFilters" class="flex flex-wrap gap-2"></div>
    </div>

    <div class="mb-6">
      <h4 class="text-sm font-semibold text-mint-400 flex items-center gap-2 mb-3">
        <i data-lucide="users" class="w-4 h-4"></i> Opponent
      </h4>
      <div class="relative mb-2">
        <i data-lucide="search" class="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-500"></i>
        <input id="opponentSearch" type="text" placeholder="Search teams…" class="search-input"/>
      </div>
      <div id="opponentFilters" class="flex flex-wrap gap-2 max-h-56 overflow-y-auto pr-1"></div>
      <p class="text-[11px] text-slate-500 mt-2">Leave none selected to include all opponents.</p>
    </div>

    <div class="hr-soft my-4"></div>

    <div class="flex items-center gap-3">
      <button id="resetFilters" class="flex-1 px-4 py-3 rounded-xl border border-white/10 text-sm font-semibold hover:border-white/30 transition" style="background:transparent;color:#e5e7eb;cursor:pointer;">Reset</button>
      <button id="applyFilters" class="flex-1 px-4 py-3 rounded-xl bg-gradient-to-r from-bat-500 to-bat-400 text-ink-900 text-sm font-bold hover:from-bat-400 hover:to-bat-200 transition" style="border:0;cursor:pointer;">Apply</button>
    </div>
  </aside>
</div>

<!-- ============= DATA & APP LOGIC (verbatim from original) ============= -->
<script>
window.CRICKET_DATA = {data_json};
</script>

<script>
(() => {{
  'use strict';

  const $  = (sel, ctx=document) => ctx.querySelector(sel);
  const $$ = (sel, ctx=document) => Array.from(ctx.querySelectorAll(sel));
  const fmt = (n, d=0) => (n == null || isNaN(n)) ? '—' : Number(n).toLocaleString('en-US', {{ minimumFractionDigits:d, maximumFractionDigits:d }});

  if (window.Chart) {{
    Chart.defaults.font.family = "'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, system-ui, sans-serif";
    Chart.defaults.font.size = 12;
  }}

  const oversToBalls = ov => {{
    if (ov == null) return 0;
    const s = String(ov);
    const [o, b='0'] = s.split('.');
    return (parseInt(o,10)||0)*6 + (parseInt(b,10)||0);
  }};
  const ballsToOvers = balls => `${{Math.floor(balls/6)}}.${{balls%6}}`;

  const normalizeDismissal = d => {{
    if (!d) return null;
    const k = String(d).trim().toLowerCase();
    const map = {{
      'lbw':'LBW','runout':'Run Out','run out':'Run Out',
      'stump':'Stumped','stumped':'Stumped','bowled':'Bowled',
      'caught':'Caught','hit wkt':'Hit Wicket','hit wicket':'Hit Wicket',
      'caught b':'Caught Behind','caught and bowled':'Caught Behind',
      'caught & bowled':'Caught Behind','c&b':'Caught Behind',
      'caught behind':'Caught Behind'
    }};
    return map[k] || (k.charAt(0).toUpperCase()+k.slice(1));
  }};

  const normalizeMatchType = t => {{
    if (!t) return t;

    const clean = String(t).trim();
    const lower = clean.toLowerCase();

    const map = {{
      'inter uni': 'Inter University',
      'inter university': 'Inter University',
    }};

    return map[lower] || clean;
  }};

  const RAW = (window.CRICKET_DATA || []).map((r,i) => ({{
    ...r,
    matchId: r.matchId ?? (i+1),
    Dismissal: normalizeDismissal(r.Dismissal),
    Match_Type: normalizeMatchType(r.Match_Type),
  }}));

  const allYears  = [...new Set(RAW.map(r => r.Year).filter(Boolean))].sort();
  const allTypes  = [...new Set(RAW.map(r => r.Match_Type).filter(Boolean))].sort();
  const allOpps   = [...new Set(RAW.map(r => r.Opponent).filter(Boolean))].sort();

  const state = {{
    years:  new Set(allYears),
    types:  new Set(allTypes),
    opps:   new Set(),
    tab:    'overview',
    matchSort: {{ key:'matchId', dir:'asc' }},
    matchSearch: '',
  }};

  function getFiltered() {{
    return RAW.filter(r =>
      state.years.has(r.Year) &&
      state.types.has(r.Match_Type) &&
      (state.opps.size === 0 || state.opps.has(r.Opponent))
    );
  }}

  function computeBatting(df) {{
    const bat = df.filter(r => r.Runs != null);
    const matches = df.length;
    const innings = bat.length;
    const runs = bat.reduce((s,r) => s + (r.Runs||0), 0);
    const balls = bat.reduce((s,r) => s + (r.Balls||0), 0);
    const outs = bat.filter(r => String(r.Out||'').toLowerCase() === 'yes').length;
    const fours = df.reduce((s,r) => s + (r['4s']||0), 0);
    const sixes = df.reduce((s,r) => s + (r['6s']||0), 0);
    const catches = df.reduce((s,r) => s + (r.Catch||0), 0);
    const average = outs > 0 ? runs/outs : 0;
    const sr = balls > 0 ? (runs/balls)*100 : 0;

    let highest = 0, highestNotOut = false;
    if (innings > 0) {{
      const max = Math.max(...bat.map(r => r.Runs||0));
      highest = max;
      highestNotOut = bat.some(r => r.Runs === max && String(r.Out||'').toLowerCase() !== 'yes');
    }}

    const thirties = bat.filter(r => r.Runs >= 30 && r.Runs < 50).length;
    const fifties  = bat.filter(r => r.Runs >= 50 && r.Runs < 100).length;
    const hundreds = bat.filter(r => r.Runs >= 100).length;

    const dismMap = {{}};
    bat.forEach(r => {{
      if (r.Dismissal && String(r.Out||'').toLowerCase() === 'yes') {{
        dismMap[r.Dismissal] = (dismMap[r.Dismissal]||0) + 1;
      }}
    }});

    return {{
      matches, innings, runs, balls, outs, fours, sixes, catches,
      average, sr, highest, highestNotOut,
      thirties, fifties, hundreds, dismissals: dismMap,
      highestDisplay: innings ? `${{highest}}${{highestNotOut?'*':''}}` : '—',
    }};
  }}

  function computeBowling(df) {{
    const bowl = df.filter(r => r.Overs != null);
    const innings = bowl.length;
    const balls = bowl.reduce((s,r) => s + oversToBalls(r.Overs), 0);
    const overs = ballsToOvers(balls);
    const runs = bowl.reduce((s,r) => s + (r.Runs_Conceded||0), 0);
    const wickets = bowl.reduce((s,r) => s + (r.Wickets||0), 0);
    const maidens = bowl.reduce((s,r) => s + (r.Maidens||0), 0);
    const economy = balls > 0 ? runs / (balls/6) : 0;
    const average = wickets > 0 ? runs / wickets : 0;
    const sr = wickets > 0 ? balls / wickets : 0;

    let bestW = 0, bestR = Infinity;
    bowl.forEach(r => {{
      const w = r.Wickets||0, c = r.Runs_Conceded||0;
      if (w > bestW || (w === bestW && c < bestR)) {{ bestW = w; bestR = c; }}
    }});
    const best = innings ? `${{bestW}}/${{bestR === Infinity ? 0 : bestR}}` : '—';

    const threeW = bowl.filter(r => (r.Wickets||0) >= 3).length;
    const fiveW  = bowl.filter(r => (r.Wickets||0) >= 5).length;

    return {{ innings, balls, overs, runs, wickets, maidens, economy, average, sr, best, threeW, fiveW }};
  }}

  function animateCount(el, to, decimals=0, duration=900) {{
    if (!el) return;
    const from = 0;
    const start = performance.now();
    const ease = t => 1 - Math.pow(1-t, 3);
    function tick(now) {{
      const t = Math.min(1, (now-start)/duration);
      const v = from + (to-from)*ease(t);
      el.textContent = decimals === 0 ? Math.round(v).toLocaleString() : v.toFixed(decimals);
      if (t < 1) requestAnimationFrame(tick);
      else el.textContent = decimals === 0 ? Math.round(to).toLocaleString() : to.toFixed(decimals);
    }}
    requestAnimationFrame(tick);
  }}

  function renderHero(df, bat, bowl) {{
    animateCount($('#kpi-matches'), df.length);
    animateCount($('#kpi-runs'),    bat.runs);
    animateCount($('#kpi-wickets'), bowl.wickets);
    animateCount($('#kpi-catches'), bat.catches);

    const recent = [...df].slice(-5);
    const pillsEl = $('#recentFormPills');
    pillsEl.innerHTML = '';
    if (!recent.length) {{
      pillsEl.innerHTML = '<span class="text-xs text-slate-500">No matches</span>';
    }} else {{
      recent.forEach(r => {{
        let label = '–', bg = 'rgba(255,255,255,.06)', color = '#94a3b8';
        if (r.Runs != null && r.Runs >= 30) {{ label = r.Runs; bg = 'rgba(34,211,238,.18)'; color = '#a5f3fc'; }}
        else if (r.Wickets != null && r.Wickets >= 3) {{ label = `${{r.Wickets}}W`; bg = 'rgba(245,158,11,.18)'; color = '#fde68a'; }}
        else if (r.Runs != null && r.Runs > 0) {{ label = r.Runs; bg = 'rgba(255,255,255,.05)'; color = '#cbd5e1'; }}
        else if (r.Wickets != null && r.Wickets >= 1) {{ label = `${{r.Wickets}}w`; bg = 'rgba(255,255,255,.05)'; color = '#cbd5e1'; }}
        else if (r.Runs === 0) {{ label = '0'; bg = 'rgba(244,63,94,.15)'; color = '#fb7185'; }}

        const pill = document.createElement('div');
        pill.className = 'form-pill';
        pill.style.background = bg;
        pill.style.color = color;
        pill.textContent = label;
        pill.title = `vs ${{r.Opponent}} (${{r.Year}})`;
        pillsEl.appendChild(pill);
      }});
    }}

    const last5 = recent;
    const r5 = last5.reduce((s,r) => s + (r.Runs||0), 0);
    const w5 = last5.reduce((s,r) => s + (r.Wickets||0), 0);
    $('#recentFormSummary').textContent = last5.length
      ? `${{r5}} runs · ${{w5}} wickets in last ${{last5.length}}`
      : '';
  }}

  function renderFormatGrid(df) {{
    const grid = $('#formatGrid');
    grid.innerHTML = '';
    const types = [...new Set(df.map(r => r.Match_Type).filter(Boolean))].sort();
    if (!types.length) {{
      grid.innerHTML = '<div class="empty col-span-full">No formats match the current filters.</div>';
      return;
    }}
    types.forEach((t, i) => {{
      const sub = df.filter(r => r.Match_Type === t);
      const b = computeBatting(sub);
      const bo = computeBowling(sub);
      const card = document.createElement('div');
      card.className = 'glass stat-card p-5 sm:p-6 reveal';
      card.style.animationDelay = `${{i*70}}ms`;
      card.innerHTML = `
        <div class="flex items-center justify-between mb-3">
          <h3 class="text-base font-semibold">${{t}}</h3>
          <span class="text-[11px] uppercase tracking-[0.15em] text-slate-400">${{sub.length}} match${{sub.length===1?'':'es'}}</span>
        </div>
        <div class="grid grid-cols-3 gap-3">
          <div>
            <div class="text-[11px] uppercase tracking-[0.1em] text-slate-400">Runs</div>
            <div class="num-display num text-2xl text-bat-400 mt-0.5">${{fmt(b.runs)}}</div>
          </div>
          <div>
            <div class="text-[11px] uppercase tracking-[0.1em] text-slate-400">Wkts</div>
            <div class="num-display num text-2xl text-bowl-400 mt-0.5">${{fmt(bo.wickets)}}</div>
          </div>
          <div>
            <div class="text-[11px] uppercase tracking-[0.1em] text-slate-400">HS / Best</div>
            <div class="num-display num text-2xl text-white mt-0.5 truncate" title="HS ${{b.highestDisplay}} · Best ${{bo.best}}">${{b.highestDisplay}}</div>
          </div>
        </div>
        <div class="hr-soft my-4"></div>
        <div class="grid grid-cols-3 gap-3 text-xs text-slate-300">
          <div><span class="text-slate-500">Avg</span><br><span class="num">${{b.average ? fmt(b.average,1) : '—'}}</span></div>
          <div><span class="text-slate-500">SR</span><br><span class="num">${{b.sr ? fmt(b.sr,1) : '—'}}</span></div>
          <div><span class="text-slate-500">Econ</span><br><span class="num">${{bo.economy ? fmt(bo.economy,2) : '—'}}</span></div>
        </div>
      `;
      grid.appendChild(card);
    }});
  }}

  function miniStat(label, value, color='text-white') {{
    return `
      <div class="glass stat-card p-3">
        <div class="text-[10px] uppercase tracking-[0.1em] text-slate-400">${{label}}</div>
        <div class="num-display num text-2xl mt-1 ${{color}}">${{value}}</div>
      </div>`;
  }}

  function renderOverviewMini(bat, bowl) {{
    $('#overviewBattingMini').innerHTML =
      miniStat('Innings', fmt(bat.innings), 'text-white') +
      miniStat('Average', bat.average ? fmt(bat.average,2) : '—', 'text-bat-400') +
      miniStat('Strike rate', bat.sr ? fmt(bat.sr,1) : '—', 'text-bat-400');

    $('#overviewBowlingMini').innerHTML =
      miniStat('Innings', fmt(bowl.innings), 'text-white') +
      miniStat('Average', bowl.average ? fmt(bowl.average,2) : '—', 'text-bowl-400') +
      miniStat('Economy', bowl.economy ? fmt(bowl.economy,2) : '—', 'text-bowl-400');
  }}

  function renderMilestones(df, bat, bowl) {{
    const grid = $('#milestonesGrid');
    grid.innerHTML = '';
    const items = [
      {{ label:'Hundreds', value: bat.hundreds, sub:'100+ scores', icon:'crown', color:'bat' }},
      {{ label:'Fifties',  value: bat.fifties,  sub:'50–99 scores', icon:'star', color:'bat' }},
      {{ label:'Thirties', value: bat.thirties, sub:'30–49 scores', icon:'award', color:'bat' }},
      {{ label:'Highest',  value: bat.highestDisplay, sub:'Top knock', icon:'flame', color:'bat' }},
      {{ label:'5W hauls', value: bowl.fiveW, sub:'5+ wickets', icon:'flame', color:'bowl' }},
      {{ label:'3W hauls', value: bowl.threeW, sub:'3+ wickets', icon:'zap', color:'bowl' }},
      {{ label:'Best fig.', value: bowl.best, sub:'Best bowling', icon:'crown', color:'bowl' }},
      {{ label:'Maidens',  value: bowl.maidens, sub:'Total maidens', icon:'target', color:'bowl' }},
    ];
    items.forEach((it,i) => {{
      const colorMap = {{
        bat:  {{ ring:'rgba(34,211,238,.25)',  num:'text-bat-400' }},
        bowl: {{ ring:'rgba(245,158,11,.25)',  num:'text-bowl-400' }},
      }};
      const c = colorMap[it.color];
      const el = document.createElement('div');
      el.className = `glass stat-card ${{it.color === 'bowl' ? 'stat-card--bowl' : ''}} p-4 sm:p-5 reveal`;
      el.style.animationDelay = `${{i*40}}ms`;
      el.innerHTML = `
        <div class="flex items-center gap-2 text-slate-400 text-[11px] uppercase tracking-[0.1em]">
          <i data-lucide="${{it.icon}}" class="w-3.5 h-3.5"></i>${{it.label}}
        </div>
        <div class="num-display num text-3xl sm:text-4xl mt-1 ${{c.num}}">${{it.value}}</div>
        <div class="text-xs text-slate-500 mt-1">${{it.sub}}</div>
      `;
      grid.appendChild(el);
    }});
    lucide.createIcons();
  }}

  function renderBattingTab(df, bat) {{
    const grid = $('#battingStatGrid');
    grid.innerHTML = '';
    const cells = [
      ['Matches',     fmt(bat.matches)],
      ['Innings',     fmt(bat.innings)],
      ['Runs',        fmt(bat.runs),      'text-bat-400'],
      ['Balls',       fmt(bat.balls)],
      ['Average',     bat.average ? fmt(bat.average,2) : '—', 'text-bat-400'],
      ['Strike rate', bat.sr ? fmt(bat.sr,1) : '—',           'text-bat-400'],
      ['Highest',     bat.highestDisplay,'text-white'],
      ['100s',        fmt(bat.hundreds)],
      ['50s',         fmt(bat.fifties)],
      ['30+',         fmt(bat.thirties)],
      ['4s',          fmt(bat.fours)],
      ['6s',          fmt(bat.sixes)],
    ];
    cells.forEach(([label, val, color], i) => {{
      const card = document.createElement('div');
      card.className = 'glass stat-card p-4 sm:p-5 reveal';
      card.style.animationDelay = `${{i*30}}ms`;
      card.innerHTML = `
        <div class="text-[11px] uppercase tracking-[0.1em] text-slate-400">${{label}}</div>
        <div class="num-display num text-3xl sm:text-4xl mt-1.5 ${{color||'text-white'}}">${{val}}</div>
      `;
      grid.appendChild(card);
    }});

    const knocks = df
      .filter(r => r.Runs != null && r.Runs >= 30)
      .sort((a,b) => (b.Runs||0) - (a.Runs||0));
    const list = $('#bestKnocksList');
    list.innerHTML = '';
    if (!knocks.length) {{
      list.innerHTML = '<div class="empty">No 30+ scores yet — chip away.</div>';
    }} else {{
      knocks.slice(0,12).forEach(r => {{
        const sr = r.Balls ? ((r.Runs/r.Balls)*100).toFixed(1) : '—';
        const isHundred = r.Runs >= 100;
        const isFifty   = r.Runs >= 50 && r.Runs < 100;
        const badge = isHundred ? '<span class="badge badge-100">100</span>'
                    : isFifty   ? '<span class="badge badge-50">50</span>'
                    : '<span class="badge">30+</span>';
        const out = String(r.Out||'').toLowerCase() === 'yes' ? r.Dismissal||'Out' : 'Not out';
        const item = document.createElement('div');
        item.className = 'flex items-center justify-between gap-3 p-3 rounded-xl border border-white/5 hover:border-white/10 hover:bg-white/[.02] transition';
        item.innerHTML = `
          <div class="min-w-0 flex items-center gap-3">
            <div class="num-display num text-2xl sm:text-3xl text-bat-400 min-w-[60px]">${{r.Runs}}${{out==='Not out'?'<span class=\\"text-bat-200\\">*</span>':''}}</div>
            <div class="min-w-0">
              <div class="text-sm font-medium truncate">vs ${{r.Opponent || 'Unknown'}}</div>
              <div class="text-xs text-slate-400 truncate">${{r.Match_Type||'—'}} · ${{r.Year||''}} · ${{r.Balls||0}} balls · SR ${{sr}} · ${{out}}</div>
            </div>
          </div>
          ${{badge}}
        `;
        list.appendChild(item);
      }});
    }}
  }}

  function renderBowlingTab(df, bowl) {{
    const grid = $('#bowlingStatGrid');
    grid.innerHTML = '';
    const cells = [
      ['Innings',     fmt(bowl.innings)],
      ['Overs',       bowl.overs || '—'],
      ['Wickets',     fmt(bowl.wickets), 'text-bowl-400'],
      ['Maidens',     fmt(bowl.maidens)],
      ['Average',     bowl.average ? fmt(bowl.average,2) : '—', 'text-bowl-400'],
      ['Economy',     bowl.economy ? fmt(bowl.economy,2) : '—', 'text-bowl-400'],
      ['Strike rate', bowl.sr ? fmt(bowl.sr,1) : '—'],
      ['Best',        bowl.best, 'text-white'],
      ['5W',          fmt(bowl.fiveW)],
      ['3W',          fmt(bowl.threeW)],
      ['Runs given',  fmt(bowl.runs)],
      ['Balls',       fmt(bowl.balls)],
    ];
    cells.forEach(([label, val, color], i) => {{
      const card = document.createElement('div');
      card.className = 'glass stat-card stat-card--bowl p-4 sm:p-5 reveal';
      card.style.animationDelay = `${{i*30}}ms`;
      card.innerHTML = `
        <div class="text-[11px] uppercase tracking-[0.1em] text-slate-400">${{label}}</div>
        <div class="num-display num text-3xl sm:text-4xl mt-1.5 ${{color||'text-white'}}">${{val}}</div>
      `;
      grid.appendChild(card);
    }});

    const spells = df
      .filter(r => r.Overs != null && (r.Wickets||0) >= 3)
      .sort((a,b) => (b.Wickets-a.Wickets) || ((a.Runs_Conceded||0)-(b.Runs_Conceded||0)));
    const list = $('#bestSpellsList');
    list.innerHTML = '';
    if (!spells.length) {{
      list.innerHTML = '<div class="empty">No 3+ wicket spells yet.</div>';
    }} else {{
      spells.slice(0,15).forEach(r => {{
        const isFive = (r.Wickets||0) >= 5;
        const badge = isFive ? '<span class="badge badge-5w">5W</span>' : '<span class="badge badge-3w">3W</span>';
        const econ = r.Overs ? ((r.Runs_Conceded||0) / (oversToBalls(r.Overs)/6)).toFixed(2) : '—';
        const item = document.createElement('div');
        item.className = 'flex items-center justify-between gap-3 p-3 rounded-xl border border-white/5 hover:border-white/10 hover:bg-white/[.02] transition';
        item.innerHTML = `
          <div class="min-w-0 flex items-center gap-3">
            <div class="num-display num text-2xl sm:text-3xl text-bowl-400 min-w-[80px] whitespace-nowrap">${{r.Wickets||0}}/${{r.Runs_Conceded||0}}</div>
            <div class="min-w-0">
              <div class="text-sm font-medium truncate">vs ${{r.Opponent||'Unknown'}}</div>
              <div class="text-xs text-slate-400 truncate">${{r.Match_Type||'—'}} · ${{r.Year||''}} · ${{r.Overs||0}} overs · econ ${{econ}}</div>
            </div>
          </div>
          ${{badge}}
        `;
        list.appendChild(item);
      }});
    }}
  }}

  const chartColors = {{
    bat:    '#22d3ee',
    bowl:   '#f59e0b',
    bat2:   '#0891b2',
    bowl2:  '#d97706',
    grid:   'rgba(255,255,255,.06)',
    tick:   'rgba(226,232,240,.7)',
    label:  'rgba(226,232,240,.85)',
  }};

  function gradientFill(ctx, area, hex) {{
    if (!area) return hex+'40';
    const g = ctx.createLinearGradient(0, area.top, 0, area.bottom);
    g.addColorStop(0, hex+'66');
    g.addColorStop(1, hex+'00');
    return g;
  }}

  const baseLineOpts = (color, label) => ({{
    type: 'line',
    options: {{
      responsive: true, maintainAspectRatio: false,
      animation: {{ duration: 700, easing: 'easeOutCubic' }},
      interaction: {{ mode: 'index', intersect: false }},
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          backgroundColor: 'rgba(10,14,26,.95)', borderColor: 'rgba(255,255,255,.1)', borderWidth: 1,
          titleColor: '#fff', bodyColor: '#cbd5e1', padding: 12, cornerRadius: 10,
          displayColors: false,
          callbacks: {{ title: items => `Match ${{items[0].label}}` }}
        }}
      }},
      scales: {{
        x: {{ grid: {{ color: chartColors.grid, drawBorder:false }}, ticks: {{ color: chartColors.tick, font:{{ size: 10 }} }} }},
        y: {{ grid: {{ color: chartColors.grid, drawBorder:false }}, ticks: {{ color: chartColors.tick, font:{{ size: 10 }} }}, beginAtZero: true }}
      }}
    }},
    data: {{
      labels: [],
      datasets: [{{
        label, data: [], borderColor: color, borderWidth: 2.5,
        pointRadius: 3, pointHoverRadius: 6, pointBackgroundColor: color, pointBorderColor: '#0a0e1a',
        tension: 0.35, fill: true,
        backgroundColor: function(context) {{
          const {{ ctx, chartArea }} = context.chart;
          return gradientFill(ctx, chartArea, color);
        }}
      }}]
    }}
  }});

  const baseBarOpts = (color) => ({{
    type: 'bar',
    options: {{
      responsive: true, maintainAspectRatio: false,
      animation: {{ duration: 700 }},
      plugins: {{
        legend: {{ display: false }},
        tooltip: {{
          backgroundColor: 'rgba(10,14,26,.95)', borderColor: 'rgba(255,255,255,.1)', borderWidth: 1,
          titleColor: '#fff', bodyColor: '#cbd5e1', padding: 12, cornerRadius: 10, displayColors: false,
        }}
      }},
      scales: {{
        x: {{ grid: {{ display: false }}, ticks: {{ color: chartColors.tick, font:{{ size: 10 }} }} }},
        y: {{ grid: {{ color: chartColors.grid, drawBorder:false }}, ticks: {{ color: chartColors.tick, font:{{ size: 10 }} }}, beginAtZero: true }}
      }}
    }},
    data: {{ labels: [], datasets: [{{ data: [], backgroundColor: color, borderRadius: 6, borderSkipped: false, maxBarThickness: 28 }}] }}
  }});

  const charts = {{}};

  function destroyCharts() {{
    Object.values(charts).forEach(c => c && c.destroy());
    Object.keys(charts).forEach(k => delete charts[k]);
  }}

  function renderCharts(df) {{
    destroyCharts();
    state._lastDf = df;
    renderOverviewCharts(df);
    if (state.tab === 'batting') renderBattingChartsOnly(df);
    if (state.tab === 'bowling') renderBowlingChartsOnly(df);
  }}

  function renderOverviewCharts(df) {{
    const ordered = [...df].sort((a,b) => (a.Year-b.Year) || (a.matchId-b.matchId));
    const yrs = [...new Set(ordered.map(r => r.Year))].sort();
    const yearMap = {{}}, wktYearMap = {{}};
    ordered.forEach(r => {{
      if (r.Runs != null) yearMap[r.Year] = (yearMap[r.Year]||0) + (r.Runs||0);
      if (r.Overs != null) wktYearMap[r.Year] = (wktYearMap[r.Year]||0) + (r.Wickets||0);
    }});

    if (charts.runsYear) charts.runsYear.destroy();
    const runsYearCfg = baseBarOpts(chartColors.bat);
    runsYearCfg.data.labels = yrs;
    runsYearCfg.data.datasets[0].data = yrs.map(y => yearMap[y]||0);
    charts.runsYear = new Chart($('#chart-runs-year'), runsYearCfg);

    if (charts.wktsYear) charts.wktsYear.destroy();
    const wktsYearCfg = baseBarOpts(chartColors.bowl);
    wktsYearCfg.data.labels = yrs;
    wktsYearCfg.data.datasets[0].data = yrs.map(y => wktYearMap[y]||0);
    charts.wktsYear = new Chart($('#chart-wickets-year'), wktsYearCfg);
  }}

  function renderBattingChartsOnly(df) {{
    const ordered = [...df].sort((a,b) => (a.Year-b.Year) || (a.matchId-b.matchId));
    const bat = ordered.filter(r => r.Runs != null);
    let cumRuns = 0, cumOuts = 0, cumBalls = 0;
    const labels = [], avg = [], sr = [], runsArr = [];
    bat.forEach((r, i) => {{
      cumRuns += (r.Runs||0);
      cumBalls += (r.Balls||0);
      if (String(r.Out||'').toLowerCase() === 'yes') cumOuts++;
      labels.push(String(i+1));
      avg.push(cumOuts ? +(cumRuns/cumOuts).toFixed(2) : cumRuns);
      sr.push(cumBalls ? +((cumRuns/cumBalls)*100).toFixed(2) : 0);
      runsArr.push(r.Runs||0);
    }});

    if (charts.batAvg) charts.batAvg.destroy();
    const avgCfg = baseLineOpts(chartColors.bat, 'Average');
    avgCfg.data.labels = labels; avgCfg.data.datasets[0].data = avg;
    avgCfg.options.plugins.tooltip.callbacks.label = c => `Avg: ${{c.parsed.y.toFixed(2)}}`;
    charts.batAvg = new Chart($('#chart-bat-avg'), avgCfg);

    if (charts.batSR) charts.batSR.destroy();
    const srCfg = baseLineOpts(chartColors.bat2, 'Strike rate');
    srCfg.data.labels = labels; srCfg.data.datasets[0].data = sr;
    srCfg.options.plugins.tooltip.callbacks.label = c => `SR: ${{c.parsed.y.toFixed(1)}}`;
    charts.batSR = new Chart($('#chart-bat-sr'), srCfg);

    if (charts.batPI) charts.batPI.destroy();
    const max = Math.max(...runsArr, 0);
    const perInnCfg = baseBarOpts(chartColors.bat);
    perInnCfg.data.labels = labels;
    perInnCfg.data.datasets[0].data = runsArr;
    perInnCfg.data.datasets[0].backgroundColor = runsArr.map(v => v === max && max > 0 ? '#22d3ee' : 'rgba(34,211,238,.45)');
    perInnCfg.options.plugins.tooltip.callbacks = {{
      title: items => `Innings ${{items[0].label}}`,
      label: c => {{
        const r = bat[c.dataIndex];
        return [`${{c.parsed.y}} runs vs ${{r.Opponent||'?'}}`, `${{r.Year||''}} · ${{r.Match_Type||''}}`];
      }}
    }};
    charts.batPI = new Chart($('#chart-bat-perInnings'), perInnCfg);

    const batStats = computeBatting(df);
    renderDismissalsDonut(batStats);
  }}

  function renderBowlingChartsOnly(df) {{
    const ordered = [...df].sort((a,b) => (a.Year-b.Year) || (a.matchId-b.matchId));
    const bowl = ordered.filter(r => r.Overs != null);
    let cR = 0, cW = 0, cB = 0;
    const blabels = [], bavg = [], econ = [], wkts = [];
    bowl.forEach((r, i) => {{
      cR += (r.Runs_Conceded||0);
      cW += (r.Wickets||0);
      cB += oversToBalls(r.Overs);
      blabels.push(String(i+1));
      bavg.push(cW ? +(cR/cW).toFixed(2) : 0);
      econ.push(cB ? +(cR / (cB/6)).toFixed(2) : 0);
      wkts.push(r.Wickets||0);
    }});

    if (charts.bowlAvg) charts.bowlAvg.destroy();
    const bAvgCfg = baseLineOpts(chartColors.bowl, 'Bowling avg');
    bAvgCfg.data.labels = blabels; bAvgCfg.data.datasets[0].data = bavg;
    bAvgCfg.options.plugins.tooltip.callbacks.label = c => `Avg: ${{c.parsed.y.toFixed(2)}}`;
    charts.bowlAvg = new Chart($('#chart-bowl-avg'), bAvgCfg);

    if (charts.bowlEcon) charts.bowlEcon.destroy();
    const econCfg = baseLineOpts(chartColors.bowl2, 'Economy');
    econCfg.data.labels = blabels; econCfg.data.datasets[0].data = econ;
    econCfg.options.plugins.tooltip.callbacks.label = c => `Econ: ${{c.parsed.y.toFixed(2)}}`;
    charts.bowlEcon = new Chart($('#chart-bowl-econ'), econCfg);

    if (charts.bowlPI) charts.bowlPI.destroy();
    const wpiCfg = baseBarOpts(chartColors.bowl);
    wpiCfg.data.labels = blabels;
    wpiCfg.data.datasets[0].data = wkts;
    wpiCfg.data.datasets[0].backgroundColor = wkts.map(v => v >= 5 ? '#fb923c' : v >= 3 ? '#f59e0b' : 'rgba(245,158,11,.45)');
    wpiCfg.options.plugins.tooltip.callbacks = {{
      title: items => `Innings ${{items[0].label}}`,
      label: c => {{
        const r = bowl[c.dataIndex];
        return [`${{c.parsed.y}} wkts · ${{r.Runs_Conceded||0}} runs in ${{r.Overs||0}} ov`, `vs ${{r.Opponent||'?'}} · ${{r.Year||''}}`];
      }}
    }};
    charts.bowlPI = new Chart($('#chart-bowl-perInnings'), wpiCfg);
  }}

  function renderDismissalsDonut(bat) {{
    if (charts.donut) charts.donut.destroy();
    const data = bat.dismissals;
    const labels = Object.keys(data);
    const values = labels.map(k => data[k]);
    const total = values.reduce((a,b) => a+b, 0);
    $('#dismissTotal').textContent = total;

    const palette = ['#22d3ee', '#f59e0b', '#34d399', '#a78bfa', '#fb7185', '#60a5fa', '#fde68a', '#fb923c'];
    const colors = labels.map((_,i) => palette[i % palette.length]);

    if (!labels.length) {{
      $('#dismissLegend').innerHTML = '<div class="empty col-span-2">No dismissals to chart.</div>';
      charts.donut = new Chart($('#chart-dismissals'), {{
        type: 'doughnut',
        data: {{ labels: ['No data'], datasets: [{{ data: [1], backgroundColor: ['rgba(255,255,255,.06)'], borderWidth: 0 }}] }},
        options: {{ responsive: true, maintainAspectRatio: false, cutout: '70%', plugins: {{ legend: {{ display: false }}, tooltip: {{ enabled: false }} }} }}
      }});
      return;
    }}

    charts.donut = new Chart($('#chart-dismissals'), {{
      type: 'doughnut',
      data: {{ labels, datasets: [{{ data: values, backgroundColor: colors, borderWidth: 0, hoverOffset: 8 }}] }},
      options: {{
        responsive: true, maintainAspectRatio: false,
        cutout: '72%',
        animation: {{ animateRotate: true, duration: 800 }},
        plugins: {{
          legend: {{ display: false }},
          tooltip: {{
            backgroundColor: 'rgba(10,14,26,.95)', borderColor: 'rgba(255,255,255,.1)', borderWidth: 1,
            titleColor: '#fff', bodyColor: '#cbd5e1', padding: 12, cornerRadius: 10,
            callbacks: {{
              label: c => `${{c.label}}: ${{c.parsed}} (${{((c.parsed/total)*100).toFixed(0)}}%)`
            }}
          }}
        }}
      }}
    }});

    const legend = $('#dismissLegend');
    legend.innerHTML = '';
    labels.forEach((lab, i) => {{
      const pct = ((values[i]/total)*100).toFixed(0);
      const el = document.createElement('div');
      el.className = 'flex items-center justify-between gap-2 text-xs p-2 rounded-lg bg-white/[.02] border border-white/5';
      el.innerHTML = `
        <div class="flex items-center gap-2 min-w-0">
          <span class="w-2.5 h-2.5 rounded-full shrink-0" style="background:${{colors[i]}}"></span>
          <span class="truncate">${{lab}}</span>
        </div>
        <div class="text-slate-400 shrink-0"><span class="num text-white">${{values[i]}}</span> · ${{pct}}%</div>
      `;
      legend.appendChild(el);
    }});
  }}

  function renderMatchesTab(df) {{
    const tbody = $('#matchTableBody');
    const cardList = $('#matchCardList');
    const empty = $('#matchEmpty');
    tbody.innerHTML = '';
    cardList.innerHTML = '';

    let rows = [...df];
    if (state.matchSearch) {{
      const q = state.matchSearch.toLowerCase();
      rows = rows.filter(r => (r.Opponent||'').toLowerCase().includes(q));
    }}

    const {{ key, dir }} = state.matchSort;
    rows.sort((a,b) => {{
      let av = a[key], bv = b[key];
      if (av == null && bv == null) return 0;
      if (av == null) return 1;
      if (bv == null) return -1;
      if (typeof av === 'number' && typeof bv === 'number') return dir === 'asc' ? av-bv : bv-av;
      return dir === 'asc' ? String(av).localeCompare(String(bv)) : String(bv).localeCompare(String(av));
    }});

    if (!rows.length) empty.classList.remove('hidden'); else empty.classList.add('hidden');

    rows.forEach(r => {{
      const out = String(r.Out||'').toLowerCase() === 'yes';
      const batCell = r.Runs != null
        ? `<span class="num text-bat-400 font-semibold">${{r.Runs}}${{out ? '' : '<span class=\\"text-bat-200\\">*</span>'}}</span><span class="text-slate-500"> (${{r.Balls||0}})</span>`
        : '<span class="text-slate-600">—</span>';
      const dismissCell = r.Runs != null ? (out ? (r.Dismissal||'Out') : 'Not out') : '<span class="text-slate-600">—</span>';
      const bowlCell = r.Overs != null
        ? `<span class="num text-bowl-400 font-semibold">${{r.Wickets||0}}/${{r.Runs_Conceded||0}}</span><span class="text-slate-500"> (${{r.Overs}})</span>`
        : '<span class="text-slate-600">—</span>';

      const notes = [];
      if ((r.Runs||0) >= 100) notes.push('<span class="badge badge-100">100</span>');
      else if ((r.Runs||0) >= 50) notes.push('<span class="badge badge-50">50</span>');
      else if ((r.Runs||0) >= 30) notes.push('<span class="badge">30+</span>');
      if ((r.Wickets||0) >= 5) notes.push('<span class="badge badge-5w">5W</span>');
      else if ((r.Wickets||0) >= 3) notes.push('<span class="badge badge-3w">3W</span>');
      if ((r.Catch||0) > 0) notes.push(`<span class="badge">+${{r.Catch}} ct</span>`);

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="text-slate-500 num">${{r.matchId}}</td>
        <td class="num">${{r.Year||''}}</td>
        <td><span class="badge">${{r.Match_Type||'—'}}</span></td>
        <td class="text-slate-200">${{r.Opponent||''}}</td>
        <td class="text-right">${{batCell}}</td>
        <td class="text-slate-300 text-xs">${{dismissCell}}</td>
        <td class="text-right">${{bowlCell}}</td>
        <td class="text-right space-x-1">${{notes.join(' ')||''}}</td>
      `;
      tbody.appendChild(tr);

      const card = document.createElement('div');
      card.className = 'p-4 hover:bg-white/[.02] transition';
      card.innerHTML = `
        <div class="flex items-start justify-between gap-3">
          <div class="min-w-0">
            <div class="text-sm font-medium truncate">vs ${{r.Opponent||'Unknown'}}</div>
            <div class="text-xs text-slate-400 mt-0.5">#${{r.matchId}} · ${{r.Year||''}} · ${{r.Match_Type||'—'}}</div>
          </div>
          <div class="flex flex-col items-end gap-1">${{notes.join(' ')||''}}</div>
        </div>
        <div class="grid grid-cols-2 gap-3 mt-3 text-sm">
          <div class="rounded-lg border border-white/5 p-2.5">
            <div class="text-[10px] uppercase tracking-[0.1em] text-slate-500">Bat</div>
            <div class="mt-0.5">${{batCell}}</div>
            <div class="text-[11px] text-slate-500 mt-0.5 truncate">${{dismissCell}}</div>
          </div>
          <div class="rounded-lg border border-white/5 p-2.5">
            <div class="text-[10px] uppercase tracking-[0.1em] text-slate-500">Bowl</div>
            <div class="mt-0.5">${{bowlCell}}</div>
            <div class="text-[11px] text-slate-500 mt-0.5">${{r.Maidens||0}} maidens</div>
          </div>
        </div>
      `;
      cardList.appendChild(card);
    }});
  }}

  function renderFilterDrawerUI() {{
    const yEl = $('#yearFilters');
    yEl.innerHTML = '';
    allYears.forEach(y => {{
      const el = document.createElement('button');
      el.className = 'chip';
      el.dataset.active = state.years.has(y);
      el.dataset.color = 'bat';
      el.innerHTML = `<i data-lucide="${{state.years.has(y)?'check':'plus'}}" class="w-3 h-3"></i>${{y}}`;
      el.onclick = () => {{
        if (state.years.has(y)) state.years.delete(y); else state.years.add(y);
        renderFilterDrawerUI(); rerender();
      }};
      yEl.appendChild(el);
    }});

    const tEl = $('#typeFilters');
    tEl.innerHTML = '';
    allTypes.forEach(t => {{
      const el = document.createElement('button');
      el.className = 'chip';
      el.dataset.active = state.types.has(t);
      el.dataset.color = 'bowl';
      el.innerHTML = `<i data-lucide="${{state.types.has(t)?'check':'plus'}}" class="w-3 h-3"></i>${{t}}`;
      el.onclick = () => {{
        if (state.types.has(t)) state.types.delete(t); else state.types.add(t);
        renderFilterDrawerUI(); rerender();
      }};
      tEl.appendChild(el);
    }});

    const oEl = $('#opponentFilters');
    oEl.innerHTML = '';
    const q = ($('#opponentSearch').value || '').toLowerCase();
    const list = allOpps.filter(o => !q || o.toLowerCase().includes(q));
    if (!list.length) {{
      oEl.innerHTML = '<span class="text-xs text-slate-500">No teams match.</span>';
    }}
    list.forEach(o => {{
      const el = document.createElement('button');
      el.className = 'chip';
      el.dataset.active = state.opps.has(o);
      el.dataset.color = 'mint';
      el.innerHTML = `<i data-lucide="${{state.opps.has(o)?'check':'plus'}}" class="w-3 h-3"></i>${{o}}`;
      el.onclick = () => {{
        if (state.opps.has(o)) state.opps.delete(o); else state.opps.add(o);
        renderFilterDrawerUI(); rerender();
      }};
      oEl.appendChild(el);
    }});

    lucide.createIcons();
  }}

  function renderActiveFilters() {{
    const bar = $('#activeFiltersBar');
    const chips = $('#activeFiltersChips');
    chips.innerHTML = '';

    const yearMissing = allYears.filter(y => !state.years.has(y));
    const typeMissing = allTypes.filter(t => !state.types.has(t));
    const opps = [...state.opps];

    if (yearMissing.length) {{
      const yearsSelected = allYears.filter(y => state.years.has(y));
      yearsSelected.forEach(y => addActiveChip(`Year: ${{y}}`, () => {{ state.years.delete(y); renderFilterDrawerUI(); rerender(); }}, 'bat'));
    }}
    if (typeMissing.length) {{
      const typesSelected = allTypes.filter(t => state.types.has(t));
      typesSelected.forEach(t => addActiveChip(`Format: ${{t}}`, () => {{ state.types.delete(t); renderFilterDrawerUI(); rerender(); }}, 'bowl'));
    }}
    opps.forEach(o => addActiveChip(`vs ${{o}}`, () => {{ state.opps.delete(o); renderFilterDrawerUI(); rerender(); }}, 'mint'));

    function addActiveChip(label, onClose, color) {{
      const c = document.createElement('span');
      c.className = 'chip';
      c.dataset.active = 'true';
      c.dataset.color = color;
      c.innerHTML = `${{label}}<i data-lucide="x" class="w-3 h-3 ml-1"></i>`;
      c.onclick = onClose;
      chips.appendChild(c);
    }}

    if (chips.children.length === 0) {{
      bar.classList.add('hidden');
      $('#activeFilterCount').classList.add('hidden');
    }} else {{
      bar.classList.remove('hidden');
      $('#activeFilterCount').classList.remove('hidden');
      $('#activeFilterCount').textContent = chips.children.length;
    }}

    lucide.createIcons();
  }}

  function switchTab(name) {{
    state.tab = name;
    $$('[data-tab-pane]').forEach(p => p.classList.toggle('hidden', p.dataset.tabPane !== name));
    $$('[data-tab]').forEach(b => b.dataset.active = String(b.dataset.tab === name));
    requestAnimationFrame(() => {{
      const df = state._lastDf || getFiltered();
      if (name === 'batting') renderBattingChartsOnly(df);
      if (name === 'bowling') renderBowlingChartsOnly(df);
      Object.values(charts).forEach(c => {{ if (c) {{ c.resize(); }} }});
    }});
    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }}

  function rerender() {{
    const df  = getFiltered();
    const bat = computeBatting(df);
    const bowl = computeBowling(df);

    renderHero(df, bat, bowl);
    renderFormatGrid(df);
    renderOverviewMini(bat, bowl);
    renderMilestones(df, bat, bowl);
    renderBattingTab(df, bat);
    renderBowlingTab(df, bowl);
    renderMatchesTab(df);
    renderCharts(df);
    renderActiveFilters();

    lucide.createIcons();
  }}

  function bindEvents() {{
    $$('[data-tab]').forEach(btn => btn.addEventListener('click', () => switchTab(btn.dataset.tab)));
    $$('[data-jump]').forEach(btn => btn.addEventListener('click', () => switchTab(btn.dataset.jump)));

    $('#openFilters').onclick = () => {{ $('#filterDrawer').classList.remove('hidden'); renderFilterDrawerUI(); }};
    $('#closeFilters').onclick = closeDrawer;
    $('#filterBackdrop').onclick = closeDrawer;
    $('#applyFilters').onclick = closeDrawer;
    function closeDrawer() {{ $('#filterDrawer').classList.add('hidden'); }}

    $('#resetFilters').onclick = () => {{
      state.years = new Set(allYears);
      state.types = new Set(allTypes);
      state.opps  = new Set();
      $('#opponentSearch').value = '';
      renderFilterDrawerUI(); rerender();
    }};
    $('#clearAllFilters').onclick = () => $('#resetFilters').click();

    $$('[data-toggle-all]').forEach(btn => btn.onclick = () => {{
      const target = btn.dataset.toggleAll;
      if (target === 'years') {{
        state.years = state.years.size === allYears.length ? new Set() : new Set(allYears);
      }}
      if (target === 'types') {{
        state.types = state.types.size === allTypes.length ? new Set() : new Set(allTypes);
      }}
      renderFilterDrawerUI(); rerender();
    }});

    $('#opponentSearch').addEventListener('input', renderFilterDrawerUI);

    $('#matchSearch').addEventListener('input', e => {{
      state.matchSearch = e.target.value;
      renderMatchesTab(getFiltered());
    }});

    $$('th.sortable').forEach(th => th.addEventListener('click', () => {{
      const k = th.dataset.sort;
      if (state.matchSort.key === k) {{
        state.matchSort.dir = state.matchSort.dir === 'asc' ? 'desc' : 'asc';
      }} else {{
        state.matchSort = {{ key: k, dir: 'asc' }};
      }}
      renderMatchesTab(getFiltered());
    }}));

    document.addEventListener('keydown', e => {{
      if (e.key === 'Escape') $('#filterDrawer').classList.add('hidden');
    }});

    let rt;
    window.addEventListener('resize', () => {{
      clearTimeout(rt);
      rt = setTimeout(() => Object.values(charts).forEach(c => c && c.resize()), 120);
    }});
  }}

  function init() {{
    if (!RAW.length) {{
      document.body.innerHTML = `<div style="padding:40px;color:#cbd5e1;text-align:center">
        <h1 style="font-size:24px;margin-bottom:12px">No data found</h1>
        <p>Make sure <code>data.py</code> contains <code>CRICKET_DATA</code>.</p>
      </div>`;
      return;
    }}
    $('#lastUpdated').textContent = new Date().toLocaleDateString('en-US', {{ year:'numeric', month:'short', day:'numeric' }});
    bindEvents();
    rerender();
    switchTab('overview');
  }}

  function whenLibsReady(cb) {{
    if (window.Chart && window.lucide && window.tailwind) cb();
    else setTimeout(() => whenLibsReady(cb), 30);
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', () => whenLibsReady(init));
  }} else {{
    whenLibsReady(init);
  }}
}})();
</script>
</body>
</html>
"""
