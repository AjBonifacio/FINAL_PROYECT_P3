const apiUrl = "http://localhost:3000/api/items";

// Obtener y mostrar items
const fetchItems = async () => {
  const response = await fetch(apiUrl);
  const items = await response.json();
  const table = document.getElementById("itemsTable");
  table.innerHTML = items.map(item => `
    <tr>
      <td>${item.code}</td>
      <td>${item.name}</td>
      <td><img src="${item.photo}" alt="${item.name}" style="width:50px;height:50px;"></td>
      <td>${item.description}</td>
      <td>${item.quantity}</td>
      <td>${item.price}</td>
      <td>
        <button onclick="deleteItem(${item.id})">Eliminar</button>
        <button onclick="editItem(${item.id}, '${item.code}', '${item.name}', '${item.photo}', '${item.description}', ${item.quantity}, ${item.price})">Editar</button>
      </td>
    </tr>
  `).join('');
};

// Agregar item
document.getElementById("itemForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const item = {
    code: document.getElementById("itemCode").value,
    name: document.getElementById("itemName").value,
    photo: document.getElementById("itemPhoto").value,
    description: document.getElementById("itemDescription").value,
    quantity: parseInt(document.getElementById("itemQuantity").value, 10),
    price: parseFloat(document.getElementById("itemPrice").value)
  };
  await fetch(apiUrl, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(item)
  });
  document.getElementById("itemForm").reset();
  fetchItems();
});

// Editar item
const editItem = async (id, code, name, photo, description, quantity, price) => {
  const newCode = prompt("Editar código del artículo:", code) || code;
  const newName = prompt("Editar nombre del artículo:", name) || name;
  const newPhoto = prompt("Editar URL de la foto:", photo) || photo;
  const newDescription = prompt("Editar descripción:", description) || description;
  const newQuantity = prompt("Editar cantidad disponible:", quantity) || quantity;
  const newPrice = prompt("Editar precio:", price) || price;

  await fetch(`${apiUrl}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      code: newCode,
      name: newName,
      photo: newPhoto,
      description: newDescription,
      quantity: parseInt(newQuantity, 10),
      price: parseFloat(newPrice)
    })
  });
  fetchItems();
};

// Eliminar item
const deleteItem = async (id) => {
  await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
  fetchItems();
};

// Inicializar
fetchItems();
