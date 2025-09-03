from time import sleep

from requests import post, get


def _check_choice(choice, pass_id):
    while True:
        if choice == "Y":
            post("http://localhost:8000/choice_yes/", data={"id": pass_id})
            break
        elif choice == "N":
            post("http://localhost:8000/choice_no/", data={"id": pass_id})
            break
        else:
            print("Введите Y или N")
            choice = input()


def main():
    res = get("http://localhost:8000/check_passes/")
    while not res:
        sleep(5)
        res = get("http://localhost:8000/check_passes/")
    pass_list = res.json()
    for _pass in pass_list:
        choice = input(f"К вам пришёл {_pass["name"]}. Выдать пропуск? (Y/N): ")
        _check_choice(choice, _pass["id"])
    main()


if __name__ == "__main__":
    main()
