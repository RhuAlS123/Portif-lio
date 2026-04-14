const root = document.documentElement;

function setTheme(next) {
  if (next) {
    root.setAttribute("data-theme", next);
    localStorage.setItem("theme", next);
  } else {
    root.removeAttribute("data-theme");
    localStorage.removeItem("theme");
  }
}

function getPreferredTheme() {
  const saved = localStorage.getItem("theme");
  if (saved === "light" || saved === "dark") return saved;
  return null;
}

function currentTheme() {
  return root.getAttribute("data-theme");
}

function toggleTheme() {
  const now = currentTheme() || (window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  setTheme(now === "dark" ? "light" : "dark");
}

function setupTheme() {
  const pref = getPreferredTheme();
  if (pref) setTheme(pref);

  const btn = document.querySelector(".theme");
  if (btn) btn.addEventListener("click", toggleTheme);
}

function setupMobileNav() {
  const toggle = document.querySelector(".nav__toggle");
  const links = document.querySelector(".nav__links");
  if (!toggle || !links) return;

  function setOpen(open) {
    links.classList.toggle("isOpen", open);
    toggle.setAttribute("aria-expanded", String(open));
  }

  toggle.addEventListener("click", () => {
    const open = !links.classList.contains("isOpen");
    setOpen(open);
  });

  links.addEventListener("click", (e) => {
    const a = e.target.closest("a");
    if (a) setOpen(false);
  });

  document.addEventListener("click", (e) => {
    if (links.contains(e.target) || toggle.contains(e.target)) return;
    setOpen(false);
  });

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") setOpen(false);
  });
}

function setupYear() {
  const el = document.getElementById("year");
  if (el) el.textContent = String(new Date().getFullYear());
}

setupTheme();
setupMobileNav();
setupYear();

