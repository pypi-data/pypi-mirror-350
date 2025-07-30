import time
from multiprocessing import Process, Queue
import asyncio
import sys
import serial
import glob

DEVICE_UPDATE_TIME = 15
LAST_DEVICE_UPDATE = 0


def available_serial_ports():
    """Lists serial port names

    Raises:
        EnvironmentError: On unsupported or unknown platforms.
        RuntimeError: If no serial ports are found.

    Returns:
        A list of available serial ports on the system.
    """
    if sys.platform.startswith("win"):
        ports = [f"COM{port_number + 1}" for port_number in range(256)]
    elif sys.platform.startswith(("linux", "cygwin")):
        # This excludes the current terminal "/dev/tty"
        ports = glob.glob("/dev/tty[A-Za-z]*")
    elif sys.platform.startswith("darwin"):
        ports = glob.glob("/dev/tty.*")
    else:
        raise EnvironmentError("Unsupported platform")

    available_ports = []
    for port in ports:
        try:
            with serial.Serial(port):
                available_ports.append(port)
        except (OSError, serial.SerialException):
            continue

    return available_ports


def multiprocessing_available_serial_ports(queue):
    available_ports = available_serial_ports()
    queue.put(available_ports)
    return available_ports


async def list_available_ports(max_index=10):
    """
    List the indices of all available video capture devices.

    Parameters:
    - max_index: Maximum device index to check. Increase if you have more devices.

    Returns:
    - List of integers, where each integer is an index of an available device.
    """
    global AVAILABLE_DEVICES, LAST_DEVICE_UPDATE
    if time.time() - LAST_DEVICE_UPDATE > DEVICE_UPDATE_TIME:
        LAST_DEVICE_UPDATE = time.time()
        print(f"Checking for available devices up to index {max_index}.")

        queue = Queue()
        proc = Process(target=multiprocessing_available_serial_ports, args=(queue,))
        proc.start()
        while proc.is_alive():
            await asyncio.sleep(0.1)
        proc.join()
        # check if the process ended with an error
        res = None
        if proc.exitcode != 0:
            return AVAILABLE_DEVICES
        res = queue.get()

        AVAILABLE_DEVICES = res
    return AVAILABLE_DEVICES
