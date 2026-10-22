import { convertPreeti, createTyper, toBikram } from "./engine.js";
import { MINISTRIES, WALLPAPERS } from "./wallpapers.js";

const FONT_URLS = {
  Kalimati: "https://raw.githubusercontent.com/mhnpd/nepali-font/master/fonts/Kalimati.ttf",
  Preeti: "https://raw.githubusercontent.com/mhnpd/nepali-font/master/fonts/Preeti.TTF",
};

const state = {
  ministry: null,
  wallpaper: WALLPAPERS[0],
  layoutId: "romanized",
  keyboards: null,
  preeti: null,
  calendar: null,
  fonts: { Kalimati: false, Preeti: false },
  shift: false,
};

const $ = (id) => document.getElementById(id);

function show(id) {
  for (const screen of document.querySelectorAll(".screen")) {
    const on = screen.id === id;
    screen.classList.toggle("on", on);
    screen.setAttribute("aria-hidden", on ? "false" : "true");
  }
}

function applyMinistry(ministry) {
  state.ministry = ministry;
  document.documentElement.style.setProperty("--accent", ministry.accent);
  $("splash-ne").textContent = ministry.nameNe;
  $("splash-en").textContent = ministry.nameEn;
  $("login-ne").textContent = ministry.nameNe;
  $("login-en").textContent = ministry.nameEn;
  $("login-support").textContent = ministry.support;
  $("lock-ne").textContent = ministry.nameNe;
  $("lock-en").textContent = ministry.nameEn;
  $("about-body").innerHTML = `
    <p><strong>${ministry.nameNe}</strong><br>${ministry.nameEn}</p>
    <p>NepalOS 0.2.0 · Debian 13 (trixie) · KDE Plasma<br>
    NepalOS · Powered by GovTechNepal</p>
    <p>Support: ${ministry.support}</p>
    <p>This browser demo is a community prototype by GovTechNepal (govtechnepal.org). It does not use the national emblem.</p>
    <p>Photographs are from Wikimedia Commons. Authors and licences are on the wallpaper caption and in <a href="CREDITS.md">CREDITS.md</a>.</p>
  `;
}

function creditLine(photo) {
  return `${photo.titleNe} · ${photo.title} · ${photo.author} · ${photo.license}`;
}

function paintPhoto(photo) {
  state.wallpaper = photo;
  const url = `url("${photo.file}")`;
  $("stage").style.backgroundImage = url;
  $("wizard-photo").style.backgroundImage = url;
  $("wizard-credit").textContent = creditLine(photo);
  for (const id of ["login-credit", "desk-credit", "lock-credit"]) {
    $(id).textContent = creditLine(photo);
  }
}

function renderCards() {
  const box = $("ministry-cards");
  box.innerHTML = "";
  for (const ministry of MINISTRIES) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "card";
    button.dataset.code = ministry.code;
    button.innerHTML = `<i style="--swatch:${ministry.accent}"></i><span><b>${ministry.nameNe}</b><small>${ministry.nameEn}</small></span>`;
    button.addEventListener("click", () => {
      for (const card of box.querySelectorAll(".card")) card.classList.remove("selected");
      button.classList.add("selected");
      state.ministry = ministry;
    });
    box.appendChild(button);
  }
  box.querySelector(".card").click();
}

function chosenMinistry() {
  return state.ministry;
}

function tick() {
  if (!state.calendar) return;
  const bs = toBikram(new Date(), state.calendar);
  $("clock").innerHTML = `<b>${bs.ne}</b><small>${bs.time} · ${bs.ad}</small>`;
}

function layout() {
  return state.keyboards[state.layoutId];
}

function fontFamily() {
  const choice = $("font-select").value;
  if (choice === "Preeti" && state.fonts.Preeti) return '"Preeti", "Noto Sans Devanagari", sans-serif';
  if (choice === "Kalimati" && state.fonts.Kalimati) return '"Kalimati", "Noto Sans Devanagari", sans-serif';
  return '"Noto Sans Devanagari", "Noto Sans", sans-serif';
}

