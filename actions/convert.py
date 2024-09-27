import mysql.connector

# Database connection setup
def connect_to_database():
    connection = mysql.connector.connect(
        host="localhost",  # Your database host (your machine's hostname)
        user="root",  # Your MySQL username
        password="12345",  # Your MySQL password
        database="waterbuddy"  # Your MySQL database name
    )
    return connection

def get_area_categorization(state, district, assessment_unit_name):
    try:
        connection = connect_to_database()
        cursor = connection.cursor()

        # SQL Query to fetch categorization based on state, district, and assessment_unit_name
        query = """
        SELECT assessment_unit_name, categorization
        FROM aol_24
        WHERE state = %s AND district = %s AND assessment_unit_name = %s
        """
        cursor.execute(query, (state, district, assessment_unit_name))
        result = cursor.fetchall()

        # If results are found
        if result:
            for row in result:
                area_name, categorization = row
                print(f"Categorization of your area '{area_name}' is: {categorization}")
        else:
            print("No data found for the given state, district, and Taluka.")

        cursor.close()
        connection.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")

# Ask for user input
state = input("Enter state name: ")
district = input("Enter district name: ")
assessment_unit_name = input("Enter Taluka (assessment unit name): ")

# Fetch and display area categorization
get_area_categorization(state, district, assessment_unit_name)
