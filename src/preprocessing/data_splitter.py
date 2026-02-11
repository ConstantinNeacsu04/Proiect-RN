import os
import shutil
import random

# Configurare
SOURCE_DIR = '../imagini antrenare'
TEST_DIR = '../imagini testare reala'
SPLIT_RATIO = 0.1  # 10% din poze merg la testare

def imparte_datele():
    if not os.path.exists(TEST_DIR):
        os.makedirs(TEST_DIR)
        
    print(f"✂️ Împart datele: {SPLIT_RATIO*100}% merg în Test...")
    
    clase = os.listdir(SOURCE_DIR)
    
    for clasa in clase:
        # Cream folderele Conform/Neconform in destinatie
        sursa_clasa = os.path.join(SOURCE_DIR, clasa)
        dest_clasa = os.path.join(TEST_DIR, clasa)
        
        if not os.path.exists(dest_clasa):
            os.makedirs(dest_clasa)
            
        if os.path.isdir(sursa_clasa):
            fisiere = os.listdir(sursa_clasa)
            random.shuffle(fisiere) # Amestecam aleatoriu
            
            # Calculam cate mutam
            numar_test = int(len(fisiere) * SPLIT_RATIO)
            fisiere_de_mutat = fisiere[:numar_test]
            
            for f in fisiere_de_mutat:
                shutil.move(os.path.join(sursa_clasa, f), os.path.join(dest_clasa, f))
                
            print(f"   -> Am mutat {numar_test} imagini din clasa '{clasa}' în Test.")

    print("✅ Împărțire completă!")

if __name__ == "__main__":
    # ATENTIE: Ruleaza asta doar o singura data, altfel tot muti poze!
    pass 
    # Decomenteaza linia de mai jos ca sa rulezi:
    # imparte_datele()