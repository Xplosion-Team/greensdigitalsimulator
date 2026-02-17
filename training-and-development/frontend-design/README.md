# 🎨 Frontend Design Module

## Overview
This module contains frontend design specifications, UI components, and visualization tools for the CGM digital simulator application. It provides a comprehensive design system for building consistent and accessible user interfaces across web and mobile platforms.

## Purpose
- Define UI component specifications and design patterns
- Provide visualization modules for CGM data
- Document user interaction flows
- Ensure accessibility and usability standards
- Maintain consistent design across platforms

## Module Structure

```
frontend-design/
├── README.md                        # This file
├── components/
│   ├── glucose_display.md           # Glucose value display component
│   ├── trend_indicator.md           # Trend arrow and direction
│   ├── glucose_graph.md             # Time-series glucose chart
│   └── meal_logger.md               # Meal logging interface
├── visualizations/
│   ├── glucose_timeline.py          # Timeline visualization
│   ├── agp_report.py                # Ambulatory Glucose Profile
│   └── patterns_view.py             # Pattern detection visualizations
├── user_flows.md                    # User interaction flows
└── design_system.md                 # Colors, typography, spacing
```

## Design Principles

### 1. **Clarity First**
- Large, easy-to-read glucose values
- Clear status indicators (colors, icons)
- Minimal cognitive load
- Obvious call-to-action buttons

### 2. **Accessibility**
- WCAG 2.1 AA compliance
- High contrast colors
- Screen reader support
- Keyboard navigation
- Large touch targets (minimum 44x44px)

### 3. **Data Visualization**
- Intuitive glucose graphs
- Pattern highlighting
- Time-in-range visualization
- Meal/insulin markers on timeline

### 4. **Mobile-First**
- Touch-friendly interfaces
- Responsive layouts
- Offline-capable
- Fast loading times

## Core Components

### 1. Glucose Display Component

```typescript
// Primary glucose display
interface GlucoseDisplayProps {
  glucose: number;           // Current glucose value
  trend: string;             // Trend direction
  timestamp: string;         // Last reading time
  unit: 'mg/dL' | 'mmol/L';  // Display unit
  size: 'small' | 'medium' | 'large';
}

// Visual design:
// ┌──────────────────────┐
// │                      │
// │       145  ↑         │  <- Large glucose + arrow
// │      mg/dL           │  <- Unit
// │   5 minutes ago      │  <- Timestamp
// │                      │
// └──────────────────────┘
```

**Color Coding:**
- Green: 70-180 mg/dL (in range)
- Yellow: 181-250 mg/dL (high)
- Orange: 55-69 mg/dL (low)
- Red: <55 or >250 mg/dL (critical)

### 2. Trend Indicator

```typescript
interface TrendIndicatorProps {
  trend: 'rapidly_rising' | 'rising' | 'stable' | 'falling' | 'rapidly_falling';
  rate?: number;  // mg/dL per minute
}

// Visual representation:
// ↑↑  Rapidly rising (>2 mg/dL/min)
// ↑   Rising (0.5-2 mg/dL/min)
// →   Stable (-0.5 to 0.5 mg/dL/min)
// ↓   Falling (-2 to -0.5 mg/dL/min)
// ↓↓  Rapidly falling (<-2 mg/dL/min)
```

### 3. Glucose Graph

```typescript
interface GlucoseGraphProps {
  readings: Array<{glucose: number, timestamp: string}>;
  timeWindow: '3h' | '6h' | '12h' | '24h' | '7d' | '30d';
  showTargetRange: boolean;
  showMeals: boolean;
  showInsulin: boolean;
}

// Visual design:
// ┌──────────────────────────────────────┐
// │ 250 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄      │ High threshold
// │ 180 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │ Target high
// │         ╱╲                           │
// │        ╱  ╲     ╱╲                   │ Glucose curve
// │  ─────╱    ╲___╱  ╲────              │
// │  70 ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │ Target low
// │     🍽️        🍽️                    │ Meal markers
// └──────────────────────────────────────┘
//   6am   9am   12pm  3pm   6pm
```

### 4. Time-in-Range Visualization

```typescript
interface TimeInRangeProps {
  percentage: number;
  target: number;  // Target percentage
  period: string;  // "Last 24 hours"
}

// Visual design (circular gauge):
//       85%
//     ┌─────┐
//    ╱       ╲
//   │   TIR   │  <- Circular progress
//   │  Goal:  │
//   │   70%   │
//    ╲       ╱
//     └─────┘
```

### 5. Meal Logger Interface

```typescript
interface MealLoggerProps {
  onMealLogged: (meal: Meal) => void;
  quickAddOptions?: string[];
}

// Visual design:
// ┌──────────────────────────────────┐
// │ 🍽️ Log Meal                      │
// ├──────────────────────────────────┤
// │ Meal Type: [Breakfast ▼]         │
// │ Foods: [                       ] │
// │ Carbs: [__] g                    │
// │ Protein: [__] g (optional)       │
// │ Fat: [__] g (optional)           │
// │                                  │
// │ Quick Add:                       │
// │ [Oatmeal] [Banana] [Sandwich]    │
// │                                  │
// │         [Log Meal]               │
// └──────────────────────────────────┘
```

## Visualization Modules

### 1. Glucose Timeline
- Scrollable 24-hour view
- Zoom in/out functionality
- Meal and insulin annotations
- Pattern highlights

