---
name: kale-frontend
description: Build frontend interfaces for Kale's internal OS and client-facing properties. Enforces Kale's brand identity — colors, typography, component patterns, and design philosophy — across all UI work. Use this skill whenever building React components, dashboards, pages, or any visual interface for Kale.
---

# Kale Frontend Design Skill

This skill enforces Kale's brand identity across all frontend work. Every component, page, and interface built for Kale — whether internal OS modules or client-facing properties — must follow these specifications.

Read this entire file before writing any code.

## Brand Philosophy

Kale's visual identity is **calm, confident, and intentional**. The brand draws from organic, earth-tone aesthetics — think high-end wellness brand meets operational tool. Typography should guide the eye instantly and feel confident without visual noise. Prioritize **readability over density**, **calm contrast** over high-energy palettes.

The internal OS specifically should feel like a **refined operational cockpit** — not a flashy SaaS dashboard. It should feel like a tool built by operators for operators: information-dense where needed, but never cluttered. Quiet confidence, not loud decoration.

---

## Color System

All colors must be defined as CSS custom properties on `:root`. Never use raw hex values in component code — always reference variables.

### CSS Variables

```css
:root {
  /* Primary */
  --kale-green: #5C8B67;
  --warm-cream: #F5F1EA;

  /* Secondary Earth-Tones */
  --soft-sage: #85B192;
  --soft-oat: #C7B39C;
  --deep-green: #32704B;

  /* Utility Neutrals */
  --linen-grey: #D6D3CB;
  --birch: #CBC6BC;
  --sage-grey: #D0DDD0;

  /* Contrasting Accents */
  --clay-red: #C85340;
  --charcoal: #292727;
  --slate-blue: #5C7471;

  /* Derived / Functional (for the OS) */
  --bg-primary: #F5F1EA;           /* Warm Cream — main app background */
  --bg-sidebar: #32704B;           /* Deep Green — sidebar background */
  --bg-card: #FFFFFF;              /* White cards on cream background */
  --bg-card-alt: #F9F7F3;         /* Slightly warm white for alternating rows */
  --bg-hover: #EBE8E1;            /* Hover state on cream backgrounds */
  --bg-input: #FFFFFF;             /* Input fields */
  --border-default: #D6D3CB;      /* Linen Grey — default borders */
  --border-subtle: #E5E2DB;       /* Lighter border for cards */

  --text-primary: #292727;         /* Charcoal — primary text */
  --text-secondary: #5C7471;       /* Slate Blue — secondary/muted text */
  --text-tertiary: #8A8580;        /* Warm grey for timestamps, metadata */
  --text-on-green: #F5F1EA;        /* Warm Cream on green backgrounds */
  --text-link: #32704B;            /* Deep Green — links and interactive text */

  /* Status Colors (for deliverability & health indicators) */
  --status-healthy: #5C8B67;       /* Kale Green */
  --status-warning: #C7B39C;       /* Soft Oat — muted warning */
  --status-warning-strong: #D4A44A; /* Warmer gold for stronger warnings */
  --status-critical: #C85340;      /* Clay Red */
  --status-info: #5C7471;          /* Slate Blue */
  --status-neutral: #D6D3CB;       /* Linen Grey */

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(41, 39, 39, 0.05);
  --shadow-md: 0 2px 8px rgba(41, 39, 39, 0.08);
  --shadow-lg: 0 4px 16px rgba(41, 39, 39, 0.10);

  /* Radii */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-lg: 14px;
  --radius-full: 9999px;

  /* Spacing scale (base 4px) */
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
}
```

### Color Usage Rules

