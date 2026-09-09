import numpy as np

class VomcsReader:
    def __init__(self, size=300):
        self.size = size
        self.mitte = size // 2

    def extract_pattern_spiral(self, matrix, layer_z, length):
        """MUSTER 0x01: Liest Bits spiralförmig von außen nach innen aus."""
        bits = []
        x, y = 0, 0
        direction = "down"
        
        for _ in range(length):
            if 0 <= x < self.size and 0 <= y < self.size:
                bits.append(int(matrix[x, y, layer_z]))
                
                if direction == "down":
                    if x < self.size - 1: x += 1
                    else: direction = "right"; y += 1
                elif direction == "right":
                    if y < self.size - 1: y += 1
                    else: break
        return bits

    def extract_pattern_zigzag(self, matrix, layer_z, length):
        """MUSTER 0x03: Liest Bits im Zickzack-Raster aus."""
        bits = []
        x, y = 0, 0
        direction = 1 # 1 = Rechts, -1 = Links
        
        for _ in range(length):
            if 0 <= x < self.size and 0 <= y < self.size:
                bits.append(int(matrix[x, y, layer_z]))
                
                if (direction == 1 and y < self.size - 1) or (direction == -1 and y > 0):
                    y += direction
                else:
                    if x < self.size - 1:
                        x += 1
                        direction *= -1
                    else: break
        return bits

    def decode_pointer(self, matrix, vomcs_pointer):
        """
        Nimmt den erweiterten VOMCS-Pointer und extrahiert 
        die exakte Bitkette aus dem Raum-Schachbrett.
        """
        m_id = vomcs_pointer["MUSTER_ID"]
        start_z = vomcs_pointer["START_Z"]
        length = vomcs_pointer["LAENGE"]
        
        print(f"[Reader] Dekodiere Pointer mit Muster_ID {m_id} in Schicht Z={start_z}...")
        
        if m_id == 1:
            return self.extract_pattern_spiral(matrix, start_z, length)
        elif m_id == 3:
            return self.extract_pattern_zigzag(matrix, start_z, length)
        else:
            raise ValueError(f"Muster-ID {m_id} im Reader noch nicht implementiert!")

    def bits_to_text(self, bits):
        """Wandelt eine Bit-Liste zurück in lesbare Zeichen (UTF-8)."""
        text = ""
        # Immer 8 Bit ergeben ein Zeichen
        for i in range(0, len(bits), 8):
            byte_bits = bits[i:i+8]
            if len(byte_bits) < 8: break
            # Bit-Liste in String umwandeln und in Integer konvertieren
            bin_str = "".join(map(str, byte_bits))
            text += chr(int(bin_str, 2))
        return text

# --- SIMULIERTER LESE-TEST ---
if __name__ == "__main__":
    reader = VomcsReader(size=300)
    
    # 1. Wir holen uns die Matrix aus deinem erfolgreichen Writer-Lauf (Simulations-Dummy)
    # Nehmen wir an, wir haben den Würfel eingescannt. Wir wissen, dass in Schicht 140 
    # ein Wort im Zickzack-Modus (Muster 3) versteckt wurde.
    simulierte_gescannte_matrix = np.zeros((300, 300, 300), dtype=int)
    
    # Das Wort "DASS" in Bits (wurde vom Writer in Schicht 140 platziert)
    dass_bits = [0,1,0,0,0,1,0,0, 0,1,0,0,0,0,0,1, 0,1,0,1,0,0,1,1, 0,1,0,1,0,0,1,1]
    
    # Wir platzieren es im Zickzack-Muster in Schicht 140 der gescannten Matrix
    x, y = 0, 0
    direction = 1
    for bit in dass_bits:
        simulierte_gescannte_matrix[x, y, 140] = bit
        if (direction == 1 and y < 299) or (direction == -1 and y > 0): y += direction
        else: x += 1; direction *= -1

    print("--- VOMCS READER ONLINE ---")
    
    # 2. Das ist der Pointer, den Freund A per Messenger geschickt hat:
    empfangener_pointer = {
        "MUSTER_ID": 3,   # Zickzack
        "START_Z": 140,   # Schicht 140
        "LAENGE": 32      # 4 Zeichen * 8 Bit
    }
    
    # 3. Dekodieren und Rekonstruieren
    extrahierte_bits = reader.decode_pointer(simulierte_gescannte_matrix, empfangener_pointer)
    rekonstruierter_text = reader.bits_to_text(extrahierte_bits)
    
    print(f"[Decoder] Extrahierte Bits: {extrahierte_bits}")
    print(f"🎉 REKONSTRUKTION ERFOLGREICH: '{rekonstruierter_text}'")
