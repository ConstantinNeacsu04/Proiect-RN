# 📘 README – Etapa 3: Analiza și Pregătirea Setului de Date pentru Rețele Neuronale

**Disciplina:** Rețele Neuronale  
**Instituție:** POLITEHNICA București – FIIR  
**Student:** Neacsu Constantin-Cristian 
**Data:** 20.11.2025

---

## Introducere

Acest document descrie activitățile realizate în **Etapa 3**, în care se analizează și se preprocesează setul de date necesar proiectului „Rețele Neuronale". Scopul etapei este pregătirea corectă a datelor pentru instruirea modelului RN, respectând bunele practici privind calitatea, consistența și reproductibilitatea datelor.

---

##  1. Structura Repository-ului Github (versiunea Etapei 3)

```
project-name/
├── README.md
├── docs/
│   └── datasets/          # descriere seturi de date, surse, diagrame
├── data/
│   ├── raw/               # date brute
│   ├── processed/         # date curățate și transformate
│   ├── train/             # set de instruire
│   ├── validation/        # set de validare
│   └── test/              # set de testare
├── src/
│   ├── preprocessing/     # funcții pentru preprocesare
│   ├── data_acquisition/  # generare / achiziție date (dacă există)
│   └── neural_network/    # implementarea RN (în etapa următoare)
├── config/                # fișiere de configurare
└── requirements.txt       # dependențe Python (dacă aplicabil)
```

---

##  2. Descrierea Setului de Date

### 2.1 Sursa datelor

* **Origine:** Google
* **Modul de achiziție:** ☐ Senzori reali / ☐ Simulare / X Fișier extern / ☐ Generare programatică
* **Perioada / condițiile colectării:**  Noiembrie 2025 - Ianuarie 2026
### 2.2 Caracteristicile dataset-ului

* **Număr total de observații:** 120   
* **Număr de caracteristici (features):**Matrice de pixeli
* **Tipuri de date:** ☐ Numerice / ☐ Categoriale / ☐ Temporale / ✓ Imagini
* **Format fișiere:** ☐ CSV / ☐ TXT / ☐ JSON /  ✓PNG / ☐ Altele: [...]

### 2.3 Descrierea fiecărei caracteristici

Caracteristică   |Tip  |Unitate     |Descriere                  |Domeniu valori
Imagine Input    |Tensor |Pixeli (RGB)|Imaginea brută a frezei CNC|0 – 255 (int)
Imagine Procesată|Tensor |Float       |Imaginea redimensionată și normalizată|0.0 – 1.0 (float)
Etichetă (Label) |Categorial |Clasă       |Starea sculei (Conform / Neconform)|0 sau 1


**Fișier recomandat:**  `data/README.md`

---

##  3. Analiza Exploratorie a Datelor (EDA) – Sintetic

### 3.1 Statistici descriptive aplicate

Distribuția claselor: Calculul numărului de imagini per clasă (nr_conform vs nr_neconform) pentru a verifica balansul datelor.
Dimensiuni: Verificarea consistenței dimensiunilor imaginilor înainte de redimensionare.
### 3.2 Analiza calității datelor

Validarea vizuală a imaginilor încărcate (verificarea încadrării subiectului).
Verificarea separării corecte în folderele conform și neconform.
### 3.3 Probleme identificate

Volum mic de date: Număr redus de imagini pentru Deep Learning, necesită Data Augmentation (posibilă îmbunătățire viitoare).
Variabilitate: Posibile diferențe de iluminare sau unghi între pozele de antrenare și cele de test.
##  4. Preprocesarea Datelor

### 4.1 Curățarea datelor

* **Eliminare duplicatelor**
* **Tratarea valorilor lipsă:**
  * Feature A: imputare cu mediană
  * Feature B: eliminare (30% valori lipsă)
* **Tratarea outlierilor:** IQR / limitare percentile

### 4.2 Transformarea caracteristicilor

Redimensionare (Resizing): Toate imaginile sunt aduse la dimensiunea 180x180 px (IMG_SIZE).
Normalizare (Rescaling): Valorile pixelilor sunt împărțite la 255 (layers.Rescaling(1./255)), transformând intervalul [0, 255] în [0, 1] pentru convergența mai rapidă a rețelei neuronale.
### 4.3 Structurarea seturilor de date

**Împărțire recomandată:**
* 80% – Train (pentru antrenarea ponderilor modelului)
* 20% – Validation (pentru monitorizarea performanței în timpul epocilor)
* Test: Se realizează separat prin scriptul de verificare (verifica_scula) pe imagini complet noi.
**Principii respectate:**
* Amestecare automat al datelor la antrenare.
### 4.4 Salvarea rezultatelor preprocesării

* Date preprocesate în `data/processed/`
* Seturi train/val/test în foldere dedicate
* Parametrii de preprocesare în `config/preprocessing_config.*` (opțional)

---

##  5. Fișiere Generate în Această Etapă

* dataset_auto/ – folderul cu datele brute organizate.
* model_scule_cnc.keras – modelul final antrenat.
* Istoric antrenare – disponibil pentru plotare grafice.
##  6. Stare Etapă (de completat de student)

- [x] Structură repository configurată
- [x] Dataset analizat (EDA realizată)
- [x] Date preprocesate
- [x] Seturi train/val/test generate
- [x] Documentație actualizată în README + `data/README.md`

---
