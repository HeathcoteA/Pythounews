from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from .. app import db, login


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_nom = db.Column(db.Text, nullable=False)
    user_bio = db.Column(db.Text, nullable=True)
    user_promo = db.Column(db.Integer, nullable=True)
    user_login = db.Column(db.String(45), nullable=False, unique=True)
    user_email = db.Column(db.Text, nullable=False)
    user_password = db.Column(db.String(100), nullable=False)
    user_spe = db.Column(db.Text, nullable=True)
    #user_publication_id = db.relationship("Publication", back_populates="publi_auteur_id")

    @staticmethod
    def identification(login, motdepasse):
        """ Identifie un utilisateur. Si cela fonctionne, renvoie les données de l'utilisateurs.

        :param login: Login de l'utilisateur
        :param motdepasse: Mot de passe envoyé par l'utilisateur
        :returns: Si réussite, données de l'utilisateur. Sinon None
        :rtype: User or None
        """
        utilisateur = User.query.filter(User.user_login == login).first()
        print(utilisateur)
        print(motdepasse)
        print(utilisateur.user_password)
        if utilisateur and check_password_hash(utilisateur.user_password, motdepasse):
            return utilisateur
        return None

    @staticmethod
    def creer(login, email, nom, motdepasse, bio, promo, spe):
        """ Crée un compte utilisateur-rice. Retourne un tuple (booléen, User ou liste).
        Si il y a une erreur, la fonction renvoie False suivi d'une liste d'erreur
        Sinon, elle renvoie True suivi de la donnée enregistrée

        :param login: Login de l'utilisateur-rice
        :param email: Email de l'utilisateur-rice
        :param nom: Nom de l'utilisateur-rice
        :param motdepasse: Mot de passe de l'utilisateur-rice (Minimum 6 caractères)
        :param promo: Année de promotion de l'utilisateur-rice
       :param bio: Courte biographie de l'utilisateur-rice

        """
        erreurs = []
        if not login:
            erreurs.append("Le login fourni est vide")
        if not email:
            erreurs.append("L'email fourni est vide")
        if not nom:
            erreurs.append("Le nom fourni est vide")
        if not motdepasse or len(motdepasse) < 6:
            erreurs.append("Le mot de passe fourni est vide ou trop court")
        if not promo :
            erreurs.append("La promo fournie est vide")


            # On vérifie que personne n'a utilisé cet email ou ce login
        uniques = User.query.filter(
            db.or_(User.user_email == email, User.user_login == login)
        ).count()
        if uniques > 0:
            erreurs.append("L'email ou le login sont déjà inscrits dans notre base de données")

        # Si on a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs

        # On crée un utilisateur
        utilisateur = User(
            user_nom=nom,
            user_login=login,
            user_email=email,
            user_password=generate_password_hash(motdepasse),
            user_bio=bio,
            user_promo=promo,
            user_spe=spe,
        )
        print(utilisateur)
        print(erreurs)
        try:
            # On l'ajoute au transport vers la base de données
            db.session.add(utilisateur)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, utilisateur
        except Exception as erreur:
            return False, [str(erreur)]

    def get_id(self):
        """ Retourne l'id de l'objet actuellement utilisé

        :returns: ID de l'utilisateur
        :rtype: int
        """
        return self.user_id

    def to_jsonapi_dict(self):
        """ It ressembles a little JSON API format but it is not completely compatible

        :return:
        """
        return {
            "type": "people",
            "attributes": {
                "name": self.user_nom

            }
        }

    @login.user_loader
    def trouver_utilisateur_via_id(identifiant):
        return User.query.get(int(identifiant))


    @staticmethod
    def modif_profil(user_id, login, email, nom, bio, promo, spe):
        """
        Méthode statique pour mettre à jour les informations sur l'utilisateur
        :param login:
        :param email:
        :param nom:
        :param motdepasse:
        :param bio:
        :param promo:
        :param spe:
        :return: Si tout va bien "True" et utilisatueur, sinon "False" et les erreurs rencontrées dans un tableau
        """
        erreurs = []
        if not nom:
            erreurs.append("Le nom est obligatoire")
        if not email:
            erreurs.append("L'email est obligatoire")
        if not login:
            erreurs.append("Le login est obligatoire")


        # On vérifie que personne n'a utilisé cet email ou ce login


        # Si on a au moins une erreur
        if len(erreurs) > 0:
            return False, erreurs

        utilisateur = User.query.get(user_id)

        print(utilisateur)
        utilisateur.user_nom = nom
        utilisateur.user_email = email
        utilisateur.user_login = login
        utilisateur.user_bio = bio
        utilisateur.use_spe = spe
        utilisateur.user_promo = promo

        try:

            # On l'ajoute au transport vers la base de données
            db.session.add(utilisateur)
            # On envoie le paquet
            db.session.commit()

            # On renvoie l'utilisateur
            return True, utilisateur

        except Exception as erreur:
            return False, [str(erreur)]
