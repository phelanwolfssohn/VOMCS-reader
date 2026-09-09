# VOMCS Reader — Die optomechanische Dekodierungs-Engine
**Spezifikation v1.0 — Rekonstruktions- und Auslese-Standard**

Dieses Repository enthält die Architektur, Spezifikationen und Verarbeitungs-Pipelines für das VOMCS-Lesegerät (`vomcs-reader`). Es fungiert als direktes Spiegelbild zur *Writer-Engine* und übersetzt physische oder digitale 3D-Lichtstrukturen verlustfrei zurück in den ursprünglichen Bitstrom.

---

## ⚙️ Funktionsweise des Lesegeräts (Die Dekodierungs-Pipeline)

Der Reader arbeitet als dreistufige Hardware-Software-Pipeline, um aus dem passiven Speichermedium die relationalen Inode-Sequenzen zu rekonstruieren:

[Physischer Würfel] ➔ [1. Optomechanischer Scan] ➔ [2. Bildverarbeitung/Kalibrierung] ➔ [3. Muster-Extraktion] ➔ [Klartext-Datei]


### 1. Die Hardware-Schnittstelle (Optomechanischer Schicht-Abtaster)
Um den mit dem *Elegoo Mars* produzierten 6-cm-Zauberwürfel (oder jede andere Polyeder-Klasse) kostengünstig auszulesen, wird ein standardisiertes Low-Cost-Lichtschnittverfahren (Light-Sheet Illumination) eingesetzt:
* **Der Schicht-Abtaster:** Ein fixierter Nah-Infrarot-Linienlaser (NIR, ca. 850 nm) wird mittels Glasoptik und einer mechanischen Spaltblende (z. B. Rasierklingen-Spalt) auf eine Strahltaille von **< 0,05 mm** fokussiert.
* **Die Präzisions-Achse:** Eine mechanische Linearachse (z. B. die zweckentfremdete Z-Achse eines 3D-Druckers) schiebt das VOMCS-Medium im exakten **0,2-mm-Takt** am Laserstrahl vorbei.
* **Der Sensor:** Eine fest installierte Infrarot-Kamera ohne IR-Sperrfilter (z. B. *Raspberry Pi NoIR-Kamera*) fotografiert bei jedem mechanischen Stopp die aktuell illuminierte Schicht senkrecht von vorne.

### 2. Digitale Bildverarbeitung & Raum-Kalibrierung
Die erfassten Graustufenbilder werden im RAM des Host-Rechners einer zweistufigen digitalen Reinigung unterzogen:
* **Binarisierung:** Ein technischer Schwellenwert-Filter (Threshold) trennt das gestreute NIR-Licht der Datenschlieren vom klaren Harzkörper. Glimmende Pixel werden als harte `1`, dunkle Bereiche als `0` definiert.
* **Anker-Kalibrierung:** Die Software sucht in der mathematischen Mitte (z. B. Schicht 150 beim 300er-Modell) nach dem permanent fixierten **Zentral-Hardware-Marker**. Eventuelle mechanische Schieflagen oder Verzerrungen des Würfels im Leseschacht werden anhand dieses Fixpunkts rechnerisch in Echtzeit korrigiert. Nach 300 Iterationen liegt eine fehlerfreie, digitale $300 \times 300 \times 300$ Bit-Matrix im Speicher vor.

### 3. Geometrische Muster-Extraktion (Die Inode-Schicht)
Nachdem die digitale Matrix rekonstruiert wurde, verarbeitet der Reader die empfangene Inode-Pointerliste. Er liest die Daten nicht linear aus, sondern wirft die im Pointer hinterlegte **Muster-ID** an, um die Bitkette exakt entlang des ursprünglichen Geometrie-Pfades abgreifen:
* **Muster `0x01` (Spirale):** Startet an den Außenkanten und rotiert nach innen.
* **Muster `0x02` (Hilbert-Kurve):** Faltet den fraktalen Pfad aus dem Raum.
* **Muster `0x03` (Boustrophedon):** Tastet das klassische Zickzack-Raster ab.

---

## 📄 Lizenz & Rechtlicher Hinweis
Dieses Projekt ist lizenziert unter den Bedingungen der **Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0)**. 

Die private, wissenschaftliche und gemeinnützige Nutzung, Modifikation, digitale Simulation und Weiterentwicklung ist ausdrücklich erlaubt und kostenfrei. Jegliche kommerzielle Nutzung, Verwertung im geschäftlichen Betrieb (physisch oder als Software-Implementierung) oder die Einbindung in proprietäre Produkte ist ohne vorherige, schriftliche Genehmigung und Lizenzierung durch den Urheber untersagt.
