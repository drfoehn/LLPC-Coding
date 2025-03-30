document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('labForm');
    const resultContainer = document.getElementById('result');
    const resultDetails = document.getElementById('resultDetails');
    const totalScoreElement = document.getElementById('totalScore');

    // Gewichtungen für die verschiedenen Kategorien
    const categoryWeights = {
        preanalytical: 1,    // a) Präanalytischer Aufwand
        analytical: 1,       // b) Analytischer Aufwand
        expertise: 1,        // c) Analytischer Aufwand (Expertise)
        postanalytical: 1,   // d) Postanalytischer Aufwand
        administrative: 1,   // e) Administrativer Aufwand
        invasiveness: 1,     // f) Invasivität
        timeRequired: 1      // g) Benötigte Zeit
    };

    // Kategorie-Namen für die Anzeige
    const categoryNames = {
        preanalytical: 'Präanalytischer Aufwand',
        analytical: 'Analytischer Aufwand',
        expertise: 'Analytischer Aufwand (Expertise)',
        postanalytical: 'Postanalytischer Aufwand',
        administrative: 'Administrativer Aufwand',
        invasiveness: 'Invasivität der Probenentnahme',
        timeRequired: 'Benötigte Zeit für die Analyse'
    };

    // Material-Namen für die Anzeige
    const materialNames = {
        blood: 'Blut',
        urine: 'Harn',
        csf: 'Liquor',
        punctate: 'Punktat',
        swab: 'Abstrich',
        stool: 'Stuhl',
        tissue: 'Gewebe',
        other: 'Sonstiges'
    };

    form.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Hole die Grundinformationen
        const loincCode = form.loincCode.value;
        const parameterName = form.parameterName.value;
        const material = form.material.value;

        // Sammle alle Werte aus den Select-Feldern
        const values = {};
        let totalScore = 0;
        let llpcSuffix = '';

        // Berechne Summe und erstelle LLPC-Code
        Object.keys(categoryWeights).forEach(category => {
            const value = parseInt(form[category].value);
            values[category] = value;
            totalScore += value * categoryWeights[category];
            llpcSuffix += value;
        });

        // Erstelle LLPC-Code
        const llpcCode = `${loincCode}_${llpcSuffix}`;

        // Bestimme Aufwandskategorie
        let aufwandsBewertung = '';
        if (totalScore <= 15) {
            aufwandsBewertung = 'Geringer oder rein administrativer Aufwand';
        } else if (totalScore <= 30) {
            aufwandsBewertung = 'Mittlerer Aufwand';
        } else {
            aufwandsBewertung = 'Hoher Aufwand';
        }

        // Zeige Ergebnisse an
        resultDetails.innerHTML = `
            <div class="result-header">
                <div class="result-item">
                    <span>LOINC-Code:</span>
                    <span>${loincCode}</span>
                </div>
                <div class="result-item">
                    <span>Laborparameter:</span>
                    <span>${parameterName}</span>
                </div>
                <div class="result-item">
                    <span>Material:</span>
                    <span>${materialNames[material]}</span>
                </div>
                <div class="result-item">
                    <span>LLPC-Code:</span>
                    <span>${llpcCode}</span>
                </div>
            </div>
            <div class="category-scores">
                <h3>Einzelbewertungen:</h3>
        `;

        Object.keys(values).forEach(category => {
            resultDetails.innerHTML += `
                <div class="result-item">
                    <span>${categoryNames[category]}:</span>
                    <span>${values[category]} Punkte</span>
                </div>
            `;
        });

        totalScoreElement.innerHTML = `
            <div class="total-score">
                <strong>Gesamtpunktzahl:</strong> ${totalScore} Punkte
            </div>
            <div class="effort-category">
                <strong>Aufwandsbewertung:</strong> ${aufwandsBewertung}
            </div>
        `;

        // Zeige Ergebnis-Container
        resultContainer.style.display = 'block';
        resultContainer.classList.add('visible');

        // Scrolle zum Ergebnis
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    });
}); 