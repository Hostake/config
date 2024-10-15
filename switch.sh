#!/bin/bash

AUTO_SEND=0  # 0 - авто отправка выключена, 1 - включена

# Функция для отправки конфигурации

send_config_to_tftp() {

  local SWITCH_IP="$1"

  local TFTP_SERVER="$2"

  local CONFIG_FILE="$3"

  {

    sleep 1

    echo "configure terminal"

    sleep 1

    echo "copy running-config tftp:"

    sleep 1

    echo "$TFTP_SERVER"

    sleep 1

    echo "$CONFIG_FILE"

    sleep 1

    echo "exit"

    sleep 1

  } | telnet "$SWITCH_IP"

  echo "Конфигурация отправлена на TFTP сервер."

}

# Функция для выбора режима отправки

choose_mode() {

  read -p "Вы хотите включить авто отправку? (y/n): " response

  if [[ "$response" == "y" ]]; then

    AUTO_SEND=1

  fi

}

# Чтение адресов коммутаторов из файла

while IFS= read -r line; do

  SWITCH_IP=$(echo "$line" | cut -d' ' -f1)

  TFTP_SERVER=$(echo "$line" | cut -d' ' -f2)

  CONFIG_FILE=$(echo "$line" | cut -d' ' -f3)

  if (( AUTO_SEND )); then

    send_config_to_tftp "$SWITCH_IP" "$TFTP_SERVER" "$CONFIG_FILE"

  else

    read -p "Отправить конфигурацию для $SWITCH_IP? (y/n): " send_now

    if [[ "$send_now" == "y" ]]; then

      send_config_to_tftp "$SWITCH_IP" "$TFTP_SERVER" "$CONFIG_FILE"

    fi

  fi

done < "config_addresses.txt"

choose_mode  # Выбор режима перед началом отправки
