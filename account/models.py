from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = [
        ('EXEC', 'Executif'),
        ('REP', 'Representant'),
    ]
    FUNCTION_CHOICES = [
        ('PRESIDENT', 'President'),
        ('VICE_P', 'Vice President'),
        ('SEC', 'Secretaire'),
        ('COM', 'Chargé a la communication'),
        ('NUM', 'Chargé au numérique'),
        ('ACOM', 'Chargé adjoint a la communication'),
        ('ANUM', 'Chargé adjoint au numérique'),
    ]
    DEPARTEMENTS_CHOICES = [
        ('BA', 'bUSINESS ADMINISTRATION'),   
        ('G.CIVIL', 'GENIE CIVIL'),
        ('BTS', 'BTS'),
        ('SEG', 'SCIENCES ECONOMIQUES ET GESTION'),
        ('GLT', 'GENIE LOGICIEL ET TRANSPORT'),
        ('D', 'DROIT'),
        ('G.I', 'GENIE INFORMATIQUE'),
        ('JC', 'JOURNALISME ET COMMUNICATION'),
]

    user_type = models.CharField(max_length=15, choices=USER_TYPE_CHOICES)
    departement = models.CharField(max_length=20, choices=DEPARTEMENTS_CHOICES, blank=True, null=True)
    function = models.CharField(max_length=100, choices=FUNCTION_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
