#Comando python chat.py 8000 http://192.168.0.2:8001
#Cor para o grid, mesma do fundo do atom(40,44,52)

from bottle import run, get, post, view, redirect, request
import requests, bottle, json, threading, time, sys
import pygame



#Variaveis Globais que precisa ser acessadas em várias threads
myGlobalList = []
flagClosedWindos = False


def initGame():
    myScreen = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("PytronTF")
    runGameFlag = True
    
    while runGameFlag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                runGameFlag = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    myGlobalList.append('Escape')
                    runGameFlag = False
                    
                if event.key == pygame.K_DOWN:
                    myGlobalList.append('d')

                if event.key == pygame.K_UP:
                    myGlobalList.append('u')

                if event.key == pygame.K_LEFT:
                    myGlobalList.append('l')

                if event.key == pygame.K_RIGHT:
                    myGlobalList.append('d')
                
                if event.key == pygame.K_w:
                    myGlobalList.append('w')
                    
                    
                    
                    
        time.sleep(0.2)
        
    pygame.display.quit()
    pygame.quit()
    print('kasjdnakjsdnakjdnakjdn')
    global flagClosedWindos
    flagClosedWindos = True
    
    
    
    
    
def showList():
    while not flagClosedWindos:
        print(myGlobalList, flagClosedWindos)
        time.sleep(1)
    

    
    
    

try:
    port_ = int(sys.argv[1])
except:
    print("Please inform a valid port.\n")
    exit(0)

try:
    peers = sys.argv[2:]
    print(peers)
except:
    print("Please inform a valid list of peers.\n")
    exit(0)

history = []



@get('/')
@view('chat.html')
def chat():
    return {'messages': history}


@get('/peers')
def index():
	return json.dumps(peers)


@get('/history')
def index():
	return json.dumps(history)


@get('/send_message')
@view('send_message.html')
def send_message():
    return


@post('/write_message')
def add_message():
    name = request.forms.get('name')
    msg = request.forms.get('msg')
    history.append([name, msg])
    mmsg = input()
    print (history, ":TESTE:", mmsg)
    redirect('/')


def get_peers():
    while not flagClosedWindos:#true
        for peer in peers:
            try:
                new_peers = requests.get(peer + "/peers")
                new_peers = json.loads(new_peers.text)
                for np in new_peers:
                    if np not in peers:
                        peers.append(np)
            except:
                pass
            time.sleep(1)

def receive_msg():
    while not flagClosedWindos:#true
        for peer in peers:
            try:
                new_h = requests.get(peer + "/history")
                new_h = json.loads(new_h.text)
                for m in new_h:
                    if m not in history:
                        history.append(m)
            except:
                pass

            time.sleep(1)


t_peers =   threading.Thread(target = get_peers)
t_chat  =   threading.Thread(target = receive_msg)
t_gameWind  =   threading.Thread(target = initGame)
t_show  =   threading.Thread(target = showList)


t_peers.start()
t_chat.start()
t_gameWind.start()
t_show.start()


run(host = '192.168.0.2', port = port_)
