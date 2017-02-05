__author__ = 'Bertrand'
import random
from tournament.models import Coach,League, Match, TeamReport
from django.db.models import Q

def shuffled_query_set(query_set):
    seed = random.randint(1, 10000)
    return query_set.extra(select={'sort_key': 'RAND(%s)' % seed}).order_by('sort_key')


def draw_round_1():
    print ("===================================")
    print ("========== Tirage ronde 1 =========")
    print ("===================================")
    # tirage des rondes
    # si il s'agit de la ronde 1 :
    # pour chaque adversaire on tire un adversaire au sort sachant que :
    # - les têtes de séries ne peuvent pas se rencontrer à la ronde 1
    # - il faut que les têtes de série rencontrent un joueur qui n'est pas de leur ligue

    # algo :
    # - on fait un chapeau tête de série
    # - on fait un chapeau de ligue, chaque ligue contenant les joueurs de la ligue
    shuffled_head_coachs = shuffled_query_set(Coach.objects.filter(head = True))

    table = 1
    #un adversaire ne peut pas être choisi deux fois
    foe_list = []
    #une ligue ne peut pas être choisie deux fois
    chosen_league_list = []
    for head_coach in shuffled_head_coachs:

        chosen_league = get_random_league(chosen_league_list)

        # si on ne trouve pas de ligue eligible, ça veut dire qu'on a plus de tête de série que de ligue
        if chosen_league == None:
            print ("pas de ligue éligible pour affronter la tête de série" +head_coach.name)
            print (chosen_league_list)
            return

        # On ajoute la ligue choisie, afin qu'elle soit interdite à la prochaine itération
        chosen_league_list.append(chosen_league)

        # on trouve un adversaire pour la tête de série, qui appartient à la ligue, et qui n'a pas déjà été choisi
        foe = get_random_coach_of_league(foe_list,chosen_league)

        if foe == None:
            print ("pas de coach éligible dans la ligue "+chosen_league+"pour affronter la tête de série"+head_coach.name)
            return

        foe_list.append(foe)

        create_match(1,table,head_coach,foe)
        print("table "+repr(table)+" : "+head_coach.name+" Vs "+foe.name)


        table+=1

    for remaining_coach in Coach.objects.filter(head = False).filter(~Q(id__in=[f.id for f in foe_list])):

        if remaining_coach in foe_list:
            continue

        foe_list.append(remaining_coach)

        coach_foe = get_random_coach_not_of_league(remaining_coach.league,foe_list)

        # Si on ne trouve pas de coach qui respecte la contrainte inter ligue,
        if coach_foe is None:
            # on essaye d'en trouver un de la même ligue
            coach_foe = get_random_coach(foe_list)

            #si on en trouve pas non plus, alors c'est que tous les coachs sont pris, donc on sort
            if coach_foe is None:
                break

        #on ajoute les deux coachs à la liste des coach appariés
        foe_list.append(coach_foe)

        # on crée le match entre ces deux coachs

        create_match(1,table,remaining_coach,coach_foe)

        # on imprime la sortie
        print("table "+repr(table)+" : "+remaining_coach.name+" Vs "+coach_foe.name)

        table+=1

#
# ronde : le numéro de la ronde à tirer
#
def draw_next_round(ronde):

    print ("===================================")
    print ("====== Tirage ronde suivante ======")
    print ("===================================")
    #on choppe la liste des coachs, ordonnée par point
    coach_ranking = Coach.objects.all().order_by('-points')

    foe_list = []
    table = 1

    #pour chaque coach, on choppe le premier adversaire éligible,
    for coach in coach_ranking:

        #si le coach est dans la liste des coachs appariés, on continue
        if coach in foe_list:
            continue

        foe_list.append(coach)
        # celui qui à le nombre de point juste en dessous, qui n'est pas de la même ligue,
        # et qui n'est pas déjà apparié
        foe = Coach.objects.filter(points__lte=coach.points)\
                            .exclude(league=coach.league)\
                            .exclude(Q(id__in=[f.id for f in foe_list]))\
                            .order_by('-points','name').first()

        #si on en trouve pas, on prend deux joueurs de la même ligue
        if foe == None:
            foe = Coach.objects.filter(points__lte=coach.points)\
                            .exclude(Q(id__in=[f.id for f in foe_list]))\
                            .order_by('-points').first()

        #si on en trouve toujours pas, alors on sort
        if foe == None:
            break

        create_match(ronde=ronde,
                     table=table,
                     coach1=coach,
                     coach2=foe)

        #on stocke le coach ayant déjà joué
        foe_list.append(foe)

        # on imprime la sortie
        print("table "+repr(table)+" : "+coach.name+" Vs "+foe.name)
        table +=1

#
# Annulation de la ronde :
# On supprime les matchs et les rapports associés
#
def cancel_ronde(ronde_id):
    Match.objects.filter(ronde = ronde_id).delete()



#
# on renvoie au hasard une ligue qui n'est pas dans la liste interdite
#
def get_random_league(forbidden_League_list):

    eligible_league = League.objects.filter(~Q(id__in=[l.id for l in forbidden_League_list]))
    return shuffled_query_set(eligible_league).first()

#
# renvoi un coach, non tête de série qui appartient à la ligue spécifié et
# qui n'est pas dans la liste des coaches interdite
#
def get_random_coach_of_league(forbidden_coachs_list, target_league):

    eligible_coachs = Coach.objects.filter(head = False).filter(league = target_league).filter(~Q(id__in=[f.id for f in forbidden_coachs_list]))
    return shuffled_query_set(eligible_coachs).first()


#
# renvoi un coach, non tête de série qui n'appartient pas à la ligue spécifié et
# qui n'est pas dans la liste des coaches interdite
#
def get_random_coach_not_of_league(forbidden_league,forbidden_coach_list):
    eligible_coachs = Coach.objects.filter(head = False).filter(~Q(id__in=[f.id for f in forbidden_coach_list])).exclude(league = forbidden_league,)
    return shuffled_query_set(eligible_coachs).first()

#
# renvoi au hasard un coach qui n'appartient pas à la liste spécifiéé
#
def get_random_coach(forbidden_coach_list):
    eligible_coachs = Coach.objects.filter(head = False).filter(~Q(id__in=[f.id for f in forbidden_coach_list]))
    return shuffled_query_set(eligible_coachs).first()

def create_match(ronde,table,coach1,coach2):
        m = Match(ronde=ronde, table=table)
        m.save()
        tr1 = TeamReport(match=m,
                         coach=coach1)
        tr1.save()
        tr2 = TeamReport(match=m,
                         coach=coach2)
        tr2.save()
