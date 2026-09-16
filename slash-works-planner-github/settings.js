/* Slash Works Room Planner — settings
   Edit this file to change prices, names, the inquiry email, the disclaimer,
   and the finish options. Keep the quotes and commas as they are.
   Piece ids ("01"…"05") must match the models in data/models.js. */

const CONTACT_EMAIL = "info@slash-works.com";
const PIECES = [
  { id:"01", name:"Object 01", price:600  },
  { id:"02", name:"Object 02", price:500  },
  { id:"03", name:"Object 03", price:900  },
  { id:"04", name:"Object 04", price:2900 },
  { id:"05", name:"Object 05", price:2000 },
];
const DISCLAIMER = "Estimate only. Excludes tax & shipping.";
const FLOORS = {
  oak:      { label:"Light oak" },
  dark:     { label:"Dark wood" },
  concrete: { label:"Polished concrete" },
  tile:     { label:"White tile" },
};
const WALLS = {
  white:    { label:"White",     color:"#F1EFEA" },
  gray:     { label:"Warm gray", color:"#CBC5BB" },
  charcoal: { label:"Charcoal",  color:"#48494D" },
};
