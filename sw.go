package main

import (
    "bufio"
    "fmt"
    "log"
    "os"
    "strings"

    "github.com/reiver/go-telnet"
)

func main() {
    // Адрес коммутатора
    addr := "192.168.1.1:23"

    // Имя пользователя и пароль
    username := "admin"
    password := "password"

    // Подключаемся к коммутатору
    conn, err := telnet.Dial("tcp", addr)
    if err != nil {
        log.Fatal(err)
    }
    defer conn.Close()

    // Читаем приветственное сообщение
    reader := bufio.NewReader(conn)
    msg, err := reader.ReadString('\n')
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(msg)

    // Вводим имя пользователя
    _, err = conn.Write([]byte(username + "\n"))
    if err != nil {
        log.Fatal(err)
    }

    // Читаем сообщение о пароле
    msg, err = reader.ReadString('\n')
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(msg)

    // Вводим пароль
    _, err = conn.Write([]byte(password + "\n"))
    if err != nil {
        log.Fatal(err)
    }

    // Читаем сообщение после авторизации
    msg, err = reader.ReadString('\n')
    if err != nil {
        log.Fatal(err)
    }
    fmt.Println(msg)

    // Выполняем команду show running-config
    cmd := "show running-config\n"
    _, err = conn.Write([]byte(cmd))
    if err != nil {
        log.Fatal(err)
    }

    // Создаем файл для записи конфигурации
    file, err := os.Create("config.txt")
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

    // Читаем результат команды и записываем в файл
    for {
        msg, err = reader.ReadString('\n')
        if err != nil {
            log.Fatal(err)
        }
        if strings.Contains(msg, "--More--") {
            // Если появляется "--More--", то отправляем пробел для продолжения вывода
            _, err = conn.Write([]byte(" "))
            if err != nil {
                log.Fatal(err)
            }
        } else if strings.Contains(msg, "end") {
            // Если появляется "end", то завершаем чтение конфигурации
            break
        }
        _, err = file.WriteString(msg)
        if err != nil {
            log.Fatal(err)
        }
    }

    fmt.Println("Конфигурация сохранена в файле config.txt")

    // Выходим из коммутатора
    cmd = "exit\n"
    _, err = conn.Write([]byte(cmd))
    if err != nil {
        log.Fatal(err)
    }
}
