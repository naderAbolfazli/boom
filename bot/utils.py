def persian_alpha_sort(e):
    print(e, e[0])
    alphabet = "آابپتثجچحخدذرزژسشصضطظعغفقکكگلمنوهیي"
    return alphabet.index(e[0]) * 1000 + alphabet.index(e[1])


def persian_num_sort(e):
    numbers = "۱ ۲ ۳ ۴ ۵ ۶ ۷ ۸ ۹ ۱۰ ۱۱ ۱۲ ۱۳ ۱۴ ۱۵ ۱۶ ۱۷ ۱۸ ۱۹ ۲۰ ۲۱ ۲۲ ۲۳ ۲۴ ۲۵ ۲۶ ۲۷ ۲۸ ۲۹ ۳۰ ۳۱"
    return numbers.index(e[0:2])


def validate_national_code(national_code):
    if len(national_code) != 10:
        return False

    controller_digit = 0
    for i in range(0, 9):
        controller_digit += int(national_code[i]) * (10 - i)

    check_digit = controller_digit % 11
    if check_digit < 2 and national_code[9] == str(check_digit):
        return True
    elif check_digit >= 2 and int(national_code[9]) == (11 - check_digit):
        return True
    else:
        return False
