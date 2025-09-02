from time import sleep

from requests import post, get


def main():
    name = input("Введите ваше ФИО: ")
    print("Выберите сотрудника к которому вы пришли:")
    res = get("url/get_users")
    users = res.json()
    for user in users:
        user_name = user["full_name"]
        print(f"{user["id"]}:\t{user_name}")
    worker_id = input()
    res = post("url/create_pass", data={"name": name, "id": worker_id})

    if res.status_code == 200:
        print("Ожидайте подтвеждения от сотрудника")
        res = get("url/check_pass_status", params=("id", worker_id))
        while res.json == {"status": "WAIT"}:
            sleep(5)
            res = get("url/check_pass_status", params=("id", worker_id))
    else:
        print("В пропуске отказано")

    main()

if __name__ == "main":
    main()
