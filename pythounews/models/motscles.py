# -*- coding: utf-8 -*-

from ..app import db
from .publications import Publication
from .utilisateurs import User


# Table pour stocker les mots-clés
class Motscles(db.Model):
    motscles_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    motscles_nom = db.Column(db.Text, nullable=False)
    sujetpublis = db.relationship("Sujet_publi", back_populates="motscles")
    sujetfluxrss = db.relationship("Sujet_fluxrss", back_populates="motscles")

class Sujet_publi(db.Model):
    sujet_publi_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    sujet_publi_publication_id = db.Column(db.Integer, db.ForeignKey('publication.publication_id'), nullable=False)
    sujet_publi_motscles_id = db.Column(db.Integer, db.ForeignKey('motscles.motscles_id'), nullable=False)
    motscles = db.relationship("Motscles", back_populates="sujetpublis")
    publication = db.relationship("Publication", back_populates="sujetpublis")

    @staticmethod
    def ajouter_categorie(categorie, donnees):
        """ Ajout de la catégorie de la publication en fonction de ce que l'utilisateur a coché

        :param categorie: mots clés choisis par l'utilisateur
        :type categorie: list
        :param donnees: données rentrées par l'utilisateur (A CHANGER !!!)
        :type donnees: list
        :return: page de publication correspond au mot clé
        """
        for mot in categorie:
            if mot is not None:
                mot_id = Motscles.query.filter(Motscles.motscles_nom == mot).first()
                sujetpubli = Sujet_publi(
                    sujet_publi_publication_id=donnees.publication_id,
                    sujet_publi_motscles_id=mot_id.motscles_id
                )
        db.session.add(sujetpubli)
        db.session.commit()

    @staticmethod
    def afficher_publi_categorie(motcle):
        """ Affichage des publication ayant un mot-clé particulier

        :param motcle: mot-clé demandé
        :return: liste des publication ayant ce mot-clé
        """
        liste_publications = []
        publications = Publication.query.filter(Sujet_publi.sujet_publi_motscles_id == motcle.motscles_id).paginate(page=1, per_page=8)
        for item in publications.items:
            titre = item.publication_nom
            date = item.publication_date
            lien = item.publication_lien
            texte = item.publication_texte
            auteur = User.query.get(item.publi_user_id)
            description_url = item.publication_description_url
            titre_url = item.publication_titre_url

            liste_publications.append(
                {"titre": titre, "date": date, "lien": lien, "texte": texte, "titre_url": titre_url,
                 "description_url": description_url, "auteur": auteur})
        return liste_publications
