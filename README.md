# RPi0_KeyPad_Client

## Description

Python Raspberry Pi keyboard project with associated menu with 4 modules.

Program can handle 4 push buttons as input devices to do operations with menu module. There is also cooperated TCP Socket Client module to send
specified data packets to TCP Socket Server.

---

## Overview

Project is working as a Linux systemd service *keypad_client.service*.
Service starts at runlevel 3 (multi-user mode) right after *lcd_socket.service* ([more about lcd_socket.service here...](https://github.com/Baro-coder/RPi0_LCD_Socket)) and listening for input from push buttons.

LED connected to RPi uses PWM Pin to signal with pulsing if the service is running.

---

### **Circuit plan**

Project is developed to work with the following circuit.

> ***TODO: Circuit plan image***

#### **Components**

- 4 x push buttons
- 1 x LED diode
- 1 x 100 Ohm resistor

All the pins can be freely modified as you want (except LED pin - it has to be PWM Pin). Pin numbers are specified in *config.ini*.

``` ini
# - KeyPad_Client: config.ini

[TCP Server]
host = 127.0.0.1
port = 7666
format = utf-8
buffer_size = 1024

[RPi KeyPad]
pin_button_next = 14
pin_button_prev = 15
pin_button_back = 18
pin_button_select = 17

[RPi LED]
pin_pwmled = 13
```

Check out that TCP Server address is assign to **localhost** at port **7666**.

---

### **Service**

To use project as a service you need main bash file. Remember to move the bash file outside of the project directory. In this case it is *keypad_client.sh*.

Service at start firstly updates to latest GitHub repository version, then starting.

``` bash
#!/bin/bash

# - keypad_client.sh


GITHUB_URL="https://github.com/Baro-coder/RPi0_KeyPad_Client"

APP_DIR="/home/pi/.Private/RPi0_KeyPad_Client"
MAIN_FILE="${APP_DIR}/main.py"

start(){
    if [[ -f $MAIN_FILE ]]; then
        echo "Starting the service..."
        sudo python $MAIN_FILE
        return 0
    else
        echo "$MAIN_FILE : The file does not exists!"
        return 1
    fi
}

update(){
    if [[ -d $APP_DIR ]]; then
            # App dir exists
            echo "Removing outdated source..."
            sudo rm -R ${APP_DIR}
    fi

    PARENT_DIR="${APP_DIR%/*}"

    cd $PARENT_DIR

    git clone $GITHUB_URL

    return $?
}



update

if [ $? -eq 0 ]; then
    start
    exit $?
else
    echo "Something went wrong during git cloning..."
    exit $?
fi
```

Next you need your *.service* file to copy to the */lib/systemd/system* directory.

``` service
[Unit]
Description=Raspberry Pi KeyPad TCP Client for LCD Display
After=lcd_socket.service
StartLimitIntervalSec=0

[Service]
ExecStart=/bin/bash /home/pi/.Private/keypad_client.sh
WorkingDirectory=/home/pi/.Private
StandardOutput=append:/var/log/keypad_client.log
StandardError=append:/var/log/keypad_client.log
Restart=always
RestartSec=1
User=pi

[Install]
WantedBy=multi-user.target
```

**Example copy command:**

``` code
sudo cp /path/to/keypad_client.service /lib/systemd/system/keypad_client.service
```

Logs from service will be stored in default logfiles for systemd in */var/log/* and additionally in specified filepaths.

> StandardOutput=append:/var/log/keypad_client.log
>  
> StandardError=append:/var/log/keypad_client.log

After that service should be available by *systemd*, and if you want to run service after every boot, just enable it with *systemctl* like:

``` code
sudo systemctl enable keypad_client.service
```

To start service type:

``` code
sudo systemctl start keypad_client.service
```