function updateFontNote() {
  const choice = $("font-select").value;
  const page = $("page");
  page.style.fontFamily = fontFamily();
  const bits = [];
  if (choice === "Kalimati" && state.fonts.Kalimati) {
    bits.push("Kalimati 12 pt. The prototype package downloads this file at build time. Redistribution rights must be confirmed before production. This demo also fetches it in the browser.");
  } else if (choice === "Kalimati") {
    bits.push("Kalimati did not load. Showing Noto Sans Devanagari instead.");
  } else if (choice === "Preeti" && state.fonts.Preeti) {
    bits.push("Preeti is a legacy encoding face, loaded at runtime and not bundled. Unicode typing will look wrong in Preeti. Use the converter for old Preeti text, then switch back to Kalimati or Noto.");
  } else if (choice === "Preeti") {
    bits.push("Preeti did not load. Showing Noto Sans Devanagari. Preeti is not bundled.");
  } else {
    bits.push("Noto Sans Devanagari (SIL Open Font License). This is the fallback when Kalimati is absent.");
  }
  $("font-note").textContent = bits[0];
}

function insertText(text) {
  const page = $("page");
  const start = page.selectionStart ?? page.value.length;
  const end = page.selectionEnd ?? page.value.length;
  page.setRangeText(text, start, end, "end");
  page.focus();
}

function onType(ch) {
  const typer = createTyper(layout());
  // Physical keys are independent events; dead-key state must persist.
  if (!state.typer || state.typerId !== state.layoutId) {
    state.typer = createTyper(layout());
    state.typerId = state.layoutId;
  }
  const out = state.typer.type(ch);
  if (out) insertText(out);
}

function renderOsk() {
  const rows = ["`1234567890-=", "qwertyuiop[]\\", "asdfghjkl;'", "zxcvbnm,./"];
  const shifted = {
    "`": "~", "1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*",
    "9": "(", "0": ")", "-": "_", "=": "+", "[": "{", "]": "}", "\\": "|", ";": ":", "'": "\"",
    ",": "<", ".": ">", "/": "?",
  };
  const box = $("osk");
  box.innerHTML = "";
  const shiftRow = document.createElement("div");
  shiftRow.className = "osk-row";
  const shift = document.createElement("button");
  shift.type = "button";
  shift.className = "key";
  shift.innerHTML = "<b>Shift</b>";
  shift.addEventListener("click", () => {
    state.shift = !state.shift;
    renderOsk();
  });
  shiftRow.appendChild(shift);
  box.appendChild(shiftRow);
  const current = layout();
  for (const row of rows) {
    const line = document.createElement("div");
    line.className = "osk-row";
    for (const ch of row) {
      const shown = state.shift ? (shifted[ch] || ch.toUpperCase()) : ch;
      const label = current.passThrough ? shown : (current.map[shown] ?? shown);
      const key = document.createElement("button");
      key.type = "button";
      key.className = "key";
      key.innerHTML = `<small>${shown}</small><b>${label || "·"}</b>`;
      key.addEventListener("click", () => onType(shown));
      line.appendChild(key);
    }
    box.appendChild(line);
  }
}

function renderKeyboardMenu() {
  const menu = $("kb-menu");
  menu.innerHTML = "";
  const button = $("kb-button");
  const labels = { english: "EN", romanized: "रोम", traditional: "पर" };
  button.textContent = labels[state.layoutId];
  for (const id of ["english", "romanized", "traditional"]) {
    const item = state.keyboards[id];
    const choice = document.createElement("button");
    choice.type = "button";
    choice.setAttribute("role", "menuitemradio");
    choice.setAttribute("aria-checked", id === state.layoutId ? "true" : "false");
    choice.textContent = `${item.nameNe} · ${item.name}`;
    choice.addEventListener("click", () => {
      state.layoutId = id;
      state.typer = createTyper(layout());
      state.typerId = id;
      menu.classList.remove("on");
      renderKeyboardMenu();
      renderOsk();
    });
    menu.appendChild(choice);
  }
}

function renderLauncher() {
  const launcher = $("launcher");
  const items = [
    ["writer", "लेखक · Writer"],
    ["browser", "Chrome"],
    ["walls", "पर्खाल · Wallpapers"],
    ["about", "बारेमा · About"],
    ["lock", "लक · Lock"],
  ];
  launcher.innerHTML = "";
  for (const [id, label] of items) {
    const button = document.createElement("button");
    button.type = "button";
    button.textContent = label;
    button.addEventListener("click", () => {
      launcher.classList.remove("on");
      if (id === "lock") {
        show("lock");
        return;
      }
      openWindow(id);
    });
    launcher.appendChild(button);
  }
}

