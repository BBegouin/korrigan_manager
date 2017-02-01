__author__ = 'Bertrand'
import random
from tournament.models import Coach,League
from django.db.models import Q

def shuffled_query_set(query_set):
    seed = random.randint(1, 10000)
    return query_set.extra(select={'sort_key': 'RAND(%s)' % seed}).order_by('sort_key')

def draw_round_1():
    # tirage des rondes
    # si il s'agit de la ronde 1 :
    # pour chaque adversaire on tire un adversaire au sort sachant que :
    # - les têtes de séries ne peuvent pas se rencontrer à la ronde 1
    # - il faut que les têtes de série rencontrent un joueur qui n'est pas de leur ligue

    # algo :
    # - on fait un chapeau tête de série
    # - on fait un chapeau de ligue, chaque ligue contenant les joueurs de la ligue
    shuffled_head_coachs = shuffled_query_set(Coach.objects.filter(head = True))

    all_simple_coach = shuffled_query_set(Coach.objects.filter(head = False))

    table = 1
    #un adversaire ne peut pas être choisi deux fois
    foe_list = []
    #une ligue ne peut pas être choisie deux fois
    chosen_league_list = []
    for head_coach in shuffled_head_coachs:

        # la ligue du coach en cours est interdite
        chosen_league_list.append(head_coach.league)

        chosen_league = get_random_league(chosen_league_list)

        # On ajoute la ligue choisie, afin qu'elle soit interdite à la prochaine itération
        chosen_league_list.append(chosen_league)

        # on trouve un adversaire pour la tête de série, qui appartient à la ligue, et qui n'a pas déjà été choisi
        foe = get_random_coach_of_league(foe_list,chosen_league)

        foe_list.append(foe)

        print("table "+repr(table)+" : "+head_coach.name+" Vs "+foe.name)

        table+=1

    for remaining_coach in Coach.objects.filter(head = False).filter(~Q(id__in=[f.id for f in foe_list])):
        coach_foe = shuffled_query_set(Coach.objects.filter(head = False).filter(~Q(id__in=[f.id for f in foe_list])).exclude(league = remaining_coach.league,)).first()
        if coach_foe is None:
            break
        foe_list.append(coach_foe)
        foe_list.append(remaining_coach)
        print("table "+repr(table)+" : "+remaining_coach.name+" Vs "+coach_foe.name)
        table+=1


# on renvoie au hasard une ligue qui n'est pas dans la liste interdite
def get_random_league(forbidden_Leagues):

    eligible_league = League.objects.filter(~Q(id__in=[l.id for l in forbidden_Leagues]))
    return shuffled_query_set(eligible_league).first()

# renvoi un coach, non tête de série qui appartient à la ligue spécifié et
# qui n'est pas dans la liste des coaches interdite
def get_random_coach_of_league(forbidden_coaches, target_league):

    eligible_coaches = Coach.objects.filter(head = False).filter(league = target_league).filter(~Q(id__in=[f.id for f in forbidden_coaches]))
    return shuffled_query_set(eligible_coaches).first()
