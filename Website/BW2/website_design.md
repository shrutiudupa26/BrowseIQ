# BASIC+ – Creative Design Specification**Design theme:** Stark noir canvas punctuated by molten–metal gradients and sculptural3-D ribbon forms**Atmosphere:** Intimate night-club glow; velvety blacks, copper-rose flares, and amethyst undertones. Typography punches through the darkness like neon headlines while UI chrome stays ghost-light and utilitarian.

---

##1. Foundations (Design System)

### Colour Tokens| Token | Purpose | Hex |
|-------|---------|-----|
| ink-900 | Primary background | #1b1516 |
| copper-500 | Signature gradient stop1 | #c7856d |
| ember-700 | Gradient stop2 / danger | #6e3029 |
| ghost-100 | Body text / surfaces | #8b8c82 |
| amethyst-400 | Secondary accent | #7a528f |
| snow-0 | Pure white text / icons | #ffffff |
| slate-600 | Disabled / outlines | #4d4d4d |
| success-500 | Positive state | #3dd598 |
| info-400 | Informational | #4c83ff |

Gradient recipe “Molten”: linear-gradient(135deg, copper-5000%, ember-70050%, amethyst-400100%)

### Typography Stack• Display (h1-h2): “Poppins”,800, ‑2% letter-spacing• Body (h3-p): “Inter”,400–700• Code / Mono: “Fira Code”,400### Sizing & Effects• Spacing scale:0.25rem,0.5rem,1,1.5,2,3,4,6,8• Radius: xs2px, sm4px, md8px, lg16px, pill9999px• Shadow.lift:024rgba(0,0,0,.6)• Shadow.glow-accent:0032rgba(199,133,109,.45)•3-D ribbon effect: <img> mesh-gradient PNG + subtle WebGL rotation on scroll---

##2. Site-wide Layout• Grid:12-col, max-width1280px,24px gutters;mobile4-col (16px gutters)• Breakpoints: sm≥640, md≥768, lg≥1024, xl≥1280• Motion: – Scroll scrubbed parallax on hero ribbon (-30px to +60px Y) – Section reveals: fade-up40ms/col, cubic-bezier(.4,.0,.2,1) – Reduced-motion: all transforms disabled, opacity reveal instant• Header: sticky,64px height, glass blur(8px), darken(0.4) on scroll >80px• Footer: sticky-reveal (slides in last400px of page),240px tall, molten gradient top-border4px---

##3. Pages & Key Sections### HOME| Seq | Block | Notes |
|-----|-------|-------|
|1 | Hero: “Reach new heights” | Full-viewport; foreground ribbon WebGL canvas; CTA “Register” (primary) + “Learn more” (ghost). |
|2 | Value Tiles |3 cards (Up to50% Rev Share, CPA, Hybrid) slide-in. |
|3 | How It Works |4-step timeline, line animates copper→amethyst on scroll. |
|4 | Testimonials | Dark carousel, avatar rings glow on hover. |
|5 | Call to Action Strip | Slim bar, pill button bounces gently. |

### ABOUT| Seq | Block | Notes |
|-----|-------|-------|
|1 | Mission Statement | Split layout: text left, floating3-D ribbon right, lazy loads. |
|2 | The Team | Grid of cards, tilt-on-hover. |
|3 | Tech Stack | Icon wall; icons hue-rotate along gradient on hover. |

### CONTACT| Seq | Block | Notes |
|-----|-------|-------|
|1 | Get in Touch Hero | Copper gradient orb pulses. |
|2 | Form |2-col, floating labels; inline validation. |
|3 | Map | Dark-themed mapbox embed, neon pin. |

---

##4. Reusable Components & Micro-Interactions| Component | Behaviour / States & A11y |
|-----------|---------------------------|
| Button (primary, ghost, danger) | Idle: solid molten / ghost outline. Hover: translateY(-2px), glow-accent. Focus:2px focus ring #4c83ff. Active: compress95%. Disabled: slate-600, no glow. |
| Input | Idle: slate-600 border. Hover: border-copper-500. Focus:2px amethyst ring, label lifts. Error: ember-700 border + message aria-live. |
| Card | Hover: raise4px, Shadow.lift. Tap: quick scale(0.98). |
| Ribbon-3D WebGL | Mouse move rotates ±8°, inertia. aria-hidden="true". |
| Accordion | Chevron rotates90°, height auto with CSS “content-visibility”. |
| Toast | Slide in bottom-right,300ms; colours map to success/info/error tokens; auto-dismiss4s, pause on hover. |
| Loader | Circular stroke-dashoffset spinner, gradient stroke; aria-busy="true" toggles. |

---

##5. Performance & Accessibility Targets• Images: AVIF first, fallback WebP; hero3-D ribbon rendered once, reused via <picture>.• bundle <90KB gzipped; Tailwind JIT purge.• Lighthouse ≥95 across PWA, perf, a11y.• All hover effects mirrored by focus-visible.• Prefers-reduced-motion: disables transforms/parallax, keeps opacity.• Contrast ratio ≥4.5:1 on interactive text.• Lazy-load off-screen assets with `loading="lazy"` + `fetchpriority="high"` hero.