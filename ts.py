import socket
import sys
import threading

ts_Table = {}

#read ts file
def read():
    domainNames = []

    path = open("PROJI-DNSTS.txt", 'r')

    for i in path:
        i = i.rstrip('\r\n')
        domainNames.append(i)

    path.close()

    return domainNames

#verify port
def verifyPort(userPort):
    userPort = int (userPort)

    if userPort >= 1 and userPort <= 65535:
        return userPort
    else:
        print('port number is out of range')
        exit()


def ts():
    try:
        ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[TS]: Server socket created')
    except socket.error as err:
        print('Socket encountered an erorr while opening')
        exit()

    #call methods and print address
    ts_Port = verifyPort(sys.argv[1])
    path = read()
    address = socket.gethostbyname(socket.gethostname())
    print("Address: {}".format(address))
    print("Port: {}".format(ts_Port))

    #split each line into new table
    for i in path:
        token = i.split()
        ts_Table[token[0].lower()] = i

    #connect
    server_Binding = ('', ts_Port)
    ts.bind(server_Binding)
    ts.listen(1)

    conn, addr = ts.accept()

    #recover data
    while True:
        data = conn.recv(200)
        msg = data.decode('utf-8')

        temp_msg = msg

        #add string to dns accordingly
        if temp_msg.lower() != 'end':
            if temp_msg in ts_Table:
                hold = ts_Table[temp_msg]
                new_msg = ts_Table[temp_msg]
            else:
                new_msg = msg + "- Error: HOST NOT FOUND"
            
            conn.send(new_msg.encode('utf-8'))
        else:
            break
    
    ts.close()
    exit()

if __name__ == "__main__":
    ts = threading.Thread(name='tsServer', target=ts)
    ts.start()
