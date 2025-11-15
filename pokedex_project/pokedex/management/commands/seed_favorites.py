# pokedex/management/commands/seed_favorites.py

import random
from django.core.management.base import BaseCommand
from django.db import transaction
from pokedex.models import Favorite, Tag

class Command(BaseCommand):
    help = 'Limpa e popula o banco de dados com Pokémon favoritos e uma única tag.'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write('Limpando dados antigos...')
        Favorite.objects.all().delete()
        Tag.objects.all().delete()

        self.stdout.write('Criando tags pré-definidas...')
        tag_names = ['Competitivo', 'Shiny Hunt', 'Time Principal', 'Para Evoluir']
        tags = [Tag.objects.create(name=name) for name in tag_names]
        
        self.stdout.write('Adicionando 25 Pokémon favoritos e atribuindo uma tag...')
        for i in range(1, 26):
            # Adiciona uma chance de não ter tag (None)
            possible_tags = tags + [None] 
            random_tag = random.choice(possible_tags)
            
            favorite = Favorite.objects.create(
                pokemon_id=i,
                tag=random_tag
            )
            tag_name = f'com a tag: "{random_tag.name}"' if random_tag else 'sem tag.'
            self.stdout.write(self.style.SUCCESS(f' -> Pokémon #{i} adicionado {tag_name}'))

        self.stdout.write(self.style.SUCCESS('Seeding concluído!'))
