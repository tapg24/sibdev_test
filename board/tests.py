from django.test import TestCase
from django.utils import timezone

from .models import Ad


class AdModelTests(TestCase):

    def test_was_create_ad(self):
        title = 'title'
        ad_text = 'description'
        created_at = timezone.now()
        ad = Ad(title=title, ad_text=ad_text, created_at=created_at)
        self.assertEqual(ad.title, title, 'title is not equal')
        self.assertEqual(ad.ad_text, ad_text, 'ad_text is not equal')
        self.assertEqual(ad.created_at, created_at, 'created_at is not equal')
