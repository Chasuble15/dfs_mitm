import select
from packet import Packet
import time
import protocol
from utils import delay
import json
from datetime import datetime
import threading
from message import Message

IGNORE_PACKET_ID = [
    6743, # ChatServerMessage
    3522, # ChatServerWithObjectMessage
    7425, # GameMapMovementMessage,
    2866, # GameContextRemoveElementMessage
    5031, # MapFightCountMessage
    6515, # StatedElementUpdatedMessage
    6441, # GameRolePlayRemoveChallengeMessage,
    840, # GameMapChangeOrientationMessage
    # 4644, # BasicAckMessage
    7529, # PrismsListUpdateMessage
    7514, # GameRolePlayShowActorMessage
    2700, # UpdateMapPlayersAgressableStatusMessage
    2997, # SetCharacterRestrictionsMessage,
    # 4286, # InteractiveUsedMessage
    3848, # GameContextRefreshEntityLookMessage
    762, # GameCautiousMapMovementMessage
]

class InjectorBridgeHandler:
    
    def __init__(self, coJeu, coSer):
        self.coJeu = coJeu
        self.coSer = coSer
        self.other = {coJeu: coSer, coSer: coJeu}
        self.conns = [coJeu, coSer]    

        self.packet = Packet()
        self.injected_to_client = 0
        self.injected_to_server = 0
        self.counter = 100
        
        self.prices = {}
        
    def handle(self, data, origin):
        from_client = origin == self.coJeu


        # Select the program
        self.program1(data, from_client)
        
        
        self.other[origin].sendall(data)
        time.sleep(0.005)
        
    
    def open_hdv(self):
        packet = Packet()
        self.counter += 1    
        instance_id = self.counter
        
        elem_id = 515303
        skill_instance_uid = 148890942
        
        packet.writeVarInt(elem_id)
        packet.writeVarInt(skill_instance_uid)
        packet.writeHeader(1411, instance_id)
        
        self.coSer.sendall(packet.data)
        
    
    def check_resource(self, object_gid, follow):
        packet = Packet()
        self.counter += 1    
        instance_id = self.counter
        
        packet.writeVarInt(object_gid)
        packet.writeBoolean(follow)
        packet.writeHeader(7962, instance_id)
        
        self.coSer.sendall(packet.data)
    
    
    def select_player(self, id):
        delay(1, 3)
        packet = Packet()
        self.counter += 1
        instance_id = self.counter
        char_id = id
        
        packet.writeVarLong(char_id)
        packet.writeHeader(2967, instance_id)
        
        self.coSer.sendall(packet.data)    
        print(f"Connection au jeu avec le personnage: {char_id}")        
    
    def loop(self):
        conns = self.conns
        active = True
        try:
            while active:
                rlist, wlist, xlist = select.select(conns, [], conns)
                if xlist or not rlist:
                    break
                for r in rlist:
                    data = r.recv(8192)
                    if not data:
                        active = False
                        break
                    self.handle(data, r)
        finally:
            for c in conns:
                c.close()
    
    
    
    def program1(self, data, from_client):
        self.packet.addData(data)
        
        while len(self.packet.data) > 0:
            self.counter += 1
        
            print("Nouveau packet ------------------------------------------------------------")
        
            
            # self.packet.readHiHeader()
        
            if from_client:
                # TX
                self.packet.clear()
                # self.packet.readInt()
                # length = self.packet.readLength()
                
                # msg = Message(self.packet)


                # msg.deserialize(self.packet.packet_id)   
                # msg.packet.end()    
                # print(msg.variables)
                

            else:
                # RX
                print(self.packet.data.hex())
                self.packet.clear()
                # length = self.packet.readLength()
                # print(f"Len: {length}")
                # self.packet.verifyPacketRx(length)
                # msg = Message(self.packet)
            
                # msg.deserialize(self.packet.packet_id)   
                # msg.packet.end()
                # print(msg.variables)

                ### Click automatique sur le personnage au lancement du jeu
                # if message["message"] == "CharactersListMessage":
                #     self.select_player(message["characters"][0]["id"])
                    

          

                 
                 
                    
    def gid_parser(self, data, from_client):
        self.packet.addData(data)
        
        while len(self.packet.data) > 0:
            self.counter += 1
        
            message = protocol.get_message(self.packet)
        
            if from_client:
                # TX
                if message["packet_id"] == 7962:
                    if message["follow"]:
                        print(message.get("object_gid"))
            
            else:
                # RX
                pass  

    
    def start_scrapping(self):
        # Lorsque le client demande les infos de la map actuelle
        delay(4, 6)
        print("Open HDV")
        self.open_hdv()  
        print("HDV Opened!")
        delay(1, 2)
        # Start scraping
        with open("price_checklist.txt", "r") as f:
            for line in f:
                print("Scraping ...")
                gid = int(line)
                self.check_resource(gid, True)
                delay(0.5, 2)
                self.check_resource(gid, False)
                delay(0.5, 2)
        print("Scraping terminé")
        with open("data_output.txt", "a") as f:
                f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " - ")
                f.write(json.dumps(self.prices))
                f.write("\n")
        self.prices.clear()   
        delay(3, 4)
        quit()
    
    def ressources_collector(self, data, from_client):
        self.packet.addData(data)
        
        while len(self.packet.data) > 0:
            self.counter += 1
        
            message = protocol.get_message(self.packet)
        
            if from_client:
                # TX
                if message["message"] == "BasicAckMessage":
                    # Lorsque le client demande les infos de la map actuelle
                    if message["last_packet_id"] == 8121:
                        delay(2, 3)
                        self.open_hdv()
            
            else:
                # RX
                ### Click automatique sur le personnage au lancement du jeu
                if message["message"] == "CharactersListMessage":
                    self.select_player(message["characters"][0]["id"])
                
                ### Collecte des prix
                if message["message"] == "ExchangeTypesItemsExchangerDescriptionForUserMessage":
                    res_id = message.get("object_gid")
                    prices = message["item_descriptions"][0]["prices"]
                    # print(f"Item: {res_id}\tPrices: {prices}")
                    self.prices[res_id] = prices
                    
                ### Start scrapping 
                if message["message"] == "Unknow":   
                    if message["packet_id"] == 4524:
                        thread = threading.Thread(target=self.start_scrapping)
                        thread.start()                                                
                        