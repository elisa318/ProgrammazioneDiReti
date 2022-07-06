#Nome e Cognome : Elisa Barberini
#Numero matricola : 0000934354
#Email: elisa.barberini3@studio.unibo.it
import sys, signal
import http.server
import socketserver

# Legge il numero della porta dalla riga di comando e si mette 
#in ascolto sulla porta passata o sulla 8078 di default
if sys.argv[1:]:
  port = int(sys.argv[1])
else:
  port = 8078
#per gestire più richieste utilizzeremo ThreadingTCPServer
class ServerHandler(http.server.SimpleHTTPRequestHandler):        
    def do_GET(self):
        # Scrivo sul file di testo storicoGET.txt le richieste effettuate dal client     
        with open("storicoGET.txt", "a") as out:
          info = "GET request,\nPath: " + str(self.path) + "\nHeaders:\n" + str(self.headers) + "\n"
          out.write(str(info))
        http.server.SimpleHTTPRequestHandler.do_GET(self)
        
#funzione utilizzata per gestire più richieste
server = socketserver.ThreadingTCPServer(('127.0.0.1',port), ServerHandler)
#indichiamo che il server deve attendere la terminazione dei thread
server.daemon_threads = True  
#il Server acconsente al riutilizzo del socket anche se ancora non è stato rilasciato quello precedente, andandolo a sovrascrivere
server.allow_reuse_address = True  

def signal_handler(signal, frame):
    #definisco una funzione per consentire la terminazione dell'esecuzione da tastiera premendo Ctrl-C 
    print( 'Exiting http server (Ctrl+C pressed)')
    try:
      if( server ):
        server.server_close()
    finally:
      sys.exit(0)

#viene effettivamente interrotta l'esecuzione se da tastiera arriva la sequenza (CTRL + C) 
signal.signal(signal.SIGINT, signal_handler)

# entra nel loop infinito
try:
  while True:
    #sys.stdout.flush()
    print('ACCEDERE ALLA PORTA', port)
    server.serve_forever()
except KeyboardInterrupt:
  pass

server.server_close()
