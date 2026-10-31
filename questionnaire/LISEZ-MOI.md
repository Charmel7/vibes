# Questionnaire VIBES : mise en route (5 minutes, gratuit)

Les réponses arrivent dans une feuille Google Sheets que toi seul(e) peux ouvrir.

1. Crée une feuille Google Sheets vide, nommée par exemple « VIBES réponses ».
2. Menu **Extensions > Apps Script**. Supprime le code qui s'y trouve et colle le contenu de `apps-script.gs`. Enregistre.
3. **Déployer > Nouveau déploiement > Type : Application Web**.
   - Exécuter en tant que : **Moi**.
   - Qui a accès : **Tout le monde** (les étudiants n'ont pas besoin de compte Google).
   - Autorise l'accès quand Google le demande, puis copie l'**URL de l'application web** (elle finit par `/exec`).
4. Dans `questionnaire/index.html`, colle cette URL dans `const ENDPOINT = "";` puis publie le site.
5. Fais un test : réponds au questionnaire, une ligne doit apparaître dans l'onglet « Réponses ».

Le questionnaire est ensuite à l'adresse : `…/questionnaire/`.

Pas d'URL collée = mode démonstration : le formulaire fonctionne, mais rien n'est enregistré.
