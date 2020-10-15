import socket
import threading
import pickle
import requests

HEADER = 1024000000
PORT = 5005
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"
FETCH_API = {
    1:"https://disease.sh/v3/covid-19/all",
    2:"https://disease.sh/v3/covid-19/countries?sort=cases",
    3:"https://disease.sh/v3/covid-19/continents?sort=cases",
    4:"https://disease.sh/v3/covid-19/countries/",
    5:"http://disease.sh/v3/covid-19/continents/",
    6:"https://disease.sh/v3/covid-19/historical/",
    7:"https://disease.sh/v3/covid-19/vaccine",
}



server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)




def fetch_data(msg):
    type = msg.get("type")
    url = FETCH_API[type]
    if type == 1:
        unprocessed_data = requests.get(url)

        return unprocessed_data.json()


    elif type == 2:
        unprocessed_data = requests.get(url)
        processed_data = []
        temp = {}
        for item in unprocessed_data.json():
            temp["country"] = item.get("country")
            temp["cases"] = item.get("cases")
            temp["todayCases"]  = item.get("todayCases")
            temp["deaths"] = item.get("deaths")
            temp["todayDeaths"] = item.get("todayDeaths")
            temp["recovered"] = item.get("recovered")
            temp["todayRecovered"] = item.get("todayRecovered")
            temp["tests"] = item.get("tests")
            processed_data.append(temp)
            temp = {}


        return processed_data

    elif type==3:
        unprocessed_data = requests.get(url)
        processed_data = []
        temp = {}
        
        val = unprocessed_data.json();

        for item in val:

            temp["continent"] = item.get("continent")
            temp["cases"] = item.get("cases")
            temp["todayCases"]  = item.get("todayCases")
            temp["deaths"] = item.get("deaths")
            temp["todayDeaths"] = item.get("todayDeaths")
            temp["recovered"] = item.get("recovered")
            temp["todayRecovered"] = item.get("todayRecovered")
            temp["tests"] = item.get("tests")
            processed_data.append(temp)
            temp = {}

        return processed_data

    elif type == 4:
        url = url+str(msg.get("country"))
        processed_data = requests.get(url)
        return processed_data.json()
    elif type == 5:
        url = url+str(msg.get("continent"))
        processed_data = requests.get(url)
        return processed_data.json()
    elif type==6:
        url = url +  str(msg.get("country"))+"?lastdays="+str(msg.get("days"))
        processed_data = requests.get(url)
        return processed_data.json()
    elif type == 7:
        unprocessed_data = requests.get(url)
        processed_data = unprocessed_data.json()["data"][0]
        return processed_data







    print(url)






def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:

        msg = pickle.loads(conn.recv(HEADER))
        print(msg)

        if type(msg["type"] == "string") and msg["type"] == DISCONNECT_MESSAGE:
            connected = False
            conn.send(pickle.dumps("disconnecting"))
        else:

            print(f"[{addr}] {msg}")
            data = fetch_data(msg)
            conn.send(pickle.dumps(data))

    conn.close()



def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")


print("[STARTING] server is starting...")
start()
