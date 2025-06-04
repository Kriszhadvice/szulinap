from django.db import models

# Create your models here.

class Ember(models.Model):
    teljesnev = models.CharField(max_length=255)
    becenev = models.CharField(max_length=255)
    szulinap = models.DateField()
    nevnap = models.DateField()
    ajandek = models.CharField(max_length=255, null=True, blank=True)
    

    class Meta:
        verbose_name = "Ember"
        verbose_name_plural = "Emberek"

    def __str__(self):
        return f'{self.teljesnev}, {self.becenev}, {self.szulinap}, {self.nevnap}, {self.ajandek}'

    def letrehozas_sor_alapjan(sor):
        sor = sor.strip()
        if not sor:
            return
        sor = sor.split(',')
        ember, is_created= Ember.objects.get_or_create(teljesnev = sor[0], becenev = sor[1], szulinap = sor[2], nevnap = sor[3], ajandek = sor[4])
        return ember
    

