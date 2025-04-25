from flask import Flask, session, jsonify, request, render_template, redirect
from account import BankAccount
from transaction import Transaction
from transaction_queue import TransactionQueue

app = Flask(__name__)
app.secret_key = "supersecretkey"  
tx_queue = TransactionQueue()

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")

# In-memory accounts dictionary (same as in your CLI)
accounts = {
    "A001": BankAccount("A001", "Alice", 500),
    "A002": BankAccount("A002", "Bob", 300)
}

# Define an API to return all accounts
@app.route("/api/accounts", methods=["GET"])
def get_accounts():
    result = []
    for acc_id, acc in accounts.items():
        result.append({
            "id": acc.account_id,
            "name": acc.name,
            "balance": acc.balance
        })
    return jsonify(result)
    
@app.route("/api/accounts", methods=["POST"])
def create_account():
    data = request.get_json()
    account_id = data.get("id")
    name = data.get("name")
    balance = data.get("balance", 0)

    if account_id in accounts:
        return jsonify({"error": "Account ID already exists."}), 400

    accounts[account_id] = BankAccount(account_id, name, balance)
    return jsonify({"message": f"Account {account_id} created for {name} with balance ${balance}"}), 201

@app.route("/api/transactions", methods=["POST"])
def add_transaction():
    data = request.get_json()
    tx_type = data.get("tx_type")
    account_id = data.get("account_id")
    amount = data.get("amount")
    target_id = data.get("target_id")  # can be None

    if tx_type not in ("deposit", "withdraw", "transfer"):
        return jsonify({"error": "Invalid transaction type."}), 400

    if account_id not in accounts:
        return jsonify({"error": f"Account {account_id} not found."}), 404

    if tx_type == "transfer" and not target_id:
        return jsonify({"error": "Missing target_id for transfer."}), 400

    tx = Transaction(tx_type, account_id, amount, target_id)
    tx_queue.enqueue(tx)
    return jsonify({"message": f"{tx_type.title()} added to queue"}), 201

@app.route("/api/process", methods=["POST"])
def process_transactions():
    results = []

    while not tx_queue.is_empty():
        tx = tx_queue.dequeue()
        result = {"transaction": str(tx)}

        if tx.account_id not in accounts:
            result["status"] = "Failed"
            result["reason"] = "Source account not found"
        elif tx.tx_type == "deposit":
            accounts[tx.account_id].deposit(tx.amount)
            result["status"] = "Success"
        elif tx.tx_type == "withdraw":
            success = accounts[tx.account_id].withdraw(tx.amount)
            result["status"] = "Success" if success else "Failed"
            if not success:
                result["reason"] = "Insufficient balance"
        elif tx.tx_type == "transfer":
            if tx.target_id not in accounts:
                result["status"] = "Failed"
                result["reason"] = "Target account not found"
            else:
                success = accounts[tx.account_id].transfer(accounts[tx.target_id], tx.amount)
                result["status"] = "Success" if success else "Failed"
                if not success:
                    result["reason"] = "Insufficient balance"

        results.append(result)

    return jsonify(results)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        if email == "admin@example.com" and password == "password":
            session["user"] = email
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="❌ Invalid email or password.")

    return render_template("login.html")



@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

# Start the Flask server
if __name__ == "__main__":
    app.run(debug=True)