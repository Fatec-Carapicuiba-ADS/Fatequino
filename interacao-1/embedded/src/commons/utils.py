class Utils():
    def get_week_day(day: str):
        WEEK_DAYS = {
            "1": "Domingo",
            "2": "Segunda",
            "3": "Terça",
            "4": "Quarta",
            "5": "Quinta",
            "6": "Sexta",
            "7": "Sábado"
        }
        return WEEK_DAYS[day]

    def remove_special_characters(text: str):
        replaced_text: str = text
        regex = "!@#$%¨&*()_-+={[}]:;?/\|"
        for x in regex:
            replaced_text = replaced_text.replace(x, '')
        return replaced_text

    def remove_accent(text: str):
        replaced_text = text
        remove_a = "áãàâ"
        remove_e = "èéê"
        remove_i = "íìî"
        remove_o = "òóôõ"
        remove_u = "úùû"
        remove_c = "ç"

        for x in remove_a:
            replaced_text = replaced_text.replace(x, 'a')

        for x in remove_e:
            replaced_text = replaced_text.replace(x, 'e')

        for x in remove_i:
            replaced_text = replaced_text.replace(x, 'i')

        for x in remove_o:
            replaced_text = replaced_text.replace(x, 'o')

        for x in remove_u:
            replaced_text = replaced_text.replace(x, 'u')

        for x in remove_c:
            replaced_text = replaced_text.replace(x, 'c')

        return replaced_text