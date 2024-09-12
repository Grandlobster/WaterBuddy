# Import necessary libraries
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import pandas as pd

# Define the custom action
class ActionQueryGroundwaterData(Action):

    def name(self) -> Text:
        return "action_query_groundwater_data"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Load the Excel file into a pandas DataFrame
        df = pd.read_excel("/path/to/your/excel/file.xlsx")  # Provide the correct path to your file

        # Fetch the latest user message
        user_message = tracker.latest_message['text'].lower()

        # Example: Handle a query for the state
        if "state" in user_message:
            # Extract the state from the user message (you can use more robust NLP to do this)
            state = self.extract_state(user_message)
            
            # Filter the DataFrame by the specified state
            results = df[df['State'].str.contains(state, case=False, na=False)]
            
            if not results.empty:
                # Format the result to send to the user
                response = "Here is the groundwater status for the state of {}:\n".format(state)
                for _, row in results.iterrows():
                    response += "District: {}, Assessment Unit: {}, Categorization: {}\n".format(
                        row['District'], row['Assessment Unit Name'], row['Categorization (Over- ExploitedE/Critical/ Semi- Critical/Safe/Saline)'])
                dispatcher.utter_message(response)
            else:
                dispatcher.utter_message(f"Sorry, I couldn't find any information for the state {state}.")
        
        # Additional conditions for district or specific unit queries can be handled similarly
        
        return []

    def extract_state(self, message: Text) -> Text:
        # Dummy function to extract the state from the user message (improve this with actual NLP logic)
        # For example, you could extract using pre-trained models or keyword matching
        # Here we will use a simple example where the state is the last word of the message
        return message.split()[-1]
