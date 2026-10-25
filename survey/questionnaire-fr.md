# VIBES · Questionnaire étudiants (≈ 2 minutes)

À copier dans Google Forms. Réponses anonymes, aucun champ nom, téléphone ou e-mail. Ne pas activer « collecter les adresses e-mail ». Cocher « une réponse par personne » seulement si cela n'impose pas de compte (sinon laisser décoché et surveiller les doublons).

## Introduction (texte du formulaire)
Nous sommes des étudiants de l'UNSTIM et nous concevons VIBES, un projet de bien-être étudiant : trouver des gens qui partagent tes passions, prendre un moment pour soi, installer de petites habitudes. Ce questionnaire est **anonyme**, **facultatif** et dure environ 2 minutes. Il ne pose **aucune question médicale** et ne remplace pas un avis de professionnel. Les résultats serviront à améliorer le projet et seront présentés de façon globale. Tu peux t'arrêter à tout moment.

## Questions

**1. Tu es en quelle année ?** (une réponse) L1 · L2 · L3 · Master 1 · Master 2 · Autre

**2. Tu es arrivé(e) à l'UNSTIM...** (une réponse) cette année · il y a 1 à 2 ans · il y a plus de 2 ans

**3. Tu habites...** (une réponse) chez ma famille · en cité ou résidence universitaire · en location, seul(e) ou en colocation · autre

**4. Combien de temps passes-tu sur ton téléphone chaque jour, sur tes temps libres (réseaux, vidéos, jeux, anime, manga) ?** (une réponse, estimation) moins d'1 h · 1 à 2 h · 2 à 4 h · 4 à 6 h · plus de 6 h

**5. Ce temps te convient-il ?** (une réponse) il est trop long pour moi · il me convient · il est plutôt court

**6. Sur tes temps libres, que fais-tu le plus souvent ?** (plusieurs réponses, 3 maximum) réseaux sociaux / vidéos · jeux vidéo · séries, films, anime, manga · sport · sorties avec des amis · révisions ou travail de groupe · activités culturelles ou associatives · repos, sommeil · autre

**7. Qu'est-ce qui t'empêche le plus de faire des activités hors écran ?** (plusieurs réponses, 3 maximum) je ne sais pas ce qui existe · je n'ai pas le budget · je n'ai personne avec qui y aller · c'est trop loin · je suis timide ou je n'ose pas · manque de temps · je ne me sens pas en sécurité · rien de particulier · autre

**8. Ces deux dernières semaines, tu as manqué de compagnie...** (une réponse) jamais · rarement · parfois · souvent · je préfère ne pas répondre

**9. Combien serais-tu prêt(e) à dépenser pour une activité de groupe ?** (une réponse) rien · jusqu'à 500 FCFA · 500 à 1 000 FCFA · 1 000 à 2 000 FCFA · plus de 2 000 FCFA

**10. Comment décrirais-tu ta connexion internet ?** (une réponse) forfait data limité, je fais attention · forfait suffisant · wifi surtout (campus, maison) · variable

**11. Description courte :** « VIBES serait une application légère pour trouver des activités et des gens qui partagent tes passions, noter ton humeur en privé et recevoir de petits conseils écrits par des jeunes béninois. » **Serais-tu intéressé(e) pour l'essayer ?** (une réponse) oui · peut-être · non

**12. Pourquoi (en une phrase) ?** (réponse libre, facultative)

**13. Une chose qui t'aiderait à poser ton téléphone plus souvent ?** (réponse libre, facultative)

**14.** ☐ J'accepte que ma réponse à la question 12 ou 13 soit citée **de façon anonyme** (sans nom). (case facultative)

## Message de fin
Merci. Si tu as besoin de parler, adresse-toi à une personne de confiance ou à un service de santé de ton établissement.

---

## Comment collecter proprement
- Diffuser sur plusieurs groupes WhatsApp (filières et années différentes), pas seulement ton entourage. Noter les groupes utilisés.
- Fixer une date de clôture avant de lire les résultats (ex. 29 octobre) et la noter.
- Ne pas relancer en insistant sur un type de réponse, ne pas offrir de cadeau, ne pas supprimer de réponses « gênantes ».
- Compter le nombre de réponses (n) et la période. Ne pas arrondir à la hausse.

## Comment présenter (modèles, à remplir avec les vrais chiffres)
- Méthode : « Court questionnaire anonyme auprès d'étudiants de l'UNSTIM, du [date] au [date], n = [N], diffusé par [groupes]. Échantillon non représentatif. »
- Un chiffre : « Sur [N] étudiants, [X] % déclarent [résultat], [Y] % [résultat]. »
- Une citation (seulement si la case 14 est cochée) : « [phrase exacte] », étudiant(e) de [année].
- Limites à écrire : échantillon de commodité, réponses déclaratives, aucun lien de cause.

## Analyse
Exporter les réponses en CSV (Google Forms : Réponses > Feuille de calcul > Fichier > Télécharger > CSV) puis :
`python3 survey/analyze.py reponses.csv`
