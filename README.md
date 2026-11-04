# Générateur de flipbook

Ouvre `index.html` dans Chrome, dépose un PDF, télécharge le flipbook (HTML unique ou ZIP).
Tout se fait dans le navigateur (internet requis pour charger pdf.js et JSZip).

Reconstruire : `python make_template.py && python build.py`
(`base_flipbook.html` = flipbook source, `template.html` = modèle généré, `page-flip.js` = StPageFlip 2.0.7).
