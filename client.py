import sys
import socket
import threading
import time

results = []

# Create a second socket to connect to ts
def read():
    domainNames = []
    
    path = open('PROJI-HNS.txt', 'r')

    #format each line
    for i in path:
        i = i.rstrip('\r\n')
        domainNames.append(i.lower())
    
    path.close()

    return domainNames


# Verify port is in range
def verifyPort(userPort):
    userPort = int (userPort)

    if userPort >= 1 and userPort <= 65535:
        return userPort
    else:
        print('port number is out of range')
        exit()


def client():
    try:
        rs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error as err:
        print('Socket open error: {} \n'.format(err))
        exit()
        
    #retrieve ports and domain
    hostname = sys.argv[1]
    rsPort = verifyPort(sys.argv[2])
    tsPort = verifyPort(sys.argv[3])

    host_addr = socket.gethostbyname(hostname)
    print('\n[C]: Client host name: {} ({})'.format(hostname, host_addr))

    #connect
    server_Binding = (host_addr, rsPort)
    rs.connect(server_Binding)

    path = read()

    for i in path:
        #encode data to send to socket
        rs.send(i.encode('utf-8'))
        data = rs.recv(200)
        msg = data.decode('utf-8')

        #check NS ending
        if msg.endswith("NS"):
            for view in range(2):
                #open ts and decode data
                try:
                    ts.send(i.encode('utf-8'))
                    data_ts = ts.recv(200)
                    msg = data_ts.decode('utf-8')
                    break

                except:
                    ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                    ts_addr = socket.gethostbyname((msg).split()[0])
                    ts_binding = (ts_addr, tsPort)
                    ts.connect(ts_binding)
        
        results.append(msg)
    
    rs.send('end'.encode('utf-8'))
    ts.send('end'.encode('utf-8'))   

    file = open("RESOLVED.txt", "w")
    time.sleep(3)

    for line in results:
        print("\n" + line)
        time.sleep(0.5)
        file.write(line + "\n")

    rs.close()
    ts.close() 
    file.close()

if __name__ == "__main__":
    cs = threading.Thread(name='client', target=client)
    cs.start()
