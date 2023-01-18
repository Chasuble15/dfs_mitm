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
    
    def __init__(self, packet=Packet()):
        self.variables = dict()
        self.infos = dict()
        self.tasks = list()
        self.packet = packet
        
        
    def serialize(self, protocol_id: int):
        
        self.infos = find_dict_by_protocol_id(protocol_id)
        self.tasks = self.infos.get('attr_write')
        
        for task in self.tasks:
            if task.get('type') == 'UTF':
                self.packet.writeUTF(self.variables[task.get('variable')])
            else:
                print(f"Erreur, variables are missing: {task}")    
        
        self.packet.writeHeader(protocol_id, 454)
        print(self.packet.data.hex())
        
    
    
    def read(self, task):
        var = dict()
        
        if task.get('type_id'):
            protocol_id = self.packet.readShort()
            sub_message = Message(self.packet)
            sub_message.deserialize(protocol_id)
            var[task.get('variable')] = sub_message.variables
            
        elif task.get('object'):
            protocol_id = find_protocol_id_by_name(task.get('object'))
            sub_message = Message(self.packet)
            sub_message.deserialize(protocol_id)
            var[task.get('object')] = sub_message.variables 
        
        elif task.get('parent'):
            protocol_id = find_protocol_id_by_name(task.get('parent'))
            sub_message = Message(self.packet)
            sub_message.deserialize(protocol_id)
            var[task.get('parent')] = sub_message.variables             
        
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
        elif task.get('type') == "Byte":
            var[task.get('variable')] =  self.packet.readByte()  
        elif task.get('type') == "Double":
            var[task.get('variable')] =  self.packet.readDouble()  
        elif task.get('type') == "UTF":
            var[task.get('variable')] =  self.packet.readUTF()  
        elif task.get('type') == "Boolean":
            var[task.get('variable')] =  self.packet.readBoolean()  
        else:
            print("UNKNOWN TYPE ERROR")   
              
        # print(f"VARIABLE : {var}")                                        
        return var    


    def deserialize(self, id):
        try:
            # print(f"ID: {id}")
            # print(len(self.packet.data[self.packet.pos:]))
            ### Get the tasks list from the object ID
            self.infos = find_dict_by_protocol_id(id)
            self.tasks = self.infos.get('attr_write')
            
            ### Get the name of the object
            self.name = self.infos.get('name')
            ### Add the name to the returned data
            self.variables['name'] = self.name
            
            if self.tasks:
                for task in self.tasks:
                    
                    if task.get('variable') and "[" in task.get('variable'):
                        listname = re.sub("\[.*?\]", "", task.get('variable'))
                        length = self.variables[f"{listname}.length"]
                        array = []
                        # if task.get('type'):
                        #     task['variable'] = re.sub("\[.*?\]", "", task.get('variable'))[:-1]
                        for _ in range(length):
                            array.append(self.read(task))
                        self.variables[listname] = array
                    else:    
                        self.variables.update(self.read(task))        
        except:
            # TODO: Regler ce probleme de packets incomplets
            print("Error")
            print(self.infos)



# msg = Message()


# msg.variables["content"] = "Salutations!"
# to_send = msg.serialize(232)


# packet = Packet()

# datahex = ""
# packet.addData(bytearray.fromhex(datahex))


# while len(packet.data) > 0:
#     print("Nouveau packet ------------------------------------------------------------")
#     packet.readHiHeader()
#     # packet.readInt()
#     length = packet.readLength()
    
#     if packet.packet_id == 6951:
#         packet.pos += length
#         packet.end()
#         print("Packet skipped --------------------------------")
#         continue
    
#     print(f"Len: {length} Packet ID: {packet.packet_id}")
#     msg = Message(packet)

#     msg.deserialize(packet.packet_id)   
#     msg.packet.end()     

#     print(msg.variables)
