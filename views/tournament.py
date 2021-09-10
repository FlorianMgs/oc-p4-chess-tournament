from views.view import View
from controller.timestamp import get_timestamp
from controller.database import load_db


class CreateTournament(View):

    def display_menu(self):

        date = get_timestamp()
        print(date + " : Nouveau tournoi")

        name = input("""Nom du tournoi:\n> """)

        place = self.get_user_entry(
            msg_display="Lieu:\n> ",
            msg_error="Veuillez entrer un lieu valide",
            value_type="string"
        )

        user_selection_time_control = self.get_user_entry(
            msg_display="Contrôle de temps:\n0 - Bullet\n1 - Blitz\n2 - Coup Rapide\n> ",
            msg_error="Veuillez entrer 0, 1 ou 2.",
            value_type="selection",
            assertions=["0", "1", "2"]
        )
        if user_selection_time_control == "0":
            time_control = "Bullet"
        elif user_selection_time_control == "1":
            time_control = "Blitz"
        else:
            time_control = "Coup Rapide"

        nb_players = self.get_user_entry(
            msg_display="Nombre de joueurs:\n> ",
            msg_error="Veuillez entrer un nombre entier supérieur ou égal à 2.",
            value_type="num_superior",
            default_value=2
        )

        nb_rounds = self.get_user_entry(
            msg_display="Nombre de tours (4 par défaut):\n> ",
            msg_error="Veuillez entrer 4 ou plus.",
            value_type="num_superior",
            default_value=4
        )
        desc = input("Description du tournoi:\n> ")

        return {
            "name": name,
            "place": place,
            "date": date,
            "time_control": time_control,
            "nb_players": nb_players,
            "nb_rounds": nb_rounds,
            "desc": desc
        }


class LoadTournament(View):

    def display_menu(self):

        all_tournaments = load_db("tournaments")
        if all_tournaments:

            builded_selection = self.build_selection(iterable=all_tournaments,
                                                     display_msg="Choisir un tournoi:\n",
                                                     assertions=[])

            user_input = int(self.get_user_entry(
                msg_display=builded_selection['msg'] + "\n> ",
                msg_error="Veuillez entrer un nombre entier.",
                value_type="selection",
                assertions=builded_selection['assertions']
            ))
            serialized_loaded_tournament = all_tournaments[user_input-1]

            return serialized_loaded_tournament

        else:
            return False
