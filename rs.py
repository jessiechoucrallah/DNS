import socket
import sys
import threading

rs_Table = {}
rs_Host = ""

#read ts file
def read():
    domainNames = []

    path = open("PROJI-DNSRS.txt", 'r')

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

def rs():
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print('[RS]: Server socket created')
    except socket.error as err:
        print('Socket encountered an erorr while opening')
        exit()

    #call methods and print address
    rs_Port = verifyPort(sys.argv[1])
    path = read()
    address = socket.gethostbyname(socket.gethostname())
    print("Address: {}".format(address))
    print("Port: {}".format(rs_Port))

    #split each line into new table
    for i in path:
        token = i.split()

        if token[2] == 'NS':
            rs_Host = i
        else:
            rs_Table[token[0].lower()] = i

    #connect
    server_Binding = ('', rs_Port)
    rs.bind(server_Binding)
    rs.listen(1)

    conn, addr = rs.accept()

    #recover data
    while True:
        data = conn.recv(200)
        msg = data.decode('utf-8')

        temp_msg = msg.lower()

        #check if line in table
        if temp_msg.lower() != 'end':
            #send msg if in table
            if temp_msg in rs_Table:
                hold = rs_Table[temp_msg]
                conn.send(hold.encode('utf-8'))
            #send domain to ts
            else:
                conn.send(rs_Host.encode('utf-8'))
            
        else:
            break
    
    rs.close()
    exit()

if __name__ == "__main__":
    rs = threading.Thread(name='rsServer', target=rs)
    rs.start()
