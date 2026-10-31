// VIBES · réception des réponses du questionnaire dans une feuille Google Sheets.
// À coller dans Extensions > Apps Script de la feuille (voir LISEZ-MOI.md).
const COLONNES = ["envoye_le","version","ecole","niveau","arrivee","logement","tel","tel_avis","libre","freins","compagnie","ecoute","budget","connexion","interet","libre_texte","citation"];

function doPost(e) {
  const verrou = LockService.getScriptLock();
  verrou.waitLock(10000);
  try {
    const d = JSON.parse(e.postData.contents);
    const feuille = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Réponses") || SpreadsheetApp.getActiveSpreadsheet().insertSheet("Réponses");
    if (feuille.getLastRow() === 0) feuille.appendRow(COLONNES);
    feuille.appendRow(COLONNES.map(c => String(d[c] == null ? "" : d[c]).slice(0, 800)));
    return ContentService.createTextOutput("ok");
  } finally {
    verrou.releaseLock();
  }
}

function doGet() { return ContentService.createTextOutput("VIBES questionnaire : actif"); }
