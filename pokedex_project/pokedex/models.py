from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
 
class Favorite(models.Model):
    pokemon_id = models.IntegerField(unique=True)
    notes = models.TextField(blank=True, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Pokemon {self.pokemon_id}"