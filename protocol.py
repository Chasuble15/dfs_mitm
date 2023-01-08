from packet import Packet

def unknow(packet: Packet):
    data = packet.data.hex()
    packet.clear()
    return {"message": "Unknow", "packet_id": packet.packet_id, "data": data}


def exchangeBidHouseSearchMessage(packet: Packet):
    message = "ExchangeBidHouseSearchMessage"
    instance_id = packet.readInt()
    length = packet.readLength()
    object_gid = packet.readVarInt()
    follow = packet.readBoolean()
    packet.end()
    return {"message": message, "packet_id": packet.packet_id ,"instance_id": instance_id, "length": length, "object_gid": object_gid, "follow": follow}


def basicAckMessage(packet: Packet):
    message = "BasicAckMessage"
    length = packet.readLength()
    seq = packet.readVarInt()
    last_packet_id = packet.readVarShort()
    packet.end()
    return {"message": message, "packed_id": packet.packet_id, "length": length, "seq": seq, "last_packet_id": last_packet_id}


def exchangeTypesItemsExchangerDescriptionForUserMessage(packet: Packet):
    message = "ExchangeTypesItemsExchangerDescriptionForUserMessage"
    length = packet.readLength()
    object_gid = packet.readVarInt()
    object_type = packet.readInt()
    item_description_length = packet.readShort()
    item_descriptions = []
    for _ in range(item_description_length):
        object_uid = packet.readVarInt()
        object_gid = packet.readVarInt()
        object_type = packet.readInt()
        effects_length = packet.readShort()
        effects = []
        for _ in range(effects_length):
            # actionId
            effects.append(packet.readVarShort())
        prices_length = packet.readShort()
        prices = []
        for _ in range(prices_length):
            prices.append(packet.readVarLong())
        item_descriptions.append({
            "object_uid": object_uid,
            "object_gid": object_gid,
            "object_type": object_type,
            "effects_length": effects_length,
            "effects": effects,
            "prices_length": prices_length,
            "prices": prices
        })
    packet.end()
    return {"message": message, "packed_id": packet.packet_id, "length": length, "object_gid": object_gid, "object_type": object_type, "item_description_length": item_description_length, "item_descriptions": item_descriptions}        


def basicPingMessage(packet: Packet):
    message = "BasicPingMessage"
    instance_id = packet.readInt()
    length = packet.readLength()
    quiet = packet.readBoolean()
    packet.end()
    return {"message": message, "packet_id": packet.packet_id, "instance_id": instance_id, "length": length, "quiet": quiet}       
        

def interactiveUseRequestMessage(packet: Packet):
    message = "InteractiveUseRequestMessage"
    instance_id = packet.readInt()
    length = packet.readLength()
    elem_id = packet.readVarInt()
    skill_instance_uid = packet.readVarInt()
    packet.end()
    return {"message": message, "packet_id": packet.packet_id, "instance_id": instance_id, "length": length, "elem_id": elem_id, "skill_instance_uid": skill_instance_uid}    


