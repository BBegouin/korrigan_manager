from django.test import TestCase

# Create your tests here.

from django.test import TestCase
from tournament.models import Coach,League
from tournament.core.drawer import draw_round_1

class TestDraw(TestCase):

    def test_draw_round_1(self):
        draw_round_1
