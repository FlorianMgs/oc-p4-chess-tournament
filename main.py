from views.view import View
from controller.tournament_controller import create_tournament, play_tournament
from controller.player_controller import update_rankings

menu = View()

if __name__ == "__main__":

    # menu principal: on créer le tournoi
    print()
    user_input = menu.get_user_entry(
        msg_display="Que faire ?\n0 - Créer un tournoi\nq - Quitter\n> ",
        msg_error="Veuillez entrer une valeur valide\n> ",
        value_type="selection",
        assertions=["0", "q"]
    )

    if user_input == "0":
        tournament = create_tournament()
    else:
        quit()

    # on joue le tournoi
    print()
    user_input = menu.get_user_entry(
        msg_display="Que faire ?\n0 - Jouer le tournoi\nq - Quitter\n> ",
        msg_error="Veuillez entrer une valeur valide\n> ",
        value_type="selection",
        assertions=["0", "q"]
    )

    # on récupère les résultats une fois le tournoi terminé
    if user_input == "0":
        rankings = play_tournament(tournament)
    else:
        quit()

    # on affiche les résultats
    print()
    print(f"Tournoi {tournament.name} terminé !\nRésultats:")
    for i, player in enumerate(rankings):
        print(f"{str(i + 1)} - {player}")

    # on met à jour les classements
    print()
    user_input = menu.get_user_entry(
        msg_display="Mise à jour des classements\n0 - Automatiquement\n1 - Manuellement\nq - Quitter\n> ",
        msg_error="Veuillez entrer une valeur valide\n> ",
        value_type="selection",
        assertions=["0", "1", "q"]
    )
    if user_input == "0":
        for i, player in enumerate(rankings):
            update_rankings(player, i+1)

    elif user_input == "1":
        for player in rankings:
            rank = menu.get_user_entry(
                msg_display=f"Rang de {player}:\n> ",
                msg_error="Veuillez entrer un nombre entier.",
                value_type="numeric"
            )
            update_rankings(player, rank)

    else:
        quit()
