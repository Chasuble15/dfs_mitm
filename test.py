import json

with open("protocol.json", "r") as f:
    protocol = json.loads(f.read())
    
    
def find_dict_by_protocol_id(id):
  for d in protocol:
    if d.get('protocol_id') == id:
      return d
  return None 

def find_protocol_id_by_name(name):
    for d in protocol:
        if d.get('name') == name:
            id = d.get("protocol_id")
            return id
    return None     
    
    
def read_packet(packet_id):
    infos = find_dict_by_protocol_id(packet_id)
    attr_write = infos.get('attr_write')
    vars = infos.get('vars')
    
    # for var in vars:
    #     print(var)
    
    for attr in attr_write:
        
        print(attr)  
        # if attr.get('type') == 'Byte':
        #     print(attr.get('variable') + ": \t" + "readByte")
        # elif attr.get('type') == 'VarLong':
        #     print(attr.get('variable') + ": \t" + "readVarLong")
        # elif attr.get('type') == 'VarInt':
        #     print(attr.get('variable') + ": \t" + "readVarInt")
        # elif attr.get('type') == 'UTF':
        #     print(attr.get('variable') + ": \t" + "readUTF")
        # elif attr.get('type') == 'Short':
        #     print(attr.get('variable') + ": \t" + "readShort")    
        # else:
        #     print(attr)   
        if attr.get('object'):
            id = find_protocol_id_by_name(attr.get('object'))
            read_packet(id)            
  
    
    
read_packet(2066)    