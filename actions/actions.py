from rasa_sdk import Action
from rasa_sdk.events import SlotSet
import mysql.connector

class ActionQueryCategory(Action):
    def name(self):
        return "action_query_category"

    def run(self, dispatcher, tracker, domain):
        state = tracker.get_slot('state')
        district = tracker.get_slot('district')
        assessment_unit_name = tracker.get_slot('assessment_unit_name')

        # Connect to MySQL and run your query here
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="12345",
            database="waterbuddy"
        )
        cursor = connection.cursor()
        
        query = "SELECT categorization FROM aol_23 WHERE state = %s AND district = %s AND assessment_unit_name = %s"
        cursor.execute(query, (state, district, assessment_unit_name))
        
        result = cursor.fetchone()
        
        if result:
            category = result[0]
            dispatcher.utter_message(text=f"The category of your area is: {category}.")
        else:
            dispatcher.utter_message(text="I'm sorry, I couldn't find that information.")

        cursor.close()
        connection.close()

        return []
