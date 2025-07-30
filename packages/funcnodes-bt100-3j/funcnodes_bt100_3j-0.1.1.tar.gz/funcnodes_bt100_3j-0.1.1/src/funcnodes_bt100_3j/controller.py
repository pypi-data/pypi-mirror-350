import serial
import asyncio
import contextlib
import queue
import time

from .ports import list_available_ports


async def event_wait(evt, timeout):
    # suppress TimeoutError because we'll return False in case of timeout
    with contextlib.suppress(asyncio.TimeoutError):
        await asyncio.wait_for(evt.wait(), timeout)
    return evt.is_set()


class BT100_3J:
    COUNTERCLOCKWISE = 0x00
    CLOCKWISE = 0x01
    START = 0x01
    STOP = 0x00
    W = 0x57  # noqa: E741
    J = 0x4A  # noqa: E741
    R = 0x52  # noqa: E741
    I = 0x49  # noqa: E741
    D = 0x44  # noqa: E741

    def __init__(self):
        self._port = None
        self._ser = None
        self.readThread = None
        self.writeThread = None
        self.writeQueue = queue.Queue()
        self._connected = False
        self.start_flag = b"\xe9"
        self.stop_pdu = b"\xe9\x1f\x06\x57\x4a\x01\xf4\x10\x01\xe0"
        self.Pump_ID = b"\x01"  # Assuming Pump ID is intended to be in bytes

        self._local_state = {"rpm": 1, "state": self.STOP, "dir": self.CLOCKWISE}
        self._remote_state = {"rpm": None, "state": None, "dir": None}

        self._op_lock = asyncio.Lock()
        self._stop_evt = asyncio.Event()
        self._op_counter = 0

    async def autoconnect(self):
        print("autoconnect")
        ports = await list_available_ports()
        for port in ports:
            print("trying", port)
            try:
                await self.connect(port)
                self._port = port
                print("connected to", port)
                return
            except TimeoutError:
                print("failed due to timeout")
                pass
        raise RuntimeError("No BT100-3J pump found")

    async def connect(self, port=None):
        await self.disconnect()
        if port is None:
            port = self._port
        if port is None:
            return await self.autoconnect()

        self._port = port
        self._ser = serial.Serial(
            port,
            1200,
            timeout=1,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_EVEN,
            stopbits=serial.STOPBITS_ONE,
        )
        self.writeThread = asyncio.create_task(self._write_loop())
        self.readThread = asyncio.create_task(self._read_loop())
        self._connected = True

        await self._get_pump_state(time_out=1)
        for k, v in self._remote_state.items():
            self._local_state[k] = v
        print("connected")

    @property
    def rpm(self) -> int:
        return self._local_state["rpm"] / 10

    @property
    def connected(self) -> bool:
        return self._connected

    @property
    def state(self) -> int:
        return self._local_state["state"]

    @property
    def dir(self) -> int:
        return self._local_state["dir"]

    async def disconnect(self, timeout=0.5):
        # wait for the write queue to empty before closing the port to avoid data loss
        # max wait time is timeout seconds
        start_time = time.time()
        while not self.writeQueue.empty() and time.time() - start_time < timeout:
            await asyncio.sleep(0.01)

        self._connected = False
        if self._ser:
            self._ser.close()
        if self.readThread is not None:
            try:
                await asyncio.wait_for(self.readThread, timeout)
            except asyncio.TimeoutError:
                pass

        if self.writeThread is not None:
            try:
                await asyncio.wait_for(self.writeThread, timeout)
            except asyncio.TimeoutError:
                pass

    async def _write_loop(self):
        while self._connected:
            if not self.writeQueue.empty():
                senddata = self.writeQueue.get()
                print(">>", senddata)
                self._ser.write(senddata)
                self.writeQueue.task_done()
                await asyncio.sleep(0.05)
            else:
                await asyncio.sleep(0.1)

    def _process_message(self, message: bytes) -> bool:
        if len(message) < 3:
            return False

        # address = message[0]
        length = original_length = message[1]
        if len(message) < length + 3:
            return False
        # print("<<", message)
        # extend length if there are escape sequences
        i = 0
        while i < length:
            c = message[2 + i]
            if c == 0xE8:
                length += 1
            i += 1

        pdu = message[2 : 2 + length]

        fsc = message[-1]
        xor_value = 0
        for byte in message[: 2 + length]:
            xor_value ^= byte
        if fsc != xor_value:
            return False
        pdu = self.unescape_special_bytes(pdu)

        handled = False
        if pdu[0] == self.R:
            if pdu[1] == self.J:
                if original_length == 0x06:
                    # state response
                    self._remote_state["rpm"] = int.from_bytes(
                        pdu[2:4], byteorder="big"
                    )
                    self._remote_state["state"] = pdu[4]
                    self._remote_state["dir"] = pdu[5]
                    handled = True
        elif pdu[0] == self.W:
            if pdu[1] == self.J:
                if original_length == 0x02:
                    handled = True  # message received response
        if not handled:
            print("unhandled message", message)
        return handled

    async def _read_loop(self):
        message = b""
        while self._connected:
            if self._ser.in_waiting:
                message += self._ser.read(self._ser.in_waiting)
                # split the message into individual messages and process them
                messages = message.split(self.start_flag)[1:]
                print("<<", messages)
                if messages:
                    if len(messages) > 1:
                        for message in messages[:-1]:
                            self._process_message(message)
                    if self._process_message(messages[-1]):
                        message = b""
                    else:
                        message = self.start_flag + messages[-1]

            else:
                await asyncio.sleep(0.01)

    async def send(self, pdu: bytes):
        self.writeQueue.put(pdu)

    def unescape_special_bytes(self, pdu: bytes) -> bytes:
        unescaped_pdu = b""
        i = 0
        while i < len(pdu):
            # Check for special byte sequences and ensure not to go out of bounds
            if i + 1 < len(pdu) and pdu[i] == 0xE8 and pdu[i + 1] == 0x00:
                unescaped_pdu += b"\xe8"
                i += 2  # Skip the next byte in the escape sequence
            elif i + 1 < len(pdu) and pdu[i] == 0xE8 and pdu[i + 1] == 0x01:
                unescaped_pdu += b"\xe9"
                i += 2  # Skip the next byte in the escape sequence
            else:
                unescaped_pdu += pdu[
                    i : i + 1
                ]  # Use slicing to avoid needing to convert byte to bytes
                i += 1
        return unescaped_pdu

    def escape_special_bytes(self, pdu: bytes):
        # replaces 0xE8 with 0xE8 0x00 and 0xE9 with 0xE9 0x01 in the PDU

        escaped_pdu = b""
        for byte in pdu:
            if byte == 0xE8:
                escaped_pdu += b"\xe8\x00"
            elif byte == 0xE9:
                escaped_pdu += b"\xe8\x01"
            else:
                escaped_pdu += bytes([byte])

        return escaped_pdu

    def make_message(self, pdu: bytes):
        pdu_length = len(pdu)
        pdu = self.escape_special_bytes(pdu)
        pdu_length_byte = pdu_length.to_bytes(1, byteorder="big")

        pre_pdu = self.Pump_ID + pdu_length_byte + pdu
        xor_value = 0
        for byte in pre_pdu:
            xor_value ^= byte
        fcs = xor_value.to_bytes(1, byteorder="big")

        return self.start_flag + pre_pdu + fcs

    async def _send_pump_state(self):
        if not self._connected:
            await self.connect(self._port)

        if self._local_state["state"] == self.STOP:
            self._stop_evt.set()

        pdu = bytes([self.W, self.J])
        pdu += self._local_state["rpm"].to_bytes(2, byteorder="big")
        pdu += bytes([self._local_state["state"], self._local_state["dir"]])
        message = self.make_message(pdu)
        await self.send(message)

    async def _get_pump_state(self, time_out=9999):
        self._remote_state = {"rpm": None, "state": None, "dir": None}
        t = time.time()
        while time.time() - t < time_out:
            if all([v is not None for v in self._remote_state.values()]):
                break

            pdu = bytes([self.R, self.J])
            message = self.make_message(pdu)

            await self.send(message)

            for i in range(5):
                await asyncio.sleep(0.1)
                if all([v is not None for v in self._remote_state.values()]):
                    break

        if any([v is None for v in self._remote_state.values()]):
            raise TimeoutError("Failed to get pump state", self._remote_state)

    async def set_state(
        self, rpm: float = None, state: int = None, dir: int = None, time_out=5
    ):
        if rpm is not None:
            int_rpm = max(1, min(int(rpm * 10), 1000))
            self._local_state["rpm"] = int_rpm
        if state is not None:
            self._local_state["state"] = state
        if dir is not None:
            self._local_state["dir"] = dir

        target_state = self._local_state.copy()
        print(
            "setting state to",
            target_state,
        )
        # print("target_state", target_state)
        # print("remote_state", self._remote_state)
        # print("eq", target_state == self._remote_state)
        start_time = time.time()
        while self._remote_state != target_state:
            print("setting state", target_state, "remote_state", self._remote_state)
            for k, v in target_state.items():
                self._local_state[k] = v
            # print("target_state", target_state)
            # print("remote_state", self._remote_state)
            await self._send_pump_state()
            await asyncio.sleep(0.3)
            await self._get_pump_state(time_out=time_out)

            if time.time() - start_time > time_out:
                raise TimeoutError("Failed to set pump state")
        print("setting state to", target_state, "took", time.time() - start_time, "s")
        await asyncio.sleep(0.1)

    async def set_dir(self, dir: int):
        await self.set_state(dir=dir)

    async def set_rpm(self, rpm: float):
        await self.set_state(rpm=rpm)

    async def start(self):
        await self.set_state(state=self.START)

    async def stop(self):
        await self.set_state(state=self.STOP)
        self._stop_evt.set()

    async def ramp_to_rpm(self, rpm: float, ramp_time: float):
        start_time = time.time()
        end_time = start_time + ramp_time
        remaining_time = ramp_time
        remaining_rpm = rpm - self._local_state["rpm"] / 10
        print("remaining_rpm", remaining_rpm)
        d = []
        d.append([remaining_time, remaining_rpm])
        # estimate a single set takes 0.5s
        while self._local_state["rpm"] / 10 != rpm:
            steps = remaining_time / 0.5
            rpm_step = remaining_rpm / steps
            new_rpm = self._local_state["rpm"] / 10 + rpm_step
            print("ramping to", new_rpm)
            try:
                await self.set_rpm(new_rpm)
            except TimeoutError:
                pass
            remaining_time = end_time - time.time()
            remaining_rpm = rpm - self._local_state["rpm"] / 10
            d.append([remaining_time, remaining_rpm])
        print(d)

    async def pump_for(
        self, seconds: float, rpm: float = None, dir: int = None, cb=None
    ) -> bool:
        if rpm is None:
            rpm = self.rpm
        if dir is None:
            dir = self.dir

        async with self._op_lock:
            self._stop_evt.set()
            await asyncio.sleep(0.1)
            self._stop_evt.clear()

        t = time.time()
        if cb is not None:
            cb(0)
        await self.set_state(rpm=rpm, state=self.START, dir=dir)
        seconds = max(0, seconds - (time.time() - t))

        # sleep for time or till stop_evt is set
        print("pumping for", seconds)
        if not await event_wait(self._stop_evt, seconds):
            await self.stop()
        if cb is not None:
            cb(1)

        return True

    def __del__(self):
        try:
            asyncio.run(self.stop())
            asyncio.run(self.disconnect())
        except Exception:
            print("failed to disconnect")