def charactersListMessage(packet: Packet):
    message = "CharactersListMessage"
    length = packet.readLength()
    characters_length = packet.readShort()
    characters = []
    for _ in range(characters_length):
        type_id = packet.readShort()
        
        # Char Minimal Info
        id = packet.readVarLong()
        name = packet.readUTF()
        level = packet.readVarShort()
        
        # EntityLook
        bones_id = packet.readVarShort()
        skins_length = packet.readShort()
        skins = []
        for _ in range(skins_length):
            skins.append(packet.readVarShort())
        indexed_colors_length = packet.readShort()
        indexed_colors = []
        for _ in range(indexed_colors_length):
            indexed_colors.append(packet.readInt())
        scales_length = packet.readShort()
        scales = []
        for _ in range(scales_length):
            scales.append(packet.readVarShort())
        subentities_length = packet.readShort()
        subentities = []
        for _ in range(subentities_length):        
            binding_point_category = packet.readByte()
            binding_point_index = packet.readByte()
            # EntityLook
            bones_id = packet.readVarShort()
            skins_length = packet.readShort()
            skins = []
            for _ in range(skins_length):
                skins.append(packet.readVarShort())
            indexed_colors_length = packet.readShort()
            indexed_colors = []
            for _ in range(indexed_colors_length):
                indexed_colors.append(packet.readInt())
            scales_length = packet.readShort()
            scales = []
            for _ in range(scales_length):
                scales.append(packet.readVarShort())
            subentities.append({
                "binding_point_category": binding_point_category,
                "binding_point_index": binding_point_index,
                "bones_id": bones_id,
                "skins_length": skins_length,
                "skins": skins,
                "indexed_colors_length": indexed_colors_length,
                "indexed_colors": indexed_colors,
                "scales_length": scales_length,
                "scales": scales
            })    
            # ???
            subentities_length = packet.readShort()    
        
        breed = packet.readByte()
        sex = packet.readBoolean()
        
        characters.append({
            "type_id": type_id,
            "id": id,
            "name": name,
            "level": level,
            "bones_id": bones_id,
            "skins_length": skins_length,
            "skins": skins,
            "indexed_colors_length": indexed_colors_length,
            "indexed_colors": indexed_colors,
            "scales_length": scales_length,
            "scales": scales,
            "subentities_length": subentities_length,
            "subentities": subentities,
            "breed": breed,
            "sex": sex
        })

    has_startup_actions = packet.readBoolean()
    packet.end()
    return {
        "message": message,
        "packet_id": packet.packet_id,
        "length": length,
        "characters_length": characters_length,
        "characters": characters,
        "has_startup_actions": has_startup_actions
    }
    
    
def queueStatusMessage(packet: Packet):
    message = "QueueStatusMessage"
    length = packet.readLength()
    position = packet.readShort()
    total = packet.readShort()
    packet.end()
    return {
        "message": message,
        "packet_id": packet.packet_id,
        "length": length,
        "position": position,
        "total": total
    }
    

def humanOption(packet: Packet):
    type_id = packet.readShort()
        
    
    
def humanInformations(packet: Packet):
    # restrictions TODO
    
    # other
    sex = packet.readBoolean()
    option_length = packet.readShort()
    options = []
    for _ in range(option_length):
        options.append(humanOption(packet))    
    
    
