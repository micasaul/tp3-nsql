const API = "http://localhost:5000";

const grupos = [
  "cervecerias",
  "universidades",
  "farmacias",
  "emergencias",
  "supermercados"
];

function generarSelectGrupos() {
  let options = "";

  grupos.forEach(grupo => {
    options += `<option value="${grupo}">${grupo}</option>`;
  });

  return `<select id="grupo">${options}</select>`;
}

document.querySelectorAll(".tab").forEach(btn => {
  btn.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    renderForm(btn.dataset.tab);
  });
});

function renderForm(tipo) {
  const form = document.getElementById("form-container");

  if (tipo === "agregar") {
    form.innerHTML = `
      ${generarSelectGrupos()}
      <input id="nombre" placeholder="Nombre">
      <input id="lat" placeholder="Latitud">
      <input id="lon" placeholder="Longitud">
      <button id="btn-agregar">Agregar</button>
    `;

    document.getElementById("btn-agregar").addEventListener("click", agregar);
  }

  if (tipo === "buscar") {
    form.innerHTML = `
      ${generarSelectGrupos()}
      <input id="lat" placeholder="Latitud">
      <input id="lon" placeholder="Longitud">
      <button id="btn-buscar">Buscar</button>
    `;

    document.getElementById("btn-buscar").addEventListener("click", buscar);
  }

  if (tipo === "distancia") {
    form.innerHTML = `
      ${generarSelectGrupos()}
      <input id="origen" placeholder="Origen">
      <input id="destino" placeholder="Destino">
      <button id="btn-distancia">Calcular</button>
    `;

    document.getElementById("btn-distancia").addEventListener("click", distancia);
  }
}

async function agregar() {
  const grupo = document.getElementById("grupo").value;
  const nombre = document.getElementById("nombre").value;
  const lat = parseFloat(document.getElementById("lat").value);
  const lon = parseFloat(document.getElementById("lon").value);

  const res = await fetch(`${API}/agregar`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ grupo, nombre, lat, lon })
  });

  const data = await res.json();
  document.getElementById("resultado").innerText = data.mensaje;

  cargarLista();
}

async function buscar() {
  const grupo = document.getElementById("grupo").value;
  const lat = parseFloat(document.getElementById("lat").value);
  const lon = parseFloat(document.getElementById("lon").value);

  const res = await fetch(`${API}/buscar`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ grupo, lat, lon })
  });

  const data = await res.json();

  document.getElementById("resultado").innerText =
    JSON.stringify(data, null, 2);
}

async function distancia() {
  const grupo = document.getElementById("grupo").value;
  const origen = document.getElementById("origen").value;
  const destino = document.getElementById("destino").value;

  const res = await fetch(`${API}/distancia`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ grupo, origen, destino })
  });

  const data = await res.json();

  document.getElementById("resultado").innerText =
    `Distancia: ${data.distancia_km} km`;
}

document.getElementById("filtro").addEventListener("change", cargarLista);

async function cargarLista() {
  const filtro = document.getElementById("filtro").value;
  const lista = document.getElementById("lista");

  lista.innerHTML = "";

  const gruposMostrar = filtro === "todos" ? grupos : [filtro];

  for (let grupo of gruposMostrar) {
    const res = await fetch(`${API}/buscar`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        grupo,
        lat: -32.48,
        lon: -58.23
      })
    });

    const data = await res.json();

    data.forEach(lugar => {
      const li = document.createElement("li");
      li.textContent = `${grupo} - ${lugar}`;
      lista.appendChild(li);
    });
  }
}

renderForm("agregar");
cargarLista();