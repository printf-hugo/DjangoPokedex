import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from .models import Favorite, Tag

def index(request):

    all_tags = list(Tag.objects.values('id', 'name'))
    context = {
        'all_tags_json': json.dumps(all_tags)
    }
    return render(request, 'pokedex/index.html', context)

def favorites_view(request):

    favorites = Favorite.objects.select_related('tag').all().order_by('pokemon_id')
    all_tags = list(Tag.objects.values('id', 'name'))

    favorites_data = []
    for fav in favorites:
        tag_data = {'id': fav.tag.id, 'name': fav.tag.name} if fav.tag else None
        
        favorites_data.append({
            'pk': fav.pk,
            'pokemon_id': fav.pokemon_id,
            'notes': fav.notes,
            'tag': tag_data 
        })
        
    context = {
        'favorites_json': json.dumps(favorites_data),
        'all_tags_json': json.dumps(all_tags) 
    }
    return render(request, 'pokedex/favorites.html', context)

@csrf_exempt
@require_http_methods(["POST"])
def api_favorites(request):

    try:
        data = json.loads(request.body)
        pokemon_id = data.get('pokemon_id')
        
        if not pokemon_id:
            return JsonResponse({'error': 'Pokemon ID é obrigatório'}, status=400)

        favorite, created = Favorite.objects.get_or_create(pokemon_id=pokemon_id)
        
        if created:
            return JsonResponse({'status': 'ok', 'message': f'Pokémon #{pokemon_id} adicionado aos favoritos!', 'favorite_id': favorite.pk})
        else:
            return JsonResponse({'status': 'exists', 'message': f'Pokémon #{pokemon_id} já está nos favoritos.'})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'JSON inválido'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT", "DELETE"])
@transaction.atomic
def api_favorite_detail(request, favorite_id):

    try:
        favorite = Favorite.objects.get(pk=favorite_id)
    except Favorite.DoesNotExist:
        return JsonResponse({'error': 'Favorito não encontrado'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)
        
        favorite.notes = data.get('notes', favorite.notes)
        
        tag_id = data.get('tag_id')

        if tag_id:
            try:
                tag = Tag.objects.get(pk=tag_id)
                favorite.tag = tag
            except Tag.DoesNotExist:
                favorite.tag = None
        else:
            favorite.tag = None
        
        favorite.save()
        return JsonResponse({'status': 'ok', 'message': 'Favorito atualizado com sucesso!'})

    elif request.method == 'DELETE':
        favorite.delete()
        return JsonResponse({'status': 'ok'}, status=200)
