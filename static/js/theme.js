/**
 * iLEARN — Theme Toggle  (static/js/theme.js)
 * Saves preference in localStorage under "ilearn_theme" ("dark" | "light")
 */
const Theme = {
  STORAGE_KEY: "ilearn_theme",

  init() {
    const saved = localStorage.getItem(this.STORAGE_KEY) || "dark";
    this.apply(saved, false);
  },

  apply(theme, save) {
    if (save === undefined) save = true;

    if (theme === "light") {
      document.body.classList.add("light-mode");
    } else {
      document.body.classList.remove("light-mode");
    }

    // Update toggle buttons with clean SVG icon + label (no emoji)
    const sunIcon  = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
    const moonIcon = '<svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink:0"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';

    document.querySelectorAll(".theme-toggle").forEach(function(btn) {
      if (theme === "light") {
        btn.innerHTML = moonIcon + " Dark";
        btn.title = "Switch to dark mode";
      } else {
        btn.innerHTML = sunIcon + " Light";
        btn.title = "Switch to light mode";
      }
    });

    if (save) localStorage.setItem(Theme.STORAGE_KEY, theme);
  },

  toggle() {
    const current = localStorage.getItem(this.STORAGE_KEY) || "dark";
    this.apply(current === "dark" ? "light" : "dark");
  },

  current() {
    return localStorage.getItem(this.STORAGE_KEY) || "dark";
  }
};

// Apply immediately before DOM parsed — prevents flash of wrong theme
(function() {
  var t = localStorage.getItem("ilearn_theme") || "dark";
  if (t === "light") document.body.classList.add("light-mode");
})();

document.addEventListener("DOMContentLoaded", function() {
  Theme.init();
});
