// Bind transaction form send even
document.getElementById("transactionForm").addEventListener("submit", function (e) {
    e.preventDefault();
    addTransaction();
  });
  
  // Send transaction to backend API
  function addTransaction() {
    const tx_type = document.getElementById("txType").value;
    const account_id = document.getElementById("fromAcc").value;
    const amount = parseFloat(document.getElementById("amount").value);
    const target_id = document.getElementById("toAcc").value || null;
  
    const body = { tx_type, account_id, amount };
    if (tx_type === "transfer") body.target_id = target_id;
  
    fetch("/api/transactions", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    })
      .then(res => res.json())
      .then(data => {
        alert(data.message || data.error);
      });
  }
  
  // Process all transactions
  function processQueue() {
    fetch("/api/process", { method: "POST" })
      .then(res => res.json())
      .then(data => {
        console.table(data); // Display processing results
        alert("All queued transactions processed.");
        loadAccounts(); // Reload account balances
      });
  }

  // Send account creation request
function createAccount() {
  const id = document.getElementById("accountId").value;
  const name = document.getElementById("accountName").value;
  const balance = parseFloat(document.getElementById("accountBalance").value);

  fetch("/api/accounts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id, name, balance })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || data.error);
      loadAccounts(); // ✅ 成功後更新左側帳戶清單
    });
}

// Fetch accounts and render in table
function loadAccounts() {
  fetch("/api/accounts")
    .then(res => res.json())
    .then(data => {
      const tableBody = document.getElementById("accounts-table-body");
      tableBody.innerHTML = "";
      data.forEach(acc => {
        const row = `<tr>
          <td>${acc.id}</td>
          <td>${acc.name}</td>
          <td>${acc.balance}</td>
        </tr>`;
        tableBody.innerHTML += row;
      });
    });
}

// Send account creation request
function createAccount() {
  const id = document.getElementById("accountId").value;
  const name = document.getElementById("accountName").value;
  const balance = parseFloat(document.getElementById("accountBalance").value);

  fetch("/api/accounts", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ id, name, balance })
  })
    .then(res => res.json())
    .then(data => {
      alert(data.message || data.error);
      loadAccounts(); 
    });
}

// Fetch accounts and render in table
function loadAccounts() {
  fetch("/api/accounts")
    .then(res => res.json())
    .then(data => {
      const tableBody = document.getElementById("accounts-table-body");
      tableBody.innerHTML = "";
      data.forEach(acc => {
        const row = `<tr>
          <td>${acc.id}</td>
          <td>${acc.name}</td>
          <td>${acc.balance}</td>
        </tr>`;
        tableBody.innerHTML += row;
      });
    });
}

// Form submit handler for creating account
document.getElementById("createAccountForm").addEventListener("submit", function (e) {
  e.preventDefault();
  createAccount();
});

// Call this on page load to initialize the account table
window.onload = function () {
  loadAccounts();
};

