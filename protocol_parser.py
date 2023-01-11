import os
import json
import re
from tqdm import tqdm

# Définissez le chemin du répertoire
directory = 'scripts'

# Créez une liste vide pour stocker les chemins de fichier
file_paths = []

# Parcourez le dossier et ses sous-dossiers de manière récursive
for root, dirs, files in os.walk(directory):
    # Pour chaque fichier, ajoutez son chemin complet à la liste
    for file in files:
        # Filtrez la liste pour ne garder que les fichiers ".as"
        if file.endswith('.as'):
            file_paths.append(os.path.join(root, file))


# Créez une expression régulière qui correspond à un type de variable suivi d'un nom de variable
class_pattern = re.compile(r"\s*public class (?P<name>\w+) (?:extends (?P<parent>\w+) )?implements (?P<interface>\w+)\n")
id_pattern = re.compile(r"\s*public static const protocolId:uint = (?P<protocol_id>\d+);\n")
public_var_pattern = re.compile(r"\s*public var (?P<name>\w+):(?P<type>\S*)")
attr_write_pattern = re.compile(r"\s*output\.write(?P<type>\w+)\((?:this\.)?(?P<variable>\w+)\)")
attr_write_length_pattern = re.compile(r"\s*output\.write(?P<type>\w+)\((?:this\.)?(?P<variable>.+)\)")
write_vector_pattern = re.compile(r"\s*\(this.(?P<variable>\w+\[(.*)\]) as (?P<object>\w+)\)\.serialize\w+\(output\)")
serialize_parent_pattern = re.compile(r"\s*super\.serializeAs_(?P<parent>\w+)\(output\)")
attr_type_id_pattern = re.compile(r"\s*output.write(?P<type_id>\w+)\(\(this\.(?P<variable>\w+\[(.*)\]) as (?P<target>\w+)\)\.getTypeId\(\)\)")
type_id_secondary_pattern = re.compile(r"\s*output.write(?P<type_id>\w+)\(this\.(?P<variable>\w+)\.getTypeId")

serialize_object_pattern = re.compile(r'\s*this\.\w+\.serializeAs_(?P<object>\w+)\(output\)\;')

# Créez une liste vide contenant les classes
classes = []

# Parcourez chaque fichier ".as"
for filename in tqdm(file_paths):
    # Ouvrez le fichier
    with open(filename, 'r') as f:
        
        result = dict()
        vars = []
        attr_write = []
        
        # Parcourez chaque ligne du fichier
        for line in f:
            # Appliquez l'expression régulière à la ligne
            class_match = class_pattern.match(line)
            id_match = id_pattern.match(line)
            public_var_match = public_var_pattern.match(line)
            attr_write_match = attr_write_pattern.match(line)
            attr_write_length_match = attr_write_length_pattern.match(line)
            write_vector_match = write_vector_pattern.match(line)
            serialize_parent_match = serialize_parent_pattern.match(line)
            attr_type_id_match = attr_type_id_pattern.match(line)
            serialize_object_match = serialize_object_pattern.match(line)
            type_id_secondary_match = type_id_secondary_pattern.match(line)
            
            # Si l'expression régulière a trouvé une correspondance, ajoutez le type de variable au dictionnaire
            if class_match:
                result.update(class_match.groupdict())
                
            elif id_match:
                result["protocol_id"] = int(id_match.group("protocol_id"))
            
            elif public_var_match:
                vars.append(public_var_match.groupdict()) 
                result["vars"] = vars
                
            elif serialize_object_match:
                attr_write.append(serialize_object_match.groupdict()) 
                result["attr_write"] = attr_write                
            
            elif attr_type_id_match:
                attr_write.append(attr_type_id_match.groupdict())
                result["attr_write"] = attr_write
                
            elif type_id_secondary_match:
                attr_write.append(type_id_secondary_match.groupdict())
                result["attr_write"] = attr_write                    
                
            elif attr_write_match:
                attr_write.append(attr_write_match.groupdict())
                result["attr_write"] = attr_write
                
            elif attr_write_length_match:
                attr_write.append(attr_write_length_match.groupdict())   
                result["attr_write"] = attr_write 
            
            elif write_vector_match:
                attr_write.append(write_vector_match.groupdict())   
                result["attr_write"] = attr_write                     
                   
            elif serialize_parent_match:
                attr_write.append(serialize_parent_match.groupdict())   
                result["attr_write"] = attr_write         
                   
            else:
                continue
            
        if result:    
            classes.append(result)  
              
              
with open("protocol.json", "w") as f:       
    f.write(json.dumps(classes, indent=4))                
        