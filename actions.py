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
    return f"Joined On: {data['personal_details']['joined_on']}"


def _get_employee_health_insurance_policy(data) -> Text:
    return f"Your health policy number is {data['health_policy_number']}"


def _get_monthly_gross_deduction(data) -> Text:
    return f"Your gross deduction is {data['latest_pay_slip']['deductions']['gross_deductions']}"


def _get_monthly_deductions(data) -> Text:
    monthlyDeductions = "Your deductions are: \nProfessional Tax: {0},\nProvident Fund: {1},\n" \
                  "Income Tax: {2},\nParental Medical Insurance: {3}, Gross Deductions: {4}"\
        .format(data["latest_pay_slip"]["deductions"]["professional_tax"],
                data['latest_pay_slip']['deductions']['provident_fund'],
                data['latest_pay_slip']['deductions']['income_tax'],
                data['latest_pay_slip']['deductions']['parental_medical_insurance'],
                data['latest_pay_slip']['deductions']['gross_deductions'])
    return monthlyDeductions


def _get_monthly_earnings(data) -> Text:
    monthly_deductions = "Your earnings are: \nBasic: {0},\nHRA: {1},\nSpecial Allowance: {2},\n" \
                        "PDA: {3},\nstatutory_bonus: {4},\nGross Earnings: {5}\n" \
        .format(data["latest_pay_slip"]["earnings"]["basic"],
                data['latest_pay_slip']['earnings']['hra'],
                data['latest_pay_slip']['earnings']['special_allowance'],
                data['latest_pay_slip']['earnings']['pda'],
                data['latest_pay_slip']['earnings']['statutory_bonus'],
                data['latest_pay_slip']['earnings']['gross_earnings'])
    return monthly_deductions


def _get_reporting_manager(data) -> Text:
    return f"Your reporting manager is {data['reporting_manager']}"


def _get_wifi_password(data) -> Text:
    return "Welcome@123"


def _get_project(data) -> Text:
    return f"Your are assigned to {data['project']}"


def _get_tax_slab(data) -> Text:
    return "New Tax Slab is: {0}\nOld Tax Slab is:{1}".format(data['tax_slab']['new'], data['tax_slab']['old'])


def _latest_ctc(data) -> Text:
    year_ctc = "Your yearly CTC below: \nBasic: {0},\nHRA: {1},\nLTA: {2},\n" \
               "PDA: {3},\nSpecial Allowance: {4},\nEmployer PF: {5},\nGratuity: {6}\n" \
               "Food Plus Card: {7},\nMedical Insurance: {8},\nCost To Company: {9}\n" \
        .format(data["latest_ctc"]["year"]["basic"],
                data['latest_ctc']['year']['hra'],
                data['latest_ctc']['year']['leave_travel_allowance'],
                data['latest_ctc']['year']['pda'],
                data['latest_ctc']['year']['special_allowance'],
                data['latest_ctc']['year']['employer_pf'],
                data['latest_ctc']['year']['gratuity'],
                data['latest_ctc']['year']['food_plus_card'],
                data['latest_ctc']['year']['medical_insurance'],
                data['latest_ctc']['year']['cost_to_company'])
    return year_ctc


def _get_leave_balance(data) -> Text:
    leave_balance = "Your leave balances are: \nEarned Leave: {0},\nCasual Leave: {1},\nTotal Leaves: {2},\n" \
        .format(data["leave_balance"]["earned_leave"],
                data["leave_balance"]["casual_leave"],
                data["leave_balance"]["total_leaves"])
    return leave_balance


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


class ActionHealthPolicy(Action):

    def name(self) -> Text:
        return "action_health_policy"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        response_text = "What is your employee id?"
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = _fetch_employee_details(emp_id)
                response_text = _get_employee_health_insurance_policy(response)

        dispatcher.utter_message(response_text)
        return []


class ActionMonthlyGrossDeduction(Action):

    def name(self) -> Text:
        return "action_monthly_gross_deduction"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        response_text = "What is your employee id?"
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = _fetch_employee_details(emp_id)
                response_text = _get_monthly_gross_deduction(response)

        dispatcher.utter_message(response_text)
        return []


class ActionMonthlyDeductions(Action):

    def name(self) -> Text:
        return "action_monthly_deductions"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        response_text = "What is your employee id?"
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = _fetch_employee_details(emp_id)
                response_text = _get_monthly_deductions(response)

        dispatcher.utter_message(response_text)
        return []


class ActionMonthlyEarnings(Action):

    def name(self) -> Text:
        return "action_monthly_earnings"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        response_text = "What is your employee id?"
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = _fetch_employee_details(emp_id)
                response_text = _get_monthly_earnings(response)

        dispatcher.utter_message(response_text)
        return []


class ActionReportingManager(Action):

    def name(self) -> Text:
        return "action_reporting_manager"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        response_text = "What is your employee id?"
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = _fetch_employee_details(emp_id)
                response_text = _get_reporting_manager(response)

        dispatcher.utter_message(response_text)
        return []


class ActionGuestPassword(Action):

    def name(self) -> Text:
        return "action_guest_password"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']

        dispatcher.utter_message('Guest wifi password is WelcomeAtmecs@123')
        return []


class ActionProject(Action):

    def name(self) -> Text:
        return "action_project"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        response_text = "What is your employee id?"
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = _fetch_employee_details(emp_id)
                response_text = _get_project(response)

        dispatcher.utter_message(response_text)
        return []


class ActionTaxSlab(Action):

    def name(self) -> Text:
        return "action_tax_slab"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        response_text = "What is your employee id?"
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = _fetch_employee_details(emp_id)
                response_text = _get_tax_slab(response)

        dispatcher.utter_message(response_text)
        return []


class ActionLatestCTC(Action):

    def name(self) -> Text:
        return "action_latest_ctc"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        response_text = "What is your employee id?"
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = _fetch_employee_details(emp_id)
                response_text = _latest_ctc(response)

        dispatcher.utter_message(response_text)
        return []


class ActionLeaveBalance(Action):

    def name(self) -> Text:
        return "action_leave_balance"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = tracker.latest_message['entities']
        emp_id = None
        response_text = "What is your employee id?"
        for e in entities:
            if e['entity'] == "emp_id":
                emp_id = e["value"]
                response = _fetch_employee_details(emp_id)
                response_text = _get_leave_balance(response)

        dispatcher.utter_message(response_text)
        return []
'''
def test():
    response = _fetch_employee_details(307)
    monthly_deductions = ''
    print(monthly_deductions)

test()

'''

