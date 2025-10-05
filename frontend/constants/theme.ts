/**
 * FreshCam Theme
 * Supports both light/dark mode + custom brand colors
 */

import { Platform } from "react-native";

const tintColorLight = "#4CAF50"; // FreshCam green
const tintColorDark = "#81C784";  // Softer green for dark mode

export const Colors = {
  light: {
    text: "#11181C",
    background: "#FFFFFF",
    tint: tintColorLight,
    icon: "#687076",
    tabIconDefault: "#687076",
    tabIconSelected: tintColorLight,
    card: "#FFFFFF",
    shadow: "#00000020",
  },
  dark: {
    text: "#ECEDEE",
    background: "#151718",
    tint: tintColorDark,
    icon: "#9BA1A6",
    tabIconDefault: "#9BA1A6",
    tabIconSelected: tintColorDark,
    card: "#1E1E1E",
    shadow: "#00000050",
  },

  // 🍃 Brand Colors — usable in both themes
  primary: "#4CAF50",     // main green
  accent: "#FFC107",      // yellow accent
  danger: "#E53935",      // red for overripe alerts
  info: "#2196F3",        // blue for details or tooltips
  success: "#66BB6A",     // lighter green for "fresh"
  
};

export const Fonts = Platform.select({
  ios: {
    sans: "system-ui",
    serif: "ui-serif",
    rounded: "ui-rounded",
    mono: "ui-monospace",
  },
  default: {
    sans: "normal",
    serif: "serif",
    rounded: "normal",
    mono: "monospace",
  },
  web: {
    sans: "system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    serif: "Georgia, 'Times New Roman', serif",
    rounded: "'SF Pro Rounded', 'Hiragino Maru Gothic ProN', Meiryo, 'MS PGothic', sans-serif",
    mono: "SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace",
  },
});

export const FlatColors = {
  text: Colors.light.text,
  background: Colors.light.background,
  primary: Colors.primary,
  accent: Colors.accent,
  danger: Colors.danger,
  success: Colors.success,
  info: Colors.info,
  card: Colors.light.card,
  shadow: Colors.light.shadow,
};