import machine
import utime
import sys

led = machine.Pin(25, machine.Pin.OUT)
rtc = machine.RTC()
rtc.datetime((2025, 5, 24, 6, 12, 0, 0, 0))  # Default time

led_state = False

def blink_led(times=1, duration=0.2):
    for _ in range(times):
        led.on()
        utime.sleep(duration)
        led.off()
        utime.sleep(duration)

def show_time():
    now = rtc.datetime()
    print("Current time: {:02d}:{:02d}:{:02d}".format(now[4], now[5], now[6]))

def set_rtc_from_command(parts):
    try:
        if len(parts) != 7:
            print("Usage: set_time YYYY MM DD HH MM SS")
            return
        year = int(parts[1])
        month = int(parts[2])
        day = int(parts[3])
        hour = int(parts[4])
        minute = int(parts[5])
        second = int(parts[6])
        rtc.datetime((year, month, day, 0, hour, minute, second, 0))
        print("RTC time set successfully.")
    except Exception as e:
        print("Error setting time:", e)

def print_main_menu():
    print("\n======== RaspberryTQ ========")
    print("Type one of the following commands:")
    print("1 or time           → Show current time")
    print("2 or blink N        → Blink LED N times")
    print("3 or shell          → Enter custom shell")
    print("4 or toggle         → Toggle LED ON/OFF")
    print("5 or set_time Y M D H M S")
    print("6 or exit           → Stop the program")
    print("=============================\n")

def custom_shell():
    print("Entering custom shell. Type 'exit' to return.")
    print("Available: help, time, led_on, led_off, blink, exit")

    while True:
        sys.stdout.write("cstuser@RaspberryTQ >>> ")
        cmd = sys.stdin.readline().strip().lower()
        if cmd == "exit":
            print("Exiting shell.")
            break
        elif cmd == "help":
            print("Commands: time, led_on, led_off, blink, exit")
        elif cmd == "time":
            show_time()
        elif cmd == "led_on":
            led.on()
            print("LED turned ON.")
        elif cmd == "led_off":
            led.off()
            print("LED turned OFF.")
        elif cmd == "blink":
            blink_led()
        else:
            print("Unknown command.")

def main():
    global led_state
    print_main_menu()
    while True:
        sys.stdout.write("RaspberryTQ> ")
        line = sys.stdin.readline().strip().lower()
        parts = line.split()

        if not parts:
            continue

        cmd = parts[0]

        if cmd == "1" or cmd == "time":
            show_time()
            blink_led(1)
        elif cmd == "2" or cmd == "blink":
            try:
                times = int(parts[1]) if len(parts) > 1 else 1
                blink_led(times)
            except:
                print("Usage: blink [times]")
        elif cmd == "3" or cmd == "shell":
            custom_shell()
        elif cmd == "4" or cmd == "toggle":
            led_state = not led_state
            led.value(led_state)
            print(f"LED is now {'ON' if led_state else 'OFF'}.")
        elif cmd == "5" or cmd == "set_time":
            set_rtc_from_command(parts)
        elif cmd == "6" or cmd == "exit":
            print("Exiting RaspberryTQ. Goodbye!")
            break
        else:
            print("Unknown command. Type again.")
            print_main_menu()

if __name__ == "__main__":
    main()
