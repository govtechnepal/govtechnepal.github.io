// Input, Preeti conversion, and Bikram Sambat for the browser demo.
// Keyboard maps: Keyman nepali_romanized / nepali_traditional (MIT, Santosh Pradhan),
// which record the Madan Puraskar Pratisthan layouts. The Lipi repository was not
// readable from this environment.

const MONTHS_NE = [
  null,
  "वैशाख",
  "जेष्ठ",
  "असार",
  "श्रावण",
  "भदौ",
  "आश्विन",
  "कार्तिक",
  "मंसिर",
  "पौष",
  "माघ",
  "फाल्गुण",
  "चैत्र",
];

const MONTHS_EN = [
  null,
  "Baishakh",
  "Jestha",
  "Asar",
  "Shrawan",
  "Bhadau",
  "Aswin",
  "Kartik",
  "Mangsir",
  "Poush",
  "Magh",
  "Falgun",
  "Chaitra",
];

const DIGITS = "०१२३४५६७८९";

export function createTyper(layout) {
  let dead = null;
  return {
    type(ch) {
      if (layout.passThrough) return ch;
      if (dead) {
        const table = (layout.dead && layout.dead[dead]) || {};
        dead = null;
        if (Object.prototype.hasOwnProperty.call(table, ch)) return table[ch];
      }
      if (layout.dead && Object.prototype.hasOwnProperty.call(layout.dead, ch)) {
        dead = ch;
        return "";
      }
      if (Object.prototype.hasOwnProperty.call(layout.map, ch)) return layout.map[ch];
      return ch;
    },
    reset() {
      dead = null;
    },
  };
}

export function typeString(layout, text) {
  const typer = createTyper(layout);
  let out = "";
  for (const ch of text) out += typer.type(ch);
  return out;
}

export function convertPreeti(text, data) {
  const parts = text.match(/\s+|\S+/g) || [];
  return parts
    .map((part) => {
      if (/^\s+$/.test(part)) return part;
      let converted = "";
      for (const ch of part) converted += data.charMap[ch] ?? ch;
      for (const [pattern, repl] of data.post) {
        converted = converted.replace(new RegExp(pattern, "g"), repl ?? "");
      }
      return converted;
    })
    .join("");
}

function nepalParts(date) {
  const fmt = new Intl.DateTimeFormat("en-CA", {
    timeZone: "Asia/Kathmandu",
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
    weekday: "short",
  });
  return Object.fromEntries(fmt.formatToParts(date).map((part) => [part.type, part.value]));
}

export function toBikram(date, calendar) {
  const parts = nepalParts(date);
  const yearAD = Number(parts.year);
  const monthAD = Number(parts.month);
  const dayAD = Number(parts.day);
  const utc = Date.UTC(yearAD, monthAD - 1, dayAD);
  const ref = Date.UTC(1918, 3, 13);
  let days = Math.round((utc - ref) / 86400000);
  const byYear = new Map(calendar.map((row) => [row[0], row.slice(1)]));
  let year = 1975;
  while (year <= 2100) {
    const months = byYear.get(year);
    const yearDays = months.reduce((sum, daysInMonth) => sum + daysInMonth, 0);
    if (days < yearDays) break;
    days -= yearDays;
    year += 1;
  }
  const months = byYear.get(year);
  let month = 1;
  for (; month <= 12; month += 1) {
    if (days < months[month - 1]) break;
    days -= months[month - 1];
  }
  const day = days + 1;
  const ne = (value) => String(value).replace(/\d/g, (digit) => DIGITS[digit]);
  return {
    year,
    month,
    day,
    ne: `${ne(day)} ${MONTHS_NE[month]} ${ne(year)}`,
    en: `${day} ${MONTHS_EN[month]} ${year}`,
    time: `${parts.hour}:${parts.minute}`,
    ad: `${parts.year}-${parts.month}-${parts.day}`,
    weekday: parts.weekday,
  };
}
