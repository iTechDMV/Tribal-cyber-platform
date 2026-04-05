import os

design_dir = f"{base_dir}/design"
os.makedirs(design_dir, exist_ok=True)

# Create design system documentation
design_system = '''# Tribal Cybersecurity Platform - Design System

## Design Philosophy

### Core Principles
1. **Sovereignty & Dignity**: Design reflects Tribal self-governance and dignity
2. **Cultural Respect**: Authentic geometric patterns, not stereotypes
3. **Government Professionalism**: Meets federal usability standards
4. **Accessibility First**: WCAG 2.1 AA compliant, Section 508
5. **Community-Focused**: Designed for Tribal citizens and leaders

### Cultural Design Approach
- **Geometric Patterns**: Inspired by traditional weaving, pottery, and basketry
- **Earth Tones**: Colors from natural landscapes - earth, sky, water, fire
- **Symbolic Elements**: Four directions, cycles, balance, connection
- **Typography**: Clean, authoritative, highly readable
- **Spacing**: Generous, respectful, uncluttered

---

## Color Palette

### Primary Colors (Tribal Authority)

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Deep Earth** | `#8B4513` | 139, 69, 19 | Primary buttons, headers |
| **Terracotta** | `#CD853F` | 205, 133, 63 | Secondary elements, hover states |
| **Sage Green** | `#6B8E6B` | 107, 142, 107 | Success states, nature themes |
| **Turquoise** | `#40E0D0` | 64, 224, 208 | Accent, highlights, links |

### Secondary Colors (Federal Government)

| Color | Hex | RGB | Usage |
|-------|-----|-----|-------|
| **Government Blue** | `#1C3F95` | 28, 63, 149 | Federal compliance badges |
| **Security Red** | `#B22234` | 178, 34, 52 | Alerts, critical warnings |
| **Gold** | `#D4AF37` | 212, 175, 55 | Awards, achievements |
| **Charcoal** | `#36454F` | 54, 69, 79 | Text, borders |

### Neutral Colors

| Color | Hex | Usage |
|-------|-----|-------|
| **White** | `#FFFFFF` | Backgrounds, cards |
| **Cream** | `#F5F5DC` | Page backgrounds |
| **Light Gray** | `#E5E5E5` | Borders, dividers |
| **Dark Gray** | `#4A4A4A` | Secondary text |

---

## Typography

### Font Stack

**Primary (Headings)**: 
```css
font-family: 'Montserrat', 'Helvetica Neue', Arial, sans-serif;
```

**Secondary (Body)**:
```css
font-family: 'Open Sans', 'Segoe UI', Tahoma, sans-serif;
```

### Type Scale

| Element | Size | Weight | Usage |
|---------|------|--------|-------|
| H1 | 48px | 700 | Page titles |
| H2 | 36px | 600 | Section headers |
| H3 | 28px | 600 | Card titles |
| Body | 16px | 400 | Paragraphs |
| Small | 14px | 500 | Labels, captions |

---

## Geometric Patterns

### Four Directions Pattern
Represents balance and wholeness.

**Usage**: Headers, section dividers (5% opacity max)

### Stepped Diamonds
Represents mountains and progress.

**Usage**: Progress indicators, navigation

### Pattern Rules
1. Never exceed 10% opacity
2. Use single color, low contrast
3. Never use sacred symbols
4. Place at top/bottom, never behind text

---

## UI Components

### Buttons

**Primary (Deep Earth)**
```css
background: #8B4513;
color: #FFFFFF;
border-radius: 4px;
padding: 12px 24px;
font-weight: 600;
text-transform: uppercase;
```

**Secondary (Turquoise)**
```css
background: transparent;
color: #40E0D0;
border: 2px solid #40E0D0;
```

**Federal (Government Blue)**
```css
background: #1C3F95;
color: #FFFFFF;
```

### Cards

**Standard**
```css
background: #FFFFFF;
border: 1px solid #E5E5E5;
border-radius: 8px;
padding: 24px;
box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
```

**With Pattern Accent**
```css
border-top: 4px solid #8B4513;
background-image: url('patterns/four-directions.svg');
opacity: 0.05;
```

### Status Colors
- 🟢 **Secure**: Sage green
- 🟡 **Warning**: Terracotta
- 🔴 **Critical**: Security red
- 🔵 **Federal**: Government blue

---

## Layout

### Grid
- 12-column grid
- Max width: 1400px
- Gutter: 24px
- Margin: 48px

### Spacing Scale
```
4px  - xs
8px  - sm
16px - md
24px - lg
48px - xl
80px - 2xl
```

---

## Accessibility

### WCAG 2.1 AA
- Color contrast: 4.5:1 minimum
- Focus indicators visible
- Alt text for all images
- Keyboard navigation
- Screen reader support

### Section 508
- Federal employee accessible
- Assistive technology compatible

---
