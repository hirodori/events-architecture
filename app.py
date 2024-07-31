from flask import Flask, request, render_template_string, flash, render_template, redirect, url_for
from order import Order
import sqlite3  # Make sure order.py is in the same directory or adjust the import path

app = Flask(__name__)

# HTML form

def getValues():
    conn = sqlite3.connect('stock_data.db')
    cursor = conn.cursor()

    # SQL query to find the items by ID from 1 to 10
    query = "SELECT * FROM STOCK_DATA WHERE id BETWEEN 1 AND 10"
    cursor.execute(query)

    # Fetch all results
    results = cursor.fetchall()
    conn.close()

    return results

@app.route('/', methods=['GET', 'POST'])
def order_form():

    values = []
    values = getValues()

    if request.method == 'POST':
        # Extract form data
        order_id = request.form['id']
        quantity = request.form['quantity']

        values = getValues()
        print(values)
        
        # Construct order dictionary
        order = {
            'id': int(order_id),
            'quantity': int(quantity)
        }
        
        # Send order
        rabbitmq_publisher = Order()
        rabbitmq_publisher.send_message(order)

        return redirect(url_for('order_form'))
        
        #return render_template('index.html', values=values)

    
    return render_template('index.html', values=values)

if __name__ == '__main__':
    app.run(debug=True)
