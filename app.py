

from flask import Flask, render_template, render_template_string, request, session, redirect, url_for
from tiramisu_wallet_client import TiramisuClient

app = Flask(__name__)

app.secret_key = 'TestSecretKey123456'

USERNAME = 'USERNAME_HERE'
PASSWORD = 'PASSWORD_HERE'
ASSET_ID = 3
PRICE = 30

@app.route("/", methods=['GET', 'POST'])
def index():
    
    client = TiramisuClient(username=USERNAME,password=PASSWORD)
    asset = client.asset(ASSET_ID)
    return render_template("index.html",  asset_acronym=asset["acronym"],asset_id=ASSET_ID, price = PRICE)

@app.route("/checkout", methods=['GET', 'POST'])
def checkout():
    
    client = TiramisuClient(username=USERNAME,password=PASSWORD)
    transaction = client.transactions_receive_taproot_asset(amount=PRICE, asset=ASSET_ID, description="Test purchase of a nice dog.")
    
    session['transaction_id'] = transaction['id']
    
    return redirect(url_for('payment'))
    
@app.route("/payment", methods=['GET', 'POST'])
def payment():
    
    transaction_id = session.get('transaction_id')
    
    if not transaction_id:
        return 404, "No transaction id found."
    
    client = TiramisuClient(username=USERNAME,password=PASSWORD)
    transaction = client.transaction(id=transaction_id)
    
    transaction_status = transaction['status']
    status_description = transaction['status']
    
    if transaction_status=="inbound_invoice_waiting_for":
        payment_status_details = f"""
        <h2>Transaction status: waiting for invoice</h2>
        <img src="/static/wait.png" alt="Wait Image">
        <p>Tiramisu wallet backend is generating an invoice now</p>
        """
    elif transaction_status=="inbound_invoice_generated":
        payment_status_details = f"""
        <h2>Transaction status: invoice is waiting to be paid</h2>
        <img src="/static/invoice.png" alt="Wait Image">
        <p>Please pay the Taproot asset invoice below:</p>
        <b>{transaction['invoice_inbound']}</b>
        """
    elif transaction_status=="inbound_invoice_paid" or transaction_status=="replaced_with_internal_transaction":
        payment_status_details = f"""
        <h2>Transaction status: success</h2>
        <img src="/static/success.png" alt="Success Image">
        <p>The invoice was successfully paid. Thank you for purchasing our product!</p>
        <a href="/" class="btn btn-primary"><button>Go back home</button></a>
        """
    elif transaction_status=="error":
        payment_status_details = f"""
        <h2>Transaction status: error</h2>
        <img src="/static/error.png" alt="Error Image">
        <p>Got the following error:</p>
        {status_description}
        <a href="/" class="btn btn-primary"><button>Go back home</button></a>
        """
    else:
        return 404, f"Unknown status {transaction_status}. Error processing the transaction."
    
    return render_template("payment.html",payment_status_details=payment_status_details, price = PRICE)

if __name__ == "__main__":
    app.run()