import socket

def save_switch_configuration(ip_address, port, username, password, output_file):
    try:
        # Создаем сокет
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Устанавливаем соединение
            s.connect((ip_address, port))
            print(f"Подключение к {ip_address}:{port} успешно.")

            # Авторизация
            s.sendall(b"username " + username.encode('ascii') + b"\n")
            print("Отправлен логин.")
            s.recv(1024)  # Получаем ответ от коммутатора

            s.sendall(b"password " + password.encode('ascii') + b"\n")
            print("Отправлен пароль.")
            s.recv(1024)  # Получаем ответ от коммутатора

            # Отправляем команду для получения конфигурации
            s.sendall(b"show running-config\n")
            print("Команда отправлена.")

            # Получаем данные
            data = b""
            while True:
                part = s.recv(4096)
                if not part:
                    break
                data += part

            # Декодируем данные в ASCII
            configuration = data.decode('ascii', errors='ignore')

            # Сохраняем конфигурацию в файл
            with open(output_file, 'w', encoding='ascii') as f:
                f.write(configuration)
            print(f"Конфигурация сохранена в {output_file}.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Пример использования
save_switch_configuration('192.168.1.1', 23, 'my_username', 'my_password', 'switch_config.txt')
