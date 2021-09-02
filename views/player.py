from views.view import View


class CreatePlayer(View):

    def display_menu(self):

        name = input("""Nom du joueur:\n> """)

        first_name = input("""Prénom du joueur:\n> """)

        dob = self.get_user_entry(
            msg_display="Date de naissance (format DD-MM-YYYY):\n> ",
            msg_error="Veuillez entrer une date au format valide: DD-MM-YYYY\n> ",
            value_type="date"
        )

        sex = self.get_user_entry(
            msg_display="Sexe (H ou F):\n> ",
            msg_error="Veuillez entrer H ou F\n> ",
            value_type="selection",
            assertions=["H", "F"]
        )

        rank = self.get_user_entry(
            msg_display="Rang:\n> ",
            msg_error="Veuillez entrer une valeur numérique valide.\n> ",
            value_type="numeric"
        )

        print(f"Joueur {first_name} créé.")

        return {
            "name": name,
            "first_name": first_name,
            "dob": dob,
            "sex": sex,
            "rank": rank,
        }