# Documentație: Justificarea euristicilor și ponderilor utilizate

## 1. Introducere
Euristica este o funcție care estimează cât de favorabilă este o stare a jocului sau cât de aproape este un nod de scop într-un graf. În acest proiect, euristicile sunt utilizate în două contexte:
- **Nine Men's Morris**: Evaluarea stării tablei pentru algoritmii Minimax și Alpha-Beta.
- **A*** și **IDA***: Estimarea distanței de la un nod la nodurile scop.

---

## 2. Justificarea euristicii pentru A* și IDA*
Pentru algoritmii A* și IDA*, euristica folosește **distanța euclidiană** între noduri. Aceasta este definită ca:

$$
h(n) = \min_{goal \in goals} \sqrt{(x_n - x_{goal})^2 + (y_n - y_{goal})^2}
$$

### a. Motivație
- **Distanța euclidiană** oferă o estimare consistentă și admisibilă a costului minim de la un nod la scop.
- Este simplu de calculat și reflectă bine structura grafului.

### b. Proprietăți
- **Admisibilitate**: Euristica nu supraestimează costul real, garantând soluții optime.
- **Consistență**: Diferența dintre euristica a două noduri adiacente este cel mult costul arcului dintre ele.

---

## 3. Justificarea ponderilor pentru Nine Men's Morris
Funcția de evaluare pentru Nine Men's Morris combină mai mulți factori relevanți pentru joc, fiecare având o pondere specifică:

### a. Diferența de piese pe tablă *(Pondere: 3)*
- **Motivare**: Mai multe piese oferă mai multe opțiuni de mutare și control strategic.
- **Pondere moderată**: Este importantă, dar nu decisivă, deoarece alte elemente (ex. morile) au un impact mai mare.

### b. Diferența de mori formate *(Pondere: 6)*
- **Motivare**: Mori formate permit eliminarea pieselor adversarului, reducând mobilitatea acestuia.
- **Pondere mare**: Formarea morilor este un obiectiv principal al jocului, având un impact direct asupra rezultatului.

### c. Mobilitatea *(Pondere: 1)*
- **Motivare**: Reflectă flexibilitatea strategică a unui jucător. Un jucător blocat pierde controlul jocului.
- **Pondere mică**: Este un factor secundar, dar contribuie la evaluarea generală.

### d. Mori potențiale *(Pondere: 2)*
- **Motivare**: Indică oportunități viitoare de a forma mori și de a elimina piese ale adversarului.
- **Pondere moderată**: Este mai puțin importantă decât morile deja formate, dar influențează strategia pe termen lung.

### e. Piese blocate *(Pondere: 1)*
- **Motivare**: Piesele blocate reduc opțiunile adversarului și îl apropie de înfrângere.
- **Pondere mică**: Este un factor suplimentar, dar nu decisiv.

### f. Condiții de final de joc *(Scoruri: ±1000)*
- **Motivare**: Dacă un jucător are 2 sau mai puține piese sau nu mai poate muta, jocul se termină.
- **Scor mare**: Aceste condiții determină rezultatul final, având prioritate absolută.

---

## 4. Concluzie
Euristica și ponderile utilizate sunt bine alese pentru a reflecta obiectivele și strategiile fiecărui context:
- În **Nine Men's Morris**, ponderile prioritizează morile și condițiile de final de joc, fără a neglija mobilitatea și piesele blocate.
- În **A*** și **IDA***, distanța euclidiană asigură o estimare eficientă și corectă a costurilor.
