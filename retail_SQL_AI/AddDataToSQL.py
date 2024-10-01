import mysql.connector
from mysql.connector import Error

# Database connection parameters
db_user = "root"
db_password = "Aj213778*"
db_host = "localhost"
db_name = "Amv_Tshirts"

def create_connection():
    """Create a database connection."""
    try:
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def is_valid_t_shirt_data(brand, color, size, price, stock_quantity):
    """Validate t-shirt data before insertion."""
    valid_brands = ['Van Huesen', 'Levi', 'Nike', 'Adidas']
    valid_colors = ['Red', 'Blue', 'Black', 'White']
    valid_sizes = ['XS', 'S', 'M', 'L', 'XL']
    
    try:
        # Strip whitespace and convert types
        price = float(price.strip())
        stock_quantity = int(stock_quantity.strip())
        
        if not (10 <= price <= 50):
            print("Price must be between 10 and 50.")
            return False
            
        if stock_quantity < 0:
            print("Stock quantity cannot be negative.")
            return False
            
        # Check if brand, color, and size are valid
        if brand.strip() not in valid_brands:
            print("Invalid brand. Must be one of: " + ", ".join(valid_brands))
            return False
            
        if color.strip() not in valid_colors:
            print("Invalid color. Must be one of: " + ", ".join(valid_colors))
            return False
        
        if size.strip() not in valid_sizes:
            print("Invalid size. Must be one of: " + ", ".join(valid_sizes))
            return False
        
        return True
    except ValueError:
        print("Invalid input: Price and stock quantity must be numeric.")
        return False

def is_valid_discount_data(t_shirt_id, pct_discount):
    """Validate discount data."""
    if not isinstance(t_shirt_id, int) or t_shirt_id <= 0:
        print("T-shirt ID must be a positive integer.")
        return False
    if not isinstance(pct_discount, (int, float)) or not (0 <= pct_discount <= 100):
        print("Discount percentage must be between 0 and 100.")
        return False
    return True

def add_t_shirt(brand, color, size, price, stock_quantity):
    """Insert a new t-shirt into the t_shirts table."""
    if not is_valid_t_shirt_data(brand, color, size, price, stock_quantity):
        return

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO t_shirts (brand, color, size, price, stock_quantity)
        VALUES (%s, %s, %s, %s, %s)
        """
        
        # Prepare values
        values = (brand.strip(), color.strip(), size.strip(), float(price.strip()), int(stock_quantity.strip()))

        try:
            cursor.execute(sql_insert_query, values)
            connection.commit()
            print("T-shirt added successfully")
            # Retrieve the newly created t_shirt_id
            t_shirt_id = cursor.lastrowid
            return t_shirt_id  # Return the id for further use
        except Error as e:
            print(f"Failed to insert record into t_shirts table: {e}")
        finally:
            cursor.close()
            connection.close()

def add_discount(t_shirt_id, pct_discount):
    """Insert a new discount into the discounts table."""
    if not is_valid_discount_data(t_shirt_id, pct_discount):
        return

    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        sql_insert_query = """
        INSERT INTO discounts (t_shirt_id, pct_discount)
        VALUES (%s, %s)
        """
        values = (t_shirt_id, pct_discount)

        try:
            cursor.execute(sql_insert_query, values)
            connection.commit()
            print("Discount added successfully")
        except Error as e:
            print(f"Failed to insert record into discounts table: {e}")
        finally:
            cursor.close()
            connection.close()

# Example usage
# Ensure values are within valid ranges
t_shirt_id = add_t_shirt(brand="Levi", color="Blue", price="30", size="L", stock_quantity="3")
if t_shirt_id:
    add_discount(t_shirt_id, pct_discount=15.0)  # Assuming you want to add a discount for the newly added t-shirt
