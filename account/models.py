from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('EXEC', 'Exécutif'),
        ('REP', 'Représentant'),
    ]
    FUNCTION_CHOICES = [
        ('PRESIDENT', 'Président'),
        ('VICE_P', 'Vice-président'),
        ('SEC', 'Secrétaire'),
        ('COM', 'Chargé a la communication'),
        ('NUM', 'Chargé au numérique'),
        ('ACOM', 'Chargé adjoint a la communication'),
        ('ANUM', 'Chargé adjoint au numérique'),
    ]
    DEPARTEMENTS_CHOICES = [
        ('BA', 'Administration des affaires'),
        ('G.CIVIL', 'Génie civil'),
        ('BTS', 'BTS'),
        ('SEG', 'Sciences économiques et gestion'),
        ('GLT', 'Génie logiciel et transport'),
        ('D', 'Droit'),
        ('G.I', 'Génie informatique'),
        ('JC', 'Journalisme et communication'),
]

    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)
    departement = models.CharField(max_length=20, choices=DEPARTEMENTS_CHOICES, blank=True, null=True)
    function = models.CharField(max_length=100, choices=FUNCTION_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
