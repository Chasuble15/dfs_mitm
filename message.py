import json
from packet import Packet
import re

with open("protocol.json", "r") as f:
    PROTOCOL = json.loads(f.read())

def find_dict_by_protocol_id(id):
  for d in PROTOCOL:
    if d.get('protocol_id') == id:
      return d
  return None 


def find_protocol_id_by_name(name):
    for d in PROTOCOL:
        if d.get('name') == name:
            id = d.get("protocol_id")
            return id
    return None    


class Message():
    
    def __init__(self, packet):
        self.variables = dict()
        self.infos = dict()
        self.tasks = list()
        self.packet = packet
        
    def serialize(self, protocol_id):
        pass
    
    def read(self, task):
        var = dict()
        
        
        
        
        if task.get('object'):
            protocol_id = find_protocol_id_by_name(task.get('object'))
            sub_message = Message(self.packet)
            sub_message.deserialize(protocol_id)
            var[task.get('object')] = sub_message.variables 
            
        elif task.get('type') == "VarInt":
            var[task.get('variable')] = self.packet.readVarInt()
        elif task.get('type') == "VarShort":
            var[task.get('variable')] =  self.packet.readVarShort()    
        elif task.get('type') == "Int":
            var[task.get('variable')] =  self.packet.readInt() 
        elif task.get('type') == "Short":
            var[task.get('variable')] =  self.packet.readShort()  
        elif task.get('type') == "VarLong":
            var[task.get('variable')] =  self.packet.readVarLong()   
            
        return var    


    def deserialize(self, id):
        
        self.infos = find_dict_by_protocol_id(id)
        self.tasks = self.infos.get('attr_write')
        
        self.name = self.infos.get('name')
        self.variables['name'] = self.name
        
        if self.tasks:
            for task in self.tasks:
                print(task)
                
                if task.get('variable') and "[" in task.get('variable'):
                    listname = re.sub("\[.*?\]", "", task.get('variable'))
                    length = self.variables[f"{listname}.length"]
                    array = []
                    if task.get('type'):
                        task['variable'] = re.sub("\[.*?\]", "", task.get('variable'))[:-1]
                    for _ in range(length):
                        array.append(self.read(task))
                    self.variables[listname] = array
                else:    
                    self.variables.update(self.read(task))
            


packet = Packet()

datahex = "489103209a3e5eb91af8020000006800018cd704f802000000680000000320dc028e23939c"
packet.addData(bytearray.fromhex(datahex))


while len(packet.data) > 0:
    packet.readHiHeader()
    length = packet.readLength()
    msg = Message(packet)

    msg.deserialize(packet.packet_id)   
    msg.packet.end()     

    print(msg.variables)
