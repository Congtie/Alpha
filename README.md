# Documentație: Implementarea jocului Nine Men's Morris

Această documentație explică abordările utilizate pentru rezolvarea jocului **Nine Men's Morris** în cadrul proiectului. Sunt prezentate trei metode distincte:
1. **Algoritmi de căutare euristică (A* și IDA*)** - Fișier: `main.py`
2. **Algoritmi Minimax și Alpha-Beta pruning** - Fișier: `improved-nine-mens-morris.py`
3. **Decizii Bayesiene** - Fișier: `main2.py`

---

## 1. Introducere
**Nine Men's Morris** este un joc strategic în care scopul este de a forma "mori" (linii de trei piese) pentru a elimina piesele adversarului. Implementarea proiectului include trei abordări diferite pentru a determina cea mai bună mutare:
- **Căutare euristică**: Folosind algoritmi precum A* și IDA* pentru a găsi drumul optim către o stare câștigătoare.
- **Algoritmi Minimax și Alpha-Beta pruning**: Pentru a explora toate mutările posibile și a alege cea mai bună mutare pe baza evaluării stării tablei.
- **Decizii Bayesiene**: Pentru a calcula probabilitatea de câștig pe baza factorilor relevanți și a selecta mutarea cu cea mai mare probabilitate de succes.

---

## 2. Algoritmi de căutare euristică (A* și IDA*) - `main.py`

### a. Descriere
Fișierul `main.py` implementează algoritmii **A*** și **IDA*** pentru a găsi drumul optim către o stare câștigătoare. Euristica utilizată este distanța euclidiană între poziția curentă și nodurile scop.

### b. Euristica utilizată
Euristica este definită ca:

$$h(n) = \min_{goal \in goals} \sqrt{(x_n - x_{goal})^2 + (y_n - y_{goal})^2}$$

Aceasta garantează admisibilitatea și consistența, asigurând soluții optime.

### c. Implementare
- **A***: Utilizează o coadă de priorități pentru a explora nodurile cu cel mai mic cost `f = g + h`.
- **IDA***: Extinde căutarea iterativă pe baza unei limite de cost, utilizând backtracking recursiv.

### d. Avantaje și Dezavantaje
- **Avantaje**: Găsește soluții optime și este eficient pentru grafuri bine definite.
- **Dezavantaje**: Nu este specific pentru Nine Men's Morris și poate fi mai lent pentru jocuri complexe.

---

## 3. Algoritmi Minimax și Alpha-Beta pruning - `improved-nine-mens-morris.py`

### a. Descriere
Fișierul `improved-nine-mens-morris.py` implementează algoritmii **Minimax** și **Alpha-Beta pruning** pentru a explora toate mutările posibile și a determina cea mai bună mutare.

### b. Funcția de evaluare
Funcția de evaluare combină mai mulți factori relevanți pentru joc:
1. **Diferența de piese** *(Pondere: 3)*: Mai multe piese oferă mai multe opțiuni de mutare.
2. **Diferența de mori formate** *(Pondere: 6)*: Mori formate oferă un avantaj decisiv.
3. **Mobilitatea** *(Pondere: 1)*: Reflectă flexibilitatea strategică.
4. **Mori potențiale** *(Pondere: 2)*: Indică oportunități viitoare de a forma mori.
5. **Piese blocate** *(Pondere: 1)*: Reduc opțiunile adversarului.

### c. Implementare
- **Minimax**: Explorează toate mutările posibile până la o adâncime specificată.
- **Alpha-Beta pruning**: Optimizează Minimax prin eliminarea ramurilor inutile.

### d. Avantaje și Dezavantaje
- **Avantaje**: Specific pentru jocuri strategice precum Nine Men's Morris.
- **Dezavantaje**: Consumă mult timp pentru adâncimi mari.

---

## 4. Decizii Bayesiene - `main2.py`

### a. Descriere
Fișierul `main2.py` implementează o abordare bazată pe **Rețele Bayesiene** pentru a calcula probabilitatea de câștig pentru jucătorul `x` și a selecta mutarea optimă.

### b. Factori utilizați în evaluare
1. **Formarea morilor (Pondere: 0.4)**  
   - Mori formate permit eliminarea pieselor adversarului.
2. **Blocarea morilor adversarului (Pondere: 0.3)**  
   - Previne pierderea pieselor proprii.
3. **Numărul de piese pe tablă (Pondere: 0.2)**  
   - Mai multe piese oferă mai multe opțiuni de mutare.
4. **Poziții strategice (Pondere: 0.1)**  
   - Pozițiile centrale oferă un avantaj strategic.

### c. Calculul probabilității de câștig
Probabilitatea de câștig este calculată folosind o combinație liniară a factorilor:

$$P_{win}(x) = 0.4 \cdot \text{mills} + 0.3 \cdot \text{blocking} + 0.2 \cdot \text{pieces} + 0.1 \cdot \text{strategic}$$

### d. Avantaje și Dezavantaje
- **Avantaje**: Flexibilitate și robustețe în evaluarea stării tablei.
- **Dezavantaje**: Necesită ajustarea manuală a ponderilor pentru a reflecta strategia optimă.

---

## 5. Concluzie
Cele trei abordări oferă perspective diferite pentru rezolvarea jocului **Nine Men's Morris**:
- **A*** și **IDA*** sunt utile pentru căutarea generală în grafuri.
- **Minimax** și **Alpha-Beta pruning** sunt ideale pentru jocuri strategice.
- **Deciziile Bayesiene** oferă o metodă probabilistică pentru evaluarea stării tablei.

Fiecare metodă are avantaje și dezavantaje, iar alegerea depinde de contextul specific al jocului și de cerințele de performanță.