from keyboard import wait, send, write
from time import sleep

button = input("Выберите кнопку при нажатии на которую вы будете выходить в хаб: ")
time = int(input("Выберите задержку: 1 - 0.1с, 2 - 0.3с, 3 - 0.7с, 4 - 1с, 5 - 3с\nЗадержка: "))

if time == 1:
    timee = 0.1
elif time == 2:
    timee = 0.3
elif time == 3:
    timee = 0.7
elif time == 4:
    timee = 1
else:
    timee = 3

while True:
    wait(button)
    send("t")
    sleep(timee)
    write("/hub")
    sleep(timee)
    send("Enter")