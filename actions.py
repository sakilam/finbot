from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

ENDPOINT = {
    "base": "https://finbot-back-end.herokuapp.com/api/employees/{}"
}

def _create_path(value: Text) -> Text:
    return ENDPOINT["base"].format(value)

def _fetch_employee_details(value: Text) -> Text:
    return requests.get(_create_path(value)).json()

def _employee_personal_details(data) -> Text:
    emp_data = "Employee Name: " + data["personal_details"]["emp_name"] + "\n"
    emp_data += "First Name: " + data["personal_details"]["first_name"] + "\n"
    emp_data += "Last Name: " + data["personal_details"]["last_name"] + "\n"
    emp_data += "Gender: " + data["personal_details"]["gender"] + "\n"
    emp_data += "Email: " + data["personal_details"]["email"] + "\n"
    emp_data += "Designation: " + data["personal_details"]["designation"] + "\n"
    emp_data += "Date of Birth: " + data["personal_details"]["dob"] + "\n"
    emp_data += "PAN Number: " + data["personal_details"]["pan_no"] + "\n"
    emp_data += "Company Location: " + data["personal_details"]["company_location"] + "\n"
    emp_data += "Part Time/Full Time: " + data["personal_details"]["parttime_fulltime"] + "\n"
    emp_data += "Joined On: " + data["personal_details"]["joined_on"] + "\n"
    return emp_data

def _employee_joining_date(data) -> Text:
    return "Joined On: " + data["personal_details"]["joined_on"]


class ActionPersonalDetails(Action):

    def name(self) -> Text:
        return "action_personal_details"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        response_text = "What is your employee id?"
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = _fetch_employee_details(emp_id)
                response_text = _employee_personal_details(response)

        dispatcher.utter_message(response_text)
        return []

class ActionJoiningDate(Action):

    def name(self) -> Text:
        return "action_joining_date"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        response_text = "What is your employee id?"
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = _fetch_employee_details(emp_id)
                response_text = _employee_joining_date(response)

        dispatcher.utter_message(response_text)
        return []
