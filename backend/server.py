import time
def get_server_list():
    data = [
        {
            "id": "02",
            "ip": "192.160.0.2",
            "used": "",
            "remain": "",
            "children": [
                {
                    "id": "04",
                    "ip": "192.160.0.4",
                    "used": "2.0GB",
                    "remain": "4.0GB",
                },
                {
                    "id": "05",
                    "ip": "192.160.0.5",
                    "used": "2.0GB",
                    "remain": "4.0GB",
                },
                {
                    "id": "06",
                    "ip": "192.160.0.6",
                    "used": "2.0GB",
                    "remain": "4.0GB",
                }
            ]
        }
    ]
    time.sleep(1)
    return data