### 2. Ambulatory Glucose Profile (AGP)
- Statistical summary over 14 days
- Median glucose curve
- 25th-75th percentile range
- 10th-90th percentile range
- Time-in-range bars

### 3. Pattern Detection View
- Highlight recurring patterns
- Dawn phenomenon indicator
- Post-meal spike patterns
- Overnight stability trends

## Color System

### Primary Colors
```css
--glucose-in-range: #4CAF50      /* Green */
--glucose-high: #FF9800          /* Orange */
--glucose-low: #FF5722           /* Red-Orange */
--glucose-critical: #D32F2F      /* Red */

--primary: #2196F3               /* Blue */
--secondary: #9C27B0             /* Purple */
--accent: #00BCD4                /* Cyan */

--background: #FFFFFF            /* White */
--surface: #F5F5F5               /* Light Gray */
--text-primary: #212121          /* Almost Black */
--text-secondary: #757575        /* Gray */
```

### Semantic Colors
```css
--success: #4CAF50
--warning: #FF9800
--error: #F44336
--info: #2196F3
```

## Typography

### Font Sizes
```css
--font-glucose-value: 48px       /* Large glucose display */
--font-heading-1: 32px
--font-heading-2: 24px
--font-heading-3: 20px
--font-body: 16px
--font-small: 14px
--font-tiny: 12px
```

### Font Weights
```css
--weight-light: 300
--weight-regular: 400
--weight-medium: 500
--weight-bold: 700
```

## Spacing System

```css
--spacing-xs: 4px
--spacing-sm: 8px
--spacing-md: 16px
--spacing-lg: 24px
--spacing-xl: 32px
--spacing-xxl: 48px
```

## Responsive Breakpoints

```css
--mobile: 0-767px
--tablet: 768px-1023px
--desktop: 1024px+
```

## User Flows

### Primary Flow: Check Current Glucose
1. Open app
2. See large glucose value immediately
3. View trend arrow
4. See timestamp of last reading

### Flow: Log Meal
1. Tap "Log Meal" button
2. Select meal type or use quick-add
3. Enter carb amount (required)
4. Optionally add protein/fat
5. Confirm and log
6. See meal marker on graph

### Flow: View History
1. Navigate to History tab
2. Select time range (24h, 7d, 30d)
3. View glucose graph with statistics
4. Scroll to see details
5. Tap meal markers for info

### Flow: Run Experiment
1. Navigate to Experiments tab
2. Select experiment template
3. Follow step-by-step protocol
4. Log meals and glucose per schedule
5. View analysis when complete

## Accessibility Guidelines

### Screen Reader Support
- All interactive elements have aria-labels
- Glucose values announced with context
- Trend changes announced
- Alerts read immediately

### Keyboard Navigation
- Tab through all controls
- Enter to activate buttons
- Arrow keys for graph navigation
- Escape to close modals

### Color Contrast
- Minimum 4.5:1 for text
- 3:1 for large text (18px+)
- Icons paired with text labels
- Never rely on color alone

### Touch Targets
- Minimum 44x44px for all tappable elements
- Adequate spacing between buttons
- Large form inputs
- Easy-to-grab sliders/controls

## Animation Guidelines

### Transitions
```css
--transition-fast: 150ms
--transition-normal: 300ms
--transition-slow: 500ms
```

### Motion Preferences
- Respect `prefers-reduced-motion`
- Subtle animations only
- No autoplay videos
- Optional animation toggle

## Example Screens

### Home Screen
```
┌─────────────────────────────┐
│  ☰  Greens Twin     [🔔]   │ <- Header
├─────────────────────────────┤
│                             │
│         145  ↑              │ <- Large glucose
│        mg/dL                │
│     5 minutes ago           │
│                             │
│   ━━━━━━━━━━━━━━━━━━━━━    │ <- Target range
│         ┌───┐               │    indicator
│  TIR: 85% │░░░│             │
│         └───┘               │
│                             │
│  [📊 View Graph]            │
│  [🍽️ Log Meal]             │
│  [🧪 Start Experiment]      │
│                             │
└─────────────────────────────┘
```

### Graph Screen
```
┌─────────────────────────────┐
│  ← Glucose History          │
├─────────────────────────────┤
│  [3h] [6h] [12h] [24h] [7d] │ <- Time selector
├─────────────────────────────┤
│ 250 ┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄┄    │
│ 180 ━━━━━━━━━━━━━━━━━━━━━  │
│         ╱╲                  │
│        ╱  ╲     ╱╲          │
│  ─────╱    ╲___╱  ╲────     │
│  70 ━━━━━━━━━━━━━━━━━━━━━  │
│     🍽️        🍽️           │
├─────────────────────────────┤
│  Statistics (Last 24h)      │
│  • Avg: 125 mg/dL           │
│  • TIR: 85%                 │
│  • CV: 28%                  │
└─────────────────────────────┘
```

## Implementation Notes

### Web (React/Vue)
- Use Chart.js or D3.js for graphs
- Tailwind CSS for styling
- React Query for data fetching
- LocalStorage for offline data

### Mobile (React Native)
- Victory Native for charts
- Styled Components for styling
- AsyncStorage for persistence
- react-native-svg for custom graphics

---

**Next Steps**:
1. Review component specifications
2. Implement base components
3. Build example screens
4. Test with users
5. Iterate based on feedback

For questions or support, refer to the main [Training & Development](../README.md) guide.
