import os

FOLDER_DATE = '../imagini antrenare'

def redenumire_standard():
    print("🏷️ Redenumesc fișierele pentru standardizare...")
    
    categorii = os.listdir(FOLDER_DATE)
    
    for cat in categorii:
        cale_categorie = os.path.join(FOLDER_DATE, cat)
        if os.path.isdir(cale_categorie):
            fisiere = os.listdir(cale_categorie)
            # Prefixul va fi numele folderului (ex: date_conforme_0.jpg)
            prefix = cat.replace(" ", "_").lower()
            
            for i, fisier in enumerate(fisiere):
                extensie = os.path.splitext(fisier)[1]
                nume_nou = f"{prefix}_{i}{extensie}"
                
                cale_veche = os.path.join(cale_categorie, fisier)
                cale_noua = os.path.join(cale_categorie, nume_nou)
                
                os.rename(cale_veche, cale_noua)
                
    print("✅ Toate fișierele au fost redenumite standardizat.")

if __name__ == "__main__":
    # Decomenteaza linia de mai jos pentru a redenumi tot:
    # redenumire_standard()
    pass