function renderWalls() {
  const grid = $("wall-grid");
  grid.innerHTML = "";
  for (const photo of WALLPAPERS) {
    const button = document.createElement("button");
    button.type = "button";
    button.innerHTML = `<img alt="" src="${photo.file}"><span>${photo.titleNe}<br>${photo.author}</span>`;
    button.addEventListener("click", () => {
      paintPhoto(photo);
      $("walls").classList.remove("on");
    });
    grid.appendChild(button);
  }
}

function setLook(mode) {
  document.body.classList.toggle("dark", mode === "dark");
  $("look-chooser").classList.remove("on");
  sessionStorage.setItem("nepalos-look", mode);
}

function openWindow(id) {
  for (const win of document.querySelectorAll(".window")) win.classList.remove("on");
  $(id).classList.add("on");
  $("task-writer").hidden = id !== "writer";
  $("task-writer").classList.toggle("active", id === "writer");
  if (id === "writer") $("page").focus();
}

async function loadOptionalFonts() {
  await Promise.all(
    Object.entries(FONT_URLS).map(async ([family, url]) => {
      try {
        const face = new FontFace(family, `url(${url})`);
        await face.load();
        document.fonts.add(face);
        state.fonts[family] = true;
      } catch {
        state.fonts[family] = false;
      }
    }),
  );
  if (!state.fonts.Kalimati) $("font-select").value = "Noto Sans Devanagari";
  updateFontNote();
}

async function main() {
  const [keyboards, preeti, calendar] = await Promise.all([
    fetch("data/keyboards.json").then((response) => response.json()),
    fetch("data/preeti.json").then((response) => response.json()),
    fetch("data/calendar.json").then((response) => response.json()),
  ]);
  state.keyboards = keyboards;
  state.preeti = preeti;
  state.calendar = calendar;
  state.typer = createTyper(layout());
  state.typerId = state.layoutId;
  renderCards();
  renderLauncher();
  renderKeyboardMenu();
  renderOsk();
  renderWalls();
  paintPhoto(WALLPAPERS[0]);
  tick();
  setInterval(tick, 15000);
  loadOptionalFonts();


  $("wizard-form").addEventListener("submit", (event) => {
    event.preventDefault();
    const ministry = chosenMinistry();
    if (!ministry) return;
    applyMinistry(ministry);
    show("splash");
    window.setTimeout(() => show("login"), 1700);
  });

  $("login-form").addEventListener("submit", (event) => {
    event.preventDefault();
    show("desktop");
    if (!sessionStorage.getItem("nepalos-look")) $("look-chooser").classList.add("on");
  });
  $("look-light").addEventListener("click", () => setLook("light"));
  $("look-dark").addEventListener("click", () => setLook("dark"));
  $("look").addEventListener("click", () => $("look-chooser").classList.toggle("on"));
  $("lock-form").addEventListener("submit", (event) => {
    event.preventDefault();
    show("desktop");
  });

  $("start").addEventListener("click", () => {
    $("kb-menu").classList.remove("on");
    $("launcher").classList.toggle("on");
  });
  $("kb-button").addEventListener("click", () => {
    $("launcher").classList.remove("on");
    $("kb-menu").classList.toggle("on");
  });
  $("task-writer").addEventListener("click", () => openWindow("writer"));
  for (const button of document.querySelectorAll("[data-open]")) {
    button.addEventListener("click", () => openWindow(button.dataset.open));
  }
  for (const button of document.querySelectorAll("[data-close]")) {
    button.addEventListener("click", () => {
      $(button.dataset.close).classList.remove("on");
      $("task-writer").hidden = true;
    });
  }

  $("page").addEventListener("keydown", (event) => {
    if (event.metaKey || event.ctrlKey || event.altKey) return;
    if (event.key.length !== 1) return;
    if (state.layoutId === "english") return;
    event.preventDefault();
    onType(event.key);
  });
  $("font-select").addEventListener("change", updateFontNote);
  $("convert").addEventListener("click", () => {
    $("preeti-out").value = convertPreeti($("preeti-in").value, state.preeti);
  });
  $("preeti-in").value = "g]kfn";
}

main();
