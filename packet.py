import math
import struct

class Packet:
    
    def __init__(self, data=None):
        if data is None:
            data = bytearray()
        self.data = data
        self.pos = 0

    def addData(self, byte):
        self.data += byte
        
    
    def readHiHeader(self):
        hi_head = self.data[0:2]
        self.packet_id = int.from_bytes(hi_head, "big") >> 2
        self.lenType = int.from_bytes(hi_head, "big") & 3
        self.pos += 2

    
    def readDouble(self):
        # 8 bytes = 64 bits
        # b = self.data[self.pos:self.pos+8]
        # self.pos = self.pos + 8
        # return int.from_bytes(b, 'big', signed=True)
        print(self.data[self.pos:self.pos+8].hex())
        double_value = struct.unpack('>d', self.data[self.pos:self.pos+8])[0]
        self.pos = self.pos + 8
        return int(double_value)

    def readInt(self):
        # 4 bytes = 32 bits
        b = self.data[self.pos:self.pos+4]
        self.pos = self.pos + 4
        return int.from_bytes(b, 'big', signed=True)

    def readUnsignedInt(self):
        # 4 bytes = 32 bits
        b = self.data[self.pos:self.pos+4]
        self.pos = self.pos + 4
        return int.from_bytes(b, 'big')    

    def readShort(self):
        # 2 bytes = 16 bits
        b = self.data[self.pos:self.pos+2]
        self.pos = self.pos + 2
        return int.from_bytes(b, 'big', signed=True)

    def readUnsignedShort(self):
        b = self.data[self.pos:self.pos+2]
        self.pos = self.pos + 2
        return int.from_bytes(b, 'big')

    def readUTF(self):
        size = self.readUnsignedShort()
        b = self.data[self.pos:self.pos+size]
        self.pos = self.pos + size
        return b.decode()
    
    def readByte(self):
        b = self.data[self.pos]
        self.pos = self.pos + 1
        return b
    
    def read3Bytes(self):
        b = self.data[self.pos:self.pos+3]
        self.pos = self.pos + 3
        return int.from_bytes(b, 'big')
    
    def readLength(self):
        if self.lenType == 1:
            return self.readByte()
        elif self.lenType == 2:
            return self.readUnsignedShort()
        elif self.lenType == 3:
            return self.read3Bytes()
        else:
            print("[ERROR] LenType invalide")
            
            
    def readVarInt(self):
        ans = 0
        for i in range(0, 32, 7):
            b = self.readByte()
            ans += (b & 0b01111111) << i
            if not b & 0b10000000:
                return ans        


    def readVarUhInt(self):
        return self.readVarInt()        
            
            
    def readVarLong(self):
        ans = 0
        for i in range(0, 64, 7):
            b = self.readByte()
            ans += (b & 0b01111111) << i
            if not b & 0b10000000:
                return ans
        raise Exception("Too much data")            
            
            
    def readVarUhLong(self):
        return self.readVarLong()
            
            
    def readVarShort(self):
        ans = 0
        for i in range(0, 16, 7):
            b = self.readByte()
            ans += (b & 0b01111111) << i
            if not b & 0b10000000:
                return ans
        raise Exception("Too much data")
                
                
    def readVarUhShort(self):
        return self.readVarShort()    
    
    
    def readBoolean(self):
        val = self.readByte()
        if val == 1:
            return True
        else:
            return False
            
            
    def end(self):
        # reset the buffer
        del self.data[:self.pos]
        self.pos = 0       
        
    def clear(self):
        self.data.clear()
        self.pos = 0    
        
        
    def writeBoolean(self, b):
        if b:
            self.data += b"\x01"
        else:
            self.data += b"\x00"
            
            
    def writeUnsignedByte(self, b):
        self.data += b.to_bytes(1, "big")            
            
    def _writeVar(self, i):
        if not i:
            self.writeUnsignedByte(0)
        while i:
            b = i & 0b01111111
            i >>= 7
            if i:
                b |= 0b10000000
            self.writeUnsignedByte(b)    
            
            
    def writeVarInt(self, i):
        assert i.bit_length() <= 32
        self._writeVar(i)     
        
        
    def writeVarLong(self, i):
        assert i.bit_length() <= 64
        self._writeVar(i)       
               
        
    def writeHeader(self, packet_id, instance_id):
        # Write length
        length = len(self.data)
        lenType = math.ceil(length.bit_length() / 8)
        self.data = length.to_bytes(lenType, "big") + self.data
        # Write instance_id
        self.data = instance_id.to_bytes(4, "big") + self.data
        # Write packet id + lentype
        hihead = (packet_id << 2) + lenType
        self.data = hihead.to_bytes(2, "big") + self.data    