from..app import db
from bs4 import BeautifulSoup
import requests
import time
import datetime
from flask_login import current_user

#Table pour stocker les publication des utilisateurs
class Publication(db.Model):
    publication_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    publication_date = db.Column(db.Text, nullable=False)
    publication_nom = db.Column(db.String(40), nullable=True)
    publication_lien = db.Column(db.Integer, nullable=True)
    publication_texte = db.Column(db.Text, nullable=False, unique=True)
    sujetpublis = db.relationship("Sujet_publi", back_populates="publication")
    publication_auteur = db.Column(db.Text, nullable=False)


    @staticmethod
    def creer_publication(titre, date, lien, texte, auteur):
        """ Crée une nouvelle publication et renvoie les informations rentrées par l'utilisateur.

        :param titre: Titre de la publication
        :param date: Date de la publication
        :param lien: URL partagé par l'utilisateur
        :param texte: Texte écrit par l'utilisateur
        :returns: Si réussite, publication de l'utilisateur. Sinon None
        :rtype: Publication or None
        """
        erreurs = []

        if not titre:
            erreurs.append("Veuillez ajouter un titre à votre publication")

        if not lien:
            erreurs.append("Veuillez ajouter un lien à votre publication")

        if len(erreurs) > 0:
            return False, erreurs

        date = datetime.date.today()
        auteur = current_user

        publication = Publication(
            publication_nom=titre,
            publication_date=date,
            publication_lien=lien,
            publication_texte=texte,
            publication_auteur=auteur)

        try:
            db.session.add(publication)

            db.session.commit()

            return True, publication
        except Exception as erreur:
            return False, [str(erreur)]

    @staticmethod
    def afficher_publications():
        """ Affiche les publications des utilisateurs

        :return: affichage des publications
        """
        liste_publications = []
        publication = Publication.query.all()
        for item in publication:
            titre = item.publication_nom
            date = item.publication_date
            lien = item.publication_lien
            texte = item.publication_texte
            auteur = item.publication_auteur
            page_html = requests.get(lien)
            soup = BeautifulSoup(page_html.text, 'html.parser')
            description_url = soup.find("meta", attrs={"name":u"description"})
            titre_url = soup.title
            publi = titre, date, lien, texte, titre_url.get_text(), description_url, auteur
            liste_publications.append(publi)

        return liste_publications
