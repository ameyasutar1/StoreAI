# **Inventory SmartBot**

## **Overview**

**Inventory SmartBot** is an AI-driven chatbot designed to streamline inventory management. It allows users to interact with the system using natural language to retrieve data or add new inventory. By interpreting user queries, the chatbot generates and executes SQL queries on the backend database. The system also allows users to upload PDF invoices to automatically extract, validate, and add data into the inventory after confirmation.

## **Key Features**

1. **Natural Language Querying**: 
   - Users can ask questions like "What is the current stock of item X?" or "Show me the inventory for product Y."
   - The bot automatically generates SQL queries to fetch the requested data from the inventory database.

2. **PDF Upload and Data Addition**:
   - Users can upload PDF invoices containing inventory data.
   - The AI extracts the data, converts it into JSON, validates it according to the SQL schema, and presents it for user confirmation before updating the database.

3. **Error Correction and Data Validation**:
   - If the uploaded data contains errors or deviates from the required format, the bot automatically corrects and formats it based on predefined rules.

4. **SQL Query Generation**:
   - The chatbot automatically translates natural language input into SQL queries, making the interaction seamless and intuitive for non-technical users.

5. **Formatted Responses**:
   - The system presents inventory data in a user-friendly, formatted output.

## **Technology Stack**

- **Backend**: Python with Flask
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQL (for managing inventory data)
- **AI/NLP**: For interpreting natural language queries and converting them into SQL queries.
- **PDF Parsing**: Libraries like `PyPDF2` or `pdfminer` are used to extract structured data from PDF invoices.
- **JSON**: For data validation and parsing.

## **Project Structure**
*InventorySmartBot*

│
├── app.py                  
├── templates/              
│   └── index.html           
├── static/                 
│   └── style.css            
├── README.md               
├── requirements.txt        
└── database/               
    └── inventory.sql        
## **Installation and Setup**

**Clone the Repository**:
   ```bash
   git clone https://github.com/ameyasutar1/StoreAI.git
   ```

### **Navigate to the Project Directory**:

```bash
cd InventorySmartBot
```

### **Install Dependencies**:

Ensure Python is installed. Run the following command to install the required packages:

```bash
pip install -r requirements.txt
```

### **Set up the Database**:

1. Use the SQL schema provided in `database/inventory.sql` to set up your SQL database.
2. Configure the database connection in `app.py`.

### **Run the Application**:

Start the Flask server:

```bash
python app.py
```

### **Access the Application**:

Open your browser and go to `http://127.0.0.1:5000` to interact with the chatbot.

---

### **Usage**

#### Asking Queries:

You can type in questions such as:

- "What is the current stock of product X?"
- "Show me all items low on stock."

The AI will interpret the query, generate the corresponding SQL query, and return the requested data.

#### Adding Data via PDF:

1. Click the **"Upload Invoice"** button in the chatbot interface.
2. Select a PDF file containing inventory data (e.g., a supplier invoice).
3. The AI will scrape the data, format it into JSON, and validate it against the SQL table structure.
4. A preview of the data will be shown for your confirmation before it is uploaded to the database.

---

### **Contributing**

We welcome contributions! Feel free to fork the repository and create a pull request with improvements or new features. If you plan to make significant changes, please open an issue first to discuss your ideas.

---

### **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---



