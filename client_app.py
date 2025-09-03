from time import sleep

from requests import post, get


def _check_security(pass_id):
    res = get(f"http://localhost:8000/check_security_approval/?id={pass_id}")
    while res.status_code == 200:
        sleep(5)
        res = get(f"http://localhost:8000/check_security_approval/?id={pass_id}")
    if res.status_code == 201:
        print("Подтверждение от охраны получено")
    else:
        print("В пропуске отказано")
    return


def _check_worker(pass_id):
    res = get(f"http://localhost:8000/check_worker_approval/?id={pass_id}")
    while res.status_code == 200:
        sleep(5)
        res = get(f"http://localhost:8000/check_worker_approval/?id={pass_id}")
    if res.status_code == 201:
        print("Подтверждение от сотрудника получено")
        _check_security(pass_id)
    else:
        print("В пропуске отказано")
        return


def main():
    name = input("Введите ваше ФИО: ")
    print("Выберите сотрудника к которому вы пришли:")
    res = get("http://localhost:8000/get_users/")
    users = res.json()
    for user in users:
        user_name = user["full_name"]
        print(f"{user["id"]}\t{user_name}")
    worker_id = input()
    print("Ожидайте подтверждения от сотрудника")
    res = post("http://localhost:8000/create_pass/", data={"name": name, "worker": worker_id})

    if res.status_code == 201:
        data = res.json()
        _check_worker(data["id"])
    else:
        print("В пропуске отказано")

    main()

if __name__ == "__main__":
    main()
