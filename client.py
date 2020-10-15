import socket
import pickle

HEADER = 64
PORT = 5005
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "172.20.10.2"
ADDR = (SERVER, PORT)
FLAG = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg,message):
    client.send(msg)
    data =  pickle.loads(client.recv(1024000000))
    if data == "disconnecting":
        print("disconnecting....")
        exit()
    
    try:
        if message["type"] == 2 or message["type"] == 3:
            for i in data:
                print("\n")

                for key,value in i.items():
                    print(key ," - " ,value)

        else:
            for object in data:
                print(str(object) + " - " + str(data.get(object)))
    except:
        print("\nsome error")



print("\n\n\n                     COVID-19 REST API               \n\n\n")
print("Queries :: ")
print("1 - Worldwide\n")
print("2 - All Countries\n")
print("3 - All Continents\n")
print("4 - Specific Country\n")
print("5 - Specific Continent\n")
print("6 - Specific Country History\n")
print("7 - Recent Vaccine Update\n")
print("press any alphabet to exit\n")


while True:
    request = {}
    try:
        types = int(input("\nEnter the  Query: "))
        request["type"] = types
    except:
        types = "DISCONNECT"
        request["type"] = types
        data = pickle.dumps(request)
        send(data,request)
        exit()

    if(types == 4):
        country = input("Enter the country: ")
        request["country"] = country
    elif types == 5:
        continent = input("Enter the continent name: ")
        request["continent"] = continent
    elif types == 6:
        request["country"] = input("Enter  the  country: ")
        request["days"] = int(input("Enter no. of days: "))

    data = pickle.dumps(request)
    send(data,request)








