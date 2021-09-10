

class View:

    def get_user_entry(self, msg_display, msg_error, value_type, assertions=None, default_value=None):
        while True:
            value = input(msg_display)
            if value_type == "numeric":
                if value.isnumeric():
                    value = int(value)
                    return value
                else:
                    print(msg_error)
                    continue
            if value_type == "num_superior":
                if value.isnumeric():
                    value = int(value)
                    if value >= default_value:
                        return value
                    else:
                        print(msg_error)
                        continue
                else:
                    print(msg_error)
                    continue
            if value_type == "string":
                try:
                    float(value)
                    print(msg_error)
                    continue
                except ValueError:
                    return value
            elif value_type == "date":
                if self.verify_date(value):
                    return value
                else:
                    print(msg_error)
                    continue
            elif value_type == "selection":
                if value in assertions:
                    return value
                else:
                    print(msg_error)
                    continue

    @staticmethod
    def verify_date(value_to_test):
        if "-" not in value_to_test:
            return False
        else:
            splitted_date = value_to_test.split("-")
            for date in splitted_date:
                if not date.isnumeric():
                    return False
            return True

    @staticmethod
    def build_selection(iterable: list, display_msg: str, assertions: list) -> dict:
        display_msg = display_msg
        assertions = assertions

        for i, data in enumerate(iterable):
            display_msg = display_msg + f"{i+1} - {data['name']}\n"
            assertions.append(str(i + 1))

        return {
            "msg": display_msg,
            "assertions": assertions
            }
