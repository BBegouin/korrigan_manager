__author__ = 'Bertrand'


from django.test import TestCase
from django.contrib.auth.models import User
from tournament.models import Coach,Match,TeamReport


mr_root="/match_report/"
mr_publish_root="/match_report/%i/publish/"

"""
On teste :
- la création d'un rapport de match
- la création des rapports d'équipes liés
"""
class TestAdminIndex(TestCase):


    """
        Test d'affichage de l'admin
    """
    def test_admin_index_no_round(self):

        self.client.login(username='bagouze', password='bagouze')
        response = self.client.get('/admin/')
        self.assertEqual(response.status_code,200)

