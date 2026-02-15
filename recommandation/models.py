from django.db import models
from django.utils.text import slugify

class Message(models.Model):
    DEPARTEMENT_CHOICES = [
        ('BA', 'Business Administration'),
        ('G.CIVIL', 'Génie Civil'),
        ('BTS', 'BTS'),
        ('SEG', 'Sciences Economiques et Gestion'),
        ('GLT', 'Génie Logiciel et Transport'),
        ('D', 'Droit'),
        ('G.I', 'Génie Informatique'),
        ('JC', 'Journalisme et Communication'),
    ]
    LEVEL_CHOICES = [
        ('L1', 'L1' ),
        ('L2', 'L2' ),
        ('L3', 'L3' ),
        ('L4', 'L4' ),
        ('L5', 'L5' ),
    ]
    MESSAGE_TYPE_CHOICES = [
        ('SUG', 'Suggestion'),
        ('PLT', 'Plainte'),
        ('RMQ', 'Remarque'),
    ]
    slug = models.SlugField(unique=True)
    departement = models.CharField(max_length=20, choices=DEPARTEMENT_CHOICES,blank=False, null=False )
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES, blank=False, null=False)
    message_type = models.CharField(max_length=3, choices=MESSAGE_TYPE_CHOICES, blank=False, null=False)
    content = models.TextField(max_length=1000, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return self.message_type + " - " + self.departement + " - " + self.level

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.departement}-{self.level}-{self.message_type}")
            slug = base_slug
            counter = 1
            while Message.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)