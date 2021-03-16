from queue import Queue
import socket
import threading

#Socket will be used for our connection attempts to the host at a specific port

#Threading will allow us to run multiple scanning functions simultaneously.

#Queue is a data structure that will help us to manage the access of multiple threads on a single resource, which in our case will be the port numbers. Since our threads run simultaneously and scan the ports, we use queues to make sure that every port is only scanned once.

target = '127.0.0.1'
queue = Queue()
open_ports = []

def portscan(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((target, port))
        return True
    except:
        return False

#########################################################################################


# Now, before we get into the threading, we need to first define the ports we want to scan. For this, we will define another function called get_ports.

def get_ports(mode):
    if mode == 1:
        for port in range(1, 1024):
            queue.put(port)
    elif mode == 2:
        for port in range(1,49152):
            queue.put(port)
    elif mode == 3:
        ports = [20, 21, 22, 23, 25, 53, 80, 110, 443]
        for port in ports:
            queue.put(port)
    elif mode == 4:
        ports = input("Enter your ports (seprate by blank):")
        ports = ports.split()
        ports = list(map(int, ports))
        for port in ports:
            queue.put(port)

# Notice that when we enter the ports in mode four, we are splitting our input into a list of strings. Therefore, we need to map the typecasting function of the integer data type to every element of the list in order to use it.           

#########################################################################################

# Multithreading
#The next thing we need to do is defining a so-called worker function for our threads. This function will be responsible for getting the port numbers from the queue, scanning them and printing the results.


def worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print("port {} is open!".format(port))
            open_ports.append(port)
        #else:
        #    print("Port {} is closed!". format(port))



#########################################################################################


# So, now that we have implemented the functionality, we are going to write our main function, which creates, starts and manages our threads.

def run_scanner(threads, mode):
    get_ports(mode)
    thread_list = []

    for t in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()

    print("Open ports are:", open_ports)


run_scanner(100, 1)





