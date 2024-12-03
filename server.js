const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");

const app = express();
const PORT = 3000;

app.use(cors());
app.use(bodyParser.json());

let items = []; // Array para simular una base de datos

// Rutas CRUD
app.get("/api/items", (req, res) => {
  res.json(items);
});

app.post("/api/items", (req, res) => {
  const { code, name, photo, description, quantity, price } = req.body;
  const newItem = { id: Date.now(), code, name, photo, description, quantity, price };
  items.push(newItem);
  res.status(201).json(newItem);
});

app.put("/api/items/:id", (req, res) => {
  const id = parseInt(req.params.id);
  const index = items.findIndex((item) => item.id === id);
  if (index !== -1) {
    const { code, name, photo, description, quantity, price } = req.body;
    items[index] = { id, code, name, photo, description, quantity, price };
    res.json(items[index]);
  } else {
    res.status(404).json({ error: "Item no encontrado" });
  }
});

app.delete("/api/items/:id", (req, res) => {
  const id = parseInt(req.params.id);
  items = items.filter((item) => item.id !== id);
  res.status(204).send();
});

app.use(express.static('public'));


// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor corriendo en http://localhost:${PORT}`);
});
