document.addEventListener("DOMContentLoaded", () => {
  generatePeriodicTable();
});

function generatePeriodicTable() {
  const elements = [
    { symbol: "H", name: "Hydrogen", atomicNumber: 1, group: "Nonmetal" },
    { symbol: "He", name: "Helium", atomicNumber: 2, group: "Noble Gas" },
    // Add other periodic elements as needed
  ];

  const tableContainer = document.getElementById("table-container");
  elements.forEach(element => {
    const div = document.createElement("div");
    div.classList.add("element");
    div.innerHTML = `<strong>${element.symbol}</strong><br>${element.name}`;
    div.title = `Atomic Number: ${element.atomicNumber}`;
    div.onclick = () => showElementDetails(element);
    tableContainer.appendChild(div);
  });
}

function showElementDetails(element) {
  const detailsDiv = document.getElementById("element-details");
  detailsDiv.innerHTML = `
    <h3>${element.name} (${element.symbol})</h3>
    <p>Atomic Number: ${element.atomicNumber}</p>
    <p>Group: ${element.group}</p>
  `;
}

function showBondingInfo(type) {
  const bondingInfo = {
    ionic: "Ionic bonds form when atoms transfer electrons.",
    covalent: "Covalent bonds form when atoms share electrons.",
    metallic: "Metallic bonds involve a sea of shared electrons.",
    hydrogen: "Hydrogen bonds occur between polar molecules.",
  };
  document.getElementById("bonding-info").innerText = bondingInfo[type] || "Select a bonding type.";
}

function balanceReaction() {
  const input = document.getElementById("reaction-input").value;
  const output = document.getElementById("reaction-output");
  if (!input) {
    output.innerText = "Please enter a chemical reaction.";
    return;
  }
  // Placeholder for balancing logic
  output.innerText = `Balanced Reaction (logic pending): ${input}`;
}

function startQuiz() {
  const quizContainer = document.getElementById("quiz-container");
  quizContainer.innerHTML = `
    <p>What is the atomic number of Oxygen?</p>
    <button onclick="checkAnswer('8')">8</button>
    <button onclick="checkAnswer('16')">16</button>
    <button onclick="checkAnswer('6')">6</button>
  `;
}

function checkAnswer(answer) {
  alert(answer === "8" ? "Correct!" : "Try Again.");
}