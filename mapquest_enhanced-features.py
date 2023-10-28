import urllib.parse
import requests
from colorama import Fore, Style
from prettytable import PrettyTable

main_api = "https://www.mapquestapi.com/directions/v2/route?"
key = "qgRrjbF8jCCk9eNSco0mNKZFxHRd4EGX"

class Colors:
    RED = Fore.RED
    GREEN = Fore.GREEN
    RESET = Style.RESET_ALL

def display_colored_step_by_step(route_data):
    print("Step-by-Step Directions:")
    step_table = PrettyTable(["Step", "Directions", "Distance (miles)", "Distance (km)"])
    step_table.align["Step"] = "l"
    step_table.align["Directions"] = "l"
    step_table.align["Distance (miles)"] = "r"
    step_table.align["Distance (km)"] = "r"

    for i, step in enumerate(route_data["route"]["legs"][0]["maneuvers"], start=1):
        color = Colors.GREEN if i % 2 == 0 else Colors.RED
        step_table.add_row([i, step['narrative'], f"{step['distance']:.2f}", f"{step['distance'] * 1.61:.2f}"])
        print(f"{color}{i}. {step['narrative']} ({step['distance']:.2f} miles / {step['distance'] * 1.61:.2f} km){Colors.RESET}")

    print(step_table)
    print("=============================================")

while True:
    orig = input("Starting Location: ")
    if orig.lower() in ["quit", "q"]:
        break

    dest = input("Destination: ")
    if dest.lower() in ["quit", "q"]:
        break

    url = main_api + urllib.parse.urlencode({"key": key, "from": orig, "to": dest})
    print("URL: " + url)

    json_data = requests.get(url).json()
    json_status = json_data["info"]["statuscode"]

    if json_status == 0:
        print("API Status: " + str(json_status) + " = A successful route call.\n")
        print("=============================================")
        print("Directions from " + orig + " to " + dest)
        print("Trip Duration:   " + json_data["route"]["formattedTime"])
        print("Miles:           " + str(json_data["route"]["distance"]))
        print("Kilometers:      " + str("{:.2f}".format(json_data["route"]["distance"] * 1.61)))

        # Additional Enhancements
        print("\nAdditional Features:")
        display_colored_step_by_step(json_data)  # Step-by-step directions
        print("2. UI Enhancement: Colored output for step-by-step directions and a table format")
        print("3. Additional Options: Provide data in the metric system or miles")
        unit_choice = input("Choose unit (M for miles, K for kilometers): ").upper()
        if unit_choice == "M":
            print(f"Distance: {json_data['route']['distance']:.2f} miles")
        elif unit_choice == "K":
            print(f"Distance: {json_data['route']['distance'] * 1.61:.2f} kilometers")
        else:
            print("Invalid choice. Distance displayed in miles by default.")

        print("=============================================\n")

    else:
        print("************************************************************************")
        print("For Status Code: " + str(json_status) + "; Refer to:")
        print("https://developer.mapquest.com/documentation/directions-api/status-codes")
        print("************************************************************************\n")
