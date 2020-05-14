from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionPersonalDetails(Action):

    def name(self) -> Text:
        return "action_personal_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = requests.get("https://finbot-back-end.herokuapp.com/api/employees/" + emp_id).json()
                response_text = "Employee Name: " + response["personal_details"]["emp_name"] + "\n"
                response_text += "First Name: " + response["personal_details"]["first_name"] + "\n"
                response_text += "Last Name: " + response["personal_details"]["last_name"] + "\n"
                response_text += "Gender: " + response["personal_details"]["gender"] + "\n"
                response_text += "Email: " + response["personal_details"]["email"] + "\n"
                response_text += "Designation: " + response["personal_details"]["designation"] + "\n"
                response_text += "Date of Birth: " + response["personal_details"]["dob"] + "\n"
                response_text += "PAN Number: " + response["personal_details"]["pan_no"] + "\n"
                response_text += "Company Location: " + response["personal_details"]["company_location"] + "\n"
                response_text += "Part Time/Full Time: " + response["personal_details"]["parttime_fulltime"] + "\n"
                response_text += "Joined On: " + response["personal_details"]["joined_on"] + "\n"

        dispatcher.utter_message(response_text)
        return []
