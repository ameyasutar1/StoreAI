from flask import Flask, render_template, request, jsonify
from AI import main
from ProcessPDF import Reader, extract_json_objects  # Importing Reader from your ProcessPDF module
import os
from AddDataToSQL import add_t_shirt, add_discount

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.form['message']
    bot_message = main(user_message)
    return jsonify({'message': bot_message})

@app.route('/create-bill')
def create_bill():
    return render_template('createBill.html')

@app.route('/add-data', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        file = request.files['upload']
        name = request.form['name']
        price = request.form['price']
        quantity = request.form['quantity']

        # Print the received data to the console for debugging
        print(f"Received data: Name={name}, Price={price}, Quantity={quantity}, File={file.filename}")

        # Return a simple text response for the AJAX call
        return "Data received and printed in the server console!"
    
    return render_template('add_data.html')

@app.route('/analyze-pdf', methods=['POST'])
def analyze_pdf():
    # Check if the request is for uploading a PDF or adding a product
    if 'pdf' in request.files:
        # Handle the PDF upload logic
        uploaded_pdf = request.files.get('pdf')
        
        # Check if a file was uploaded
        if not uploaded_pdf:
            return jsonify({"error": "No PDF file provided"}), 400

        # Save the uploaded file temporarily
        save_directory = r"C:\Users\AM ECOSYSTEMS\OneDrive\Documents\Chatbot\Retail AI Store Bot\retail_SQL_AI\Files"
        pdf_path = os.path.join(save_directory, uploaded_pdf.filename)
        uploaded_pdf.save(pdf_path)

        # Call the Reader function to extract text from the PDF
        extracted_text = Reader(pdf_path)  # Ensure this function is defined elsewhere

        # Extract JSON data from the extracted text
        JsonData = extract_json_objects(extracted_text)

        # Check if JsonData is empty
        if not JsonData or "t_shirts" not in JsonData or not JsonData["t_shirts"]:
            return jsonify({"message": "No valid JSON data found"}), 404  # Return a 404 if no data found
        
        return jsonify(JsonData), 200  # Return the extracted JSON data

    elif request.json and request.json.get('action') == 'add_product':
        # Handle the product addition logic
        product_data = request.json.get('product')

        if product_data:
            print(f"Adding product to database: {product_data}")
            brand = product_data.get("brand")
            price = product_data.get('price')
            color = product_data.get('color')
            size = product_data.get('size')
            stock_quantity = product_data.get('stock_quantity')

            # Validate and convert data types as necessary
            try:
                price = str(price).strip()  # Ensure price is a string
                stock_quantity = str(stock_quantity).strip()  # Ensure stock_quantity is a string
                
                # Call the add_t_shirt function with the converted values
                Discount_Data = add_t_shirt(brand=brand, color=color, price=price, size=size, stock_quantity=stock_quantity)
                if Discount_Data:
                    add_discount(Discount_Data, pct_discount=0.0)  # Assuming you want to add a discount for the newly added t-shirt
                return jsonify({"message": "Product added successfully", "product": product_data}), 200
            
            except Exception as e:
                return jsonify({"error": f"Failed to add product due to error: {str(e)}"}), 500
        else:
            return jsonify({"error": "No product data provided"}), 400

    return jsonify({"error": "Invalid request"}), 400  # Catch-all for invalid requests

if __name__ == '__main__':
    app.run(debug=True)
