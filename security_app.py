from time import sleep

from requests import post, get


def _check_choice(choice, pass_id):
    if choice == "Y":
        post("url/choice_yes", data=pass_id)
    elif choice == "N":
        post("url/choice_no", data=pass_id)
    else:
        print("Введите Y или N")
        _check_choice(choice, pass_id)


def main():
    res = get("url/check_passes")
    while not res:
        sleep(5)
        res = get("url/check_passes")
    pass_list = res.json()
    for _pass in pass_list:
        print(f"К вам пришёл {_pass["name"]}. Выдать пропуск?")
        choice = input()
        _check_choice(choice, _pass.pk)
    main()


if __name__ == "main":
    main()
