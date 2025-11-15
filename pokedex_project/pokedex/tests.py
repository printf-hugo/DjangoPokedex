import json
from django.test import TestCase
from django.urls import reverse
from .models import Favorite, Tag

class PokedexAPITests(TestCase):

    def setUp(self):
        self.tag1 = Tag.objects.create(name='Competitivo')
        self.tag2 = Tag.objects.create(name='Shiny Hunt')
        self.favorite1 = Favorite.objects.create(pokemon_id=25, tag=self.tag1)

    def test_model_creation(self):
        self.assertEqual(self.favorite1.pokemon_id, 25)
        self.assertEqual(self.favorite1.tag, self.tag1)
        self.assertEqual(str(self.favorite1.tag), 'Competitivo')

    def test_create_favorite_api(self):
        url = reverse('api_favorites')
        data = {'pokemon_id': 149}
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(pokemon_id=149).exists())

    def test_update_favorite_api_change_tag(self):
        url = reverse('api_favorite_detail', kwargs={'favorite_id': self.favorite1.pk})
        data = {'notes': 'Nota de teste', 'tag_id': self.tag2.id}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        self.favorite1.refresh_from_db()
        self.assertEqual(self.favorite1.notes, 'Nota de teste')
        self.assertEqual(self.favorite1.tag, self.tag2)

    def test_update_favorite_api_remove_tag(self):
        url = reverse('api_favorite_detail', kwargs={'favorite_id': self.favorite1.pk})
        data = {'tag_id': ''}
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.favorite1.refresh_from_db()
        self.assertIsNone(self.favorite1.tag)

    def test_delete_favorite_api(self):
        url = reverse('api_favorite_detail', kwargs={'favorite_id': self.favorite1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Favorite.objects.filter(pk=self.favorite1.pk).exists())