def mapComplementaryInformationsDataMessage(packet: Packet):
    message = "MapComplementaryInformationsDataMessage"
    length = packet.readLength()
    print(packet.data.hex())
    sub_area_id = packet.readVarShort()
    map_id = packet.readDouble()
    houses_length = packet.readShort()
    houses = []
    print(f"houses_length: {houses_length}")
    for _ in range(houses_length):
        # Handle HouseInformations
        type_id = packet.readShort()
        # ... TODO Complete this
           
    actors_length = packet.readShort()
    print(actors_length)
    actors = []
    for _ in range(actors_length):
        # Handle GameRolePlayActorInformations
        type_id = packet.readShort()
        print(f"type_id: {type_id}")
        if type_id == 9999:
            # GameRolePlayCharacterInformations
            # 1. GameRolePlayHumanoidInformations
            # 1a. GameRolePlayNamedActorInformations
            
            # 1b. Humanoid info
            humanoid_info_type_id = packet.readShort()
            
            # 1c. account id
            account_id = packet.readInt()
            # 2. ActorAlignmentInformations
            
            
        # # serializeAs_GameContextActorPositionInformations
        # contextual_id = packet.readDouble()
        # print("Contectual: " + str(contextual_id))
        # disposition_type_id = packet.readShort()
        # # disposition.serialize EntityDispositionInformations
        # cell_id = packet.readShort()
        # print("Cell_id: " + str(cell_id))
        # direction = packet.readByte()
        # # look.serializeAs_EntityLook

        # # EntityLook
        # bones_id = packet.readVarShort()
        # skins_length = packet.readShort()
        # skins = []
        # for _ in range(skins_length):
        #     skins.append(packet.readVarShort())
        # indexed_colors_length = packet.readShort()
        # indexed_colors = []
        # for _ in range(indexed_colors_length):
        #     indexed_colors.append(packet.readInt())
            
        # print(f"Colors: {indexed_colors}")    
        # scales_length = packet.readShort()
        # scales = []
        # for _ in range(scales_length):
        #     scales.append(packet.readVarShort())
        # print(f"scales: {scales}")    
        # subentities_length = packet.readShort()
        # print(f"subentities_length: {subentities_length}")
        # subentities = []
        # for _ in range(subentities_length):        
        #     binding_point_category = packet.readByte()
        #     binding_point_index = packet.readByte()
        #     # EntityLook
        #     bones_id = packet.readVarShort()
        #     skins_length = packet.readShort()
        #     skins = []
        #     for _ in range(skins_length):
        #         skins.append(packet.readVarShort())
        #     indexed_colors_length = packet.readShort()
        #     indexed_colors = []
        #     for _ in range(indexed_colors_length):
        #         indexed_colors.append(packet.readInt())
        #     scales_length = packet.readShort()
        #     scales = []
        #     for _ in range(scales_length):
        #         scales.append(packet.readVarShort())
        #     subentities.append({
        #         "binding_point_category": binding_point_category,
        #         "binding_point_index": binding_point_index,
        #         "bones_id": bones_id,
        #         "skins_length": skins_length,
        #         "skins": skins,
        #         "indexed_colors_length": indexed_colors_length,
        #         "indexed_colors": indexed_colors,
        #         "scales_length": scales_length,
        #         "scales": scales
        #     })    
        #     # ???
        #     # subentities_length = packet.readShort()        
    interactive_elements_length = packet.readShort()
    interactive_elements = []
    for _ in range(interactive_elements_length):
        type_id = packet.readShort()
        element_id = packet.readInt()
        element_type_id = packet.readInt()
        enabled_skills_length = packet.readShort()
        enabled_skills = []
        for _ in range(enabled_skills_length):
            type_id = packet.readShort()
            skill_id = packet.readVarInt()
            skill_instance_id = packet.readInt()
            enabled_skills.append({
                "type_id": type_id,
                "skill_id": skill_id,
                "skill_instance_id": skill_instance_id
            })
        disabled_skills_length = packet.readShort()
        disabled_skills = []
        for _ in range(disabled_skills_length):
            type_id = packet.readShort()
            skill_id = packet.readVarInt()
            skill_instance_id = packet.readInt()
            disabled_skills.append({
                "type_id": type_id,
                "skill_id": skill_id,
                "skill_instance_id": skill_instance_id
            })
        on_current_map = packet.readBoolean()      
        interactive_elements.append({
            "type_id": type_id,
            "element_id": element_id,
            "element_type_id": element_type_id,
            "enabled_skills": enabled_skills,
            "disabled_skills": disabled_skills,
            "on_current_map": on_current_map
        })          
    
    packet.clear()
    return {
        "message": message,
        "packet_id": packet.packet_id,
        "length": length,
        "sub_area_id": sub_area_id,
        "map_id": map_id,
        "interactive_elements": interactive_elements
    }    

def get_message(packet: Packet):
    packet.readHiHeader()
    
    if packet.packet_id == 7962:
        return exchangeBidHouseSearchMessage(packet)
    elif packet.packet_id == 4644:
        return basicAckMessage(packet)
    elif packet.packet_id == 6062:
        return exchangeTypesItemsExchangerDescriptionForUserMessage(packet)
    elif packet.packet_id == 311:
        return basicPingMessage(packet)
    elif packet.packet_id == 1411:
        return interactiveUseRequestMessage(packet)
    elif packet.packet_id == 1159:
        return charactersListMessage(packet)
    elif packet.packet_id == 5360:
        return queueStatusMessage(packet)
    elif packet.packet_id == 4524:
        return mapComplementaryInformationsDataMessage(packet)
    else:
        return unknow(packet)


