import time
import socket
import re
import json
import sys
from datetime import datetime

def __init__(self, url, port=80):
    self.url = url
    self.port = port

def dtu_http_request(url, port=80):
    # create a socket object
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect the client
    client.connect((url, port)) 

    # get current timestamp in millis
    current_milli_time = lambda: int(round(time.time() * 1000))

    try:
        # send data
        request = f"GET /hometable.xml?_t={current_milli_time()} HTTP/1.1\r\nHost:%s\r\n\r\n" % url
        client.send(request.encode())

        # receive some data
        response = client.recv(4096)

        # processing response
        json = array_to_json(response)

        # returning json
        return json
    except Exception:
        return None

def array_to_json(response):
    try:
        splited = str(response).split(';')
        data = {}
        data['current_power_total'] = {"value": splited[0].strip('b\''), "unit": "kW" }
        data['full_power_total'] = {"value": splited[1], "unit": "kWh" }
        data['energy_today'] = {"value": splited[2], "unit": "kWh" }
        data['co2_saved'] = {"value": splited[3], "unit": "kg" }
        data['panels_online'] = splited[7]
        data['inverters'] = []
        if '01' in splited[5]:
            j = 11
            t = 0
            count = 0
            while t < int(splited[4]):
                panel_voltage = re.sub(r"[^0-9\.]", "", splited[j+t*8+2])
                grid_voltage = re.sub(r"[^0-9\.]", "", splited[j+t*8+3])
                grid_frequency = re.sub(r"[^0-9\.]", "", splited[j+t*8+4])
                panel_power = re.sub(r"[^0-9\.]", "",  splited[j+t*8+5])
                energy_today = re.sub(r"[^0-9\.]", "",  splited[j+t*8+6])
                panel_temperature = re.sub(r"[^0-9\.]", "",  splited[j+t*8+7])
                if t == 0 or (splited[j+t*8+1][:12] != splited[j+(t-1)*8+1][:12]):
                    data['inverters'].append({
                        "id": splited[j+t*8+1][:12],
                                    "channels": [{
                                                    "channel": splited[j+t*8+1][-1],
                                                    "panelvoltage": {"value": float(panel_voltage), "unit": "V" },
                                                    "gridvoltage": {"value": float(grid_voltage), "unit": "V" },
                                                    "gridfrequency": {"value": float(grid_frequency), "unit": "Hz" },
                                                    "panelpower": {"value": float(panel_power), "unit": "W" },
                                                    "energytoday": {"value": float(energy_today), "unit": "Wh" },
                                                    "temperature": {"value": float(panel_temperature), "unit": "C" },
                                                    "date": splited[j+t*8+8]
                                                }]
                            })
                    count = count + 1
                else:
                    data['inverters'][count - 1]['channels'].append({
                                                    "channel": splited[j+t*8+1][-1],
                                                    "panelvoltage": {"value": float(panel_voltage), "unit": "V" },
                                                    "gridvoltage": {"value": float(grid_voltage), "unit": "V" },
                                                    "gridfrequency": {"value": float(grid_frequency), "unit": "Hz" },
                                                    "panelpower": {"value": float(panel_power), "unit": "W" },
                                                    "energytoday": {"value": float(energy_today), "unit": "Wh" },
                                                    "temperature": {"value": float(panel_temperature), "unit": "C" },
                                                    "date": splited[j+t*8+8]
                            })
                t = t+1
        jsonStr = json.dumps(data, indent=4)
        return jsonStr
    except Exception:
        return None