1. **Background**: The app shell uses `--warm-cream` as the base. Cards and content panels sit on white (`--bg-card`) to create subtle depth against the cream.
2. **Sidebar**: Always `--deep-green` with `--text-on-green` text. Active nav items use `--kale-green` with slight opacity or a left border indicator.
3. **Status indicators**: Green/oat/red only. Never use bright neon greens, yellows, or reds. Status colors should feel organic, not alarming. The system is calm even when flagging problems.
4. **Accent usage**: `--clay-red` is for destructive actions and critical alerts ONLY. `--slate-blue` is for informational accents. Never use these as decorative colors.
5. **Avoid**: Pure white (#FFFFFF) as a page background — always use `--warm-cream`. Avoid pure black — use `--charcoal` instead. Avoid any blue/purple/neon that isn't in the palette.

---

## Typography

### Font Stack

```css
/* Import from Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=IBM+Plex+Mono:wght@400;500&display=swap');

/*
  NOTE: Bogart is a licensed font (not on Google Fonts).
  For internal OS, use DM Sans Semibold/Bold for H1/H2 as a substitute.
  If Bogart is self-hosted and available, use it for H1 and H2 only.
  The CSS below includes a Bogart fallback chain.
*/

:root {
  --font-display: 'Bogart', 'DM Sans', sans-serif;  /* H1, H2 — use Bogart if available */
  --font-body: 'DM Sans', sans-serif;                /* Everything else */
  --font-mono: 'IBM Plex Mono', monospace;            /* Metrics, data, code */
}
```

### Type Scale (for the OS)

```css
/* H1 — Page titles, dashboard headers */
h1, .text-h1 {
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 1.75rem;    /* 28px */
  line-height: 1.2;
  letter-spacing: -0.01em;
  color: var(--text-primary);
}

/* H2 — Section headers, card titles */
h2, .text-h2 {
  font-family: var(--font-display);
  font-weight: 500;
  font-size: 1.25rem;    /* 20px */
  line-height: 1.3;
  color: var(--text-primary);
}

/* H3 — Subsection headers, table group headers */
h3, .text-h3 {
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 0.9375rem;  /* 15px */
  line-height: 1.4;
  color: var(--text-primary);
}

/* Body */
body, .text-body {
  font-family: var(--font-body);
  font-weight: 300;
  font-size: 0.875rem;   /* 14px */
  line-height: 1.5;
  color: var(--text-primary);
}

/* Small / Labels */
.text-sm {
  font-family: var(--font-body);
  font-weight: 400;
  font-size: 0.8125rem;  /* 13px */
  line-height: 1.4;
  color: var(--text-secondary);
}

/* Caption / Metadata */
.text-xs {
  font-family: var(--font-body);
  font-weight: 400;
  font-size: 0.75rem;    /* 12px */
  line-height: 1.4;
  color: var(--text-tertiary);
}

/* Metric / Data values */
.text-metric {
  font-family: var(--font-mono);
  font-weight: 500;
  font-size: 1.5rem;     /* 24px */
  line-height: 1.1;
  color: var(--text-primary);
  letter-spacing: -0.02em;
}

/* Metric labels */
.text-metric-label {
  font-family: var(--font-body);
  font-weight: 400;
  font-size: 0.75rem;
  line-height: 1.4;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* Monospace for data in tables */
.text-data {
  font-family: var(--font-mono);
  font-weight: 400;
  font-size: 0.8125rem;
}
```

### Typography Rules

1. **Bogart is display-only**: H1 and H2 headings. Never use for body text, labels, or UI elements.
2. **DM Sans is the workhorse**: All body copy, labels, buttons, inputs, navigation, table content.
3. **IBM Plex Mono for data**: Metrics, percentages, counts, timestamps, email addresses, domain names, and any data that benefits from tabular alignment. Use sparingly — it's a signal that says "this is a data point."
4. **Weight discipline**: DM Sans Light (300) for body text gives the brand its calm, airy feel. DM Sans Semibold (600) for emphasis. Never use Bold (700) for DM Sans in the OS — it's too heavy.
5. **No uppercase headings**: Sentence case everywhere. Uppercase is reserved for metric labels only (e.g., "INBOX HEALTH", "TOTAL DOMAINS").

---

## Component Patterns

### Cards

```
- Background: var(--bg-card)
- Border: 1px solid var(--border-subtle)
- Border-radius: var(--radius-md)
- Shadow: var(--shadow-sm), elevate to var(--shadow-md) on hover if interactive
- Padding: var(--space-5) to var(--space-6)
- No colored borders or accent strips unless indicating status
```

### Status Badges

```
Use pill-shaped badges with subtle backgrounds:
- Healthy:  bg rgba(92,139,103,0.12)  text var(--status-healthy)
- Warning:  bg rgba(212,164,74,0.12)  text var(--status-warning-strong)
- Critical: bg rgba(200,83,64,0.12)   text var(--status-critical)
- Info:     bg rgba(92,116,113,0.12)  text var(--status-info)
- Neutral:  bg rgba(214,211,203,0.3)  text var(--text-secondary)

Font: var(--font-body), 600 weight, 12px, uppercase, letter-spacing 0.04em
Border-radius: var(--radius-full)
Padding: 2px 10px
```

### Data Tables

```
- Header: DM Sans 600, 12px uppercase, color var(--text-secondary), letter-spacing 0.05em
- Header bg: transparent (no colored header rows)
- Header border-bottom: 2px solid var(--border-default)
- Row height: 48px minimum
- Row border-bottom: 1px solid var(--border-subtle)
- Alternating rows: optional, use var(--bg-card-alt) if enabled
- Hover: var(--bg-hover)
- Data cells with numbers: use var(--font-mono)
- Clickable rows: cursor pointer, subtle shadow on hover
```

### Buttons

```
Primary:
  bg var(--kale-green), color var(--text-on-green)
  hover: bg var(--deep-green)
  border-radius: var(--radius-sm)
  font: DM Sans 500, 14px
  padding: 8px 16px

Secondary:
  bg transparent, border 1px solid var(--border-default), color var(--text-primary)
  hover: bg var(--bg-hover)

Destructive:
  bg transparent, border 1px solid var(--clay-red), color var(--clay-red)
  hover: bg rgba(200,83,64,0.08)

Ghost:
  bg transparent, color var(--text-secondary)
  hover: color var(--text-primary), bg var(--bg-hover)
```

### Sidebar Navigation

```
- Width: 240px (collapsible to 64px icon-only)
- Background: var(--deep-green)
- Logo area: top, padding var(--space-6), "kale" wordmark in --text-on-green
- Nav items:
  - font: DM Sans 400, 14px
  - color: rgba(245,241,234,0.7)  (cream at 70% opacity)
  - padding: 10px 16px
  - border-radius: var(--radius-sm)
  - hover: rgba(245,241,234,0.1) bg
  - active: rgba(245,241,234,0.15) bg + full opacity text + 3px left border var(--soft-sage)
- Section dividers: 1px solid rgba(245,241,234,0.1), margin var(--space-4) 0
- Module icons: 20px, stroke style, not filled
```

### Metric Cards (Dashboard)

```
- Same card base styles
- Layout: metric value top (text-metric), label below (text-metric-label)
- Optional: small trend indicator (arrow + percentage) in var(--status-healthy) or var(--clay-red)
- Optional: sparkline chart below metric (thin line, no axes, var(--soft-sage) stroke)
- Grid: typically 4 across on desktop, 2 on tablet, stack on mobile
```

### Inputs & Forms

```
- Background: var(--bg-input)
- Border: 1px solid var(--border-default)
- Border-radius: var(--radius-sm)
- Focus: border-color var(--kale-green), box-shadow 0 0 0 3px rgba(92,139,103,0.15)
- Font: DM Sans 400, 14px
- Padding: 8px 12px
- Label: DM Sans 500, 13px, color var(--text-secondary), margin-bottom 6px
- Error state: border-color var(--clay-red), helper text in var(--clay-red)
```

### Alerts & Notifications

```
- Border-radius: var(--radius-md)
- Left border: 3px solid [status color]
- Background: subtle status bg (same as badges)
- Content: icon + title (DM Sans 600, 14px) + description (DM Sans 300, 14px)
- Padding: var(--space-4)
- Dismiss: ghost button, top-right
```

---

## Layout Principles

1. **Page structure**: Sidebar (fixed left) + Main content area. Main content has a top bar with page title, breadcrumbs, and action buttons. Content below is the module's page.
2. **Content max-width**: 1200px centered within the main area, with `var(--space-8)` padding on sides.
3. **Vertical rhythm**: Use the spacing scale consistently. Sections separated by `var(--space-8)` or `var(--space-10)`. Cards within a section separated by `var(--space-4)`.
4. **Grid**: CSS Grid or Flexbox. Dashboard metric cards in a 4-column grid. Detail pages use a 2/3 + 1/3 layout (main content + sidebar details).
5. **Empty states**: Centered illustration area (optional) + message in `--text-secondary` + primary action button. Never leave a blank void.
6. **Loading states**: Skeleton placeholders matching card/row dimensions with a subtle shimmer animation using `--birch` to `--bg-card` gradient.

---

## Motion & Interaction

1. **Transitions**: All interactive state changes use `transition: all 150ms ease`. Never exceed 300ms.
2. **No gratuitous animation**: The OS is a work tool. Entrance animations are allowed for page loads (subtle fade-in, 200ms) but nothing bouncy or playful.
3. **Hover states**: Must be present on all interactive elements. Subtle background shift or shadow elevation.
4. **Focus states**: Visible focus rings for keyboard navigation. Use the kale-green ring defined in inputs.

---

## Implementation Notes

### For React / Next.js (Kale OS)

- Use Tailwind CSS for utility classes BUT define all Kale colors/fonts in `tailwind.config.ts` extending the default theme with the CSS variables above.
- Use shadcn/ui as the component base, then override with Kale's styles.
- Every color in Tailwind should map to a CSS variable: `kale: 'var(--kale-green)'`, etc.
- Global styles go in `globals.css` with the `:root` variables and font imports.

### For standalone artifacts (Claude chat)

- Import Google Fonts via `@import` at top of `<style>` block.
- Define all CSS variables on `:root`.
- Bogart won't be available — use DM Sans 700 as the display font substitute in artifacts.
- Inline all styles (no external CSS files in artifacts).

### For Claude Code builds

- Reference this skill file to maintain brand consistency.
- All new components should use the CSS variable system — never hardcode colors.
- When creating new status types or color needs, derive from the existing palette. Do not introduce new hues.

---

## Anti-Patterns (Never Do These)

- Purple or blue gradients
- Neon status colors (bright green #00FF00, bright red #FF0000)
- Heavy drop shadows (anything with blur > 20px or opacity > 0.15)
- Rounded corners > 16px on cards (this isn't a toy)
- Emojis in the UI (use clean SVG icons instead)
- Decorative leaf/plant illustrations in the OS (that's for marketing, not the tool)
- White (#FFFFFF) page backgrounds without cream context
- Gray sidebar (always deep green)
- More than 2 font families on a single page
- Bold (700) DM Sans for anything other than very small emphasis
