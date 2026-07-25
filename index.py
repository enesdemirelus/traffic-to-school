import os
import requests
from dotenv import load_dotenv
import csv
from datetime import datetime

load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API")

def get_data():
    url = "https://routes.googleapis.com/directions/v2:computeRoutes"


    home = os.getenv("HOME_ADDRESS")
    lpc = os.getenv("LPC_ADDRESS")
    loop = os.getenv("LOOP_ADDRESS")


    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": API_KEY,
        "X-Goog-FieldMask": "routes.duration,routes.distanceMeters,routes.staticDuration",
    }

    home_to_lpc = {
        "origin": {"address": f"{home}"},
        "destination": {"address": f"{lpc}"},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
        "computeAlternativeRoutes": True,
    }

    home_to_loop = {
        "origin": {"address": f"{home}"},
        "destination": {"address": f"{loop}"},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
        "computeAlternativeRoutes": True,
    }

    lpc_to_home = {
        "origin": {"address": f"{lpc}"},
        "destination": {"address": f"{home}"},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
        "computeAlternativeRoutes": True,
    }

    loop_to_home = {
        "origin": {"address": f"{loop}"},
        "destination": {"address": f"{home}"},
        "travelMode": "DRIVE",
        "routingPreference": "TRAFFIC_AWARE_OPTIMAL",
        "computeAlternativeRoutes": True,
    }


    home_to_lpc_r = requests.post(url, headers=headers, json=home_to_lpc)
    home_to_loop_r = requests.post(url, headers=headers, json=home_to_loop)
    lpc_to_home_r = requests.post(url, headers=headers, json=lpc_to_home)
    loop_to_home_r = requests.post(url, headers=headers, json=loop_to_home)


    home_to_lpc_data = home_to_lpc_r.json()
    home_to_loop_data = home_to_loop_r.json()
    lpc_to_home_data = lpc_to_home_r.json()
    loop_to_home_data = loop_to_home_r.json()



    home_to_lpc_route = min(home_to_lpc_data["routes"], key=lambda x: int(x["duration"].rstrip("s")))
    home_to_loop_route = min(home_to_loop_data["routes"], key=lambda x: int(x["duration"].rstrip("s")))
    lpc_to_home_route = min(lpc_to_home_data["routes"], key=lambda x: int(x["duration"].rstrip("s")))
    loop_to_home_route = min(loop_to_home_data["routes"], key=lambda x: int(x["duration"].rstrip("s")))


    home_to_lpc_traffic_sec = int(home_to_lpc_route["duration"].rstrip("s"))
    home_to_loop_traffic_sec = int(home_to_loop_route["duration"].rstrip("s"))
    lpc_to_home_traffic_sec = int(lpc_to_home_route["duration"].rstrip("s"))
    loop_to_home_traffic_sec = int(loop_to_home_route["duration"].rstrip("s"))
    
    return [home_to_lpc_traffic_sec, home_to_loop_traffic_sec, lpc_to_home_traffic_sec, loop_to_home_traffic_sec]



if __name__ == "__main__":
    try:
        hl, hlo, lh, loh = get_data()
    except Exception as e:
        with open("error.log", "a") as f:
            f.write(f"{datetime.now().isoformat()} FAILED: {e}\n")
        raise SystemExit(1)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    row = [date_str, time_str, hl, hlo, lh, loh]

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "commute_log.csv")
    file_exists = os.path.exists(path)

    with open(path, "a", newline="") as f:
        w = csv.writer(f)
        if not file_exists:
            w.writerow(["date", "time", "home_to_lpc", "home_to_loop", "lpc_to_home", "loop_to_home"])
        w.writerow(row)
