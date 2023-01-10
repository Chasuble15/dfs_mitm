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
    index_iterator = 0
    
    while index_iterator < len(attr_write):
        attr = attr_write[index_iterator]
        
        if attr.get("variable") and ".length" in attr.get("variable"):
            print("Début de la boucle")
            print("readLength")
            length = 2
            index_iterator += 1
            for _ in range(length - 1):
                print(attr_write[index_iterator])
            continue    
                
                
        
         
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
            index_iterator += 1     
            continue 
            
        print(attr)             
  
        index_iterator += 1    
    
    
read_packet(3593)