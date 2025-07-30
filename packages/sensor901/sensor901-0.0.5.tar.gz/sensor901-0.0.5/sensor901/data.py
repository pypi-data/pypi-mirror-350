from dataclasses import dataclass
from datetime import datetime


@dataclass
class Frame:
    device_name: str
    time: str
    acc_x: float
    acc_y: float
    acc_z: float
    as_x: float
    as_y: float
    as_z: float
    gx: float
    gy: float
    gz: float
    angle_x: float
    angle_y: float
    angle_z: float
    temp: float
    electric_quantity: int
    rssi: int
    version: int

    def __eq__(self, other):
        if not isinstance(other, Frame):
            return False

        return (self.device_name == other.device_name
                and self._compare_time(self.time, other.time)
                and self.acc_x == other.acc_x and self.acc_y == other.acc_y
                and self.acc_z == other.acc_z and self.as_x == other.as_x
                and self.as_y == other.as_y and self.as_z == other.as_z
                and self.gx == other.gx and self.gy == other.gy
                and self.gz == other.gz and self.angle_x == other.angle_x
                and self.angle_y == other.angle_y
                and self.angle_z == other.angle_z and self.temp == other.temp
                and self.electric_quantity == other.electric_quantity
                and self.rssi == other.rssi and self.version == other.version)

    @staticmethod
    def _parse_time(time_str: str) -> datetime:
        """
        Parse a time string into a datetime object.

        Args:
            time_str (str): Time string in the format of "YYYY-MM-DD HH:MM:SS.SSS".

        Returns:
            datetime: Parsed datetime object.
        """
        try:
            return datetime.fromisoformat(time_str)
        except ValueError:
            return datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")

    @classmethod
    def _compare_time(cls, time1: str, time2: str) -> bool:
        """
        Compare two time strings.

        Args:
            time1 (str): First time string.
            time2 (str): Second time string.

        Returns:
            bool: True if the two time strings are equal, False otherwise.
        """
        return cls._parse_time(time1) == cls._parse_time(time2)

    @property
    def time_parsed(self) -> datetime:
        """
        Get the timestamp of the frame.

        Returns:
            datetime: Timestamp of the frame.
        """
        return self._parse_time(self.time)

    def serialize(self) -> bytes:
        # Simulate serialization to bytes (example)
        name_bytes = self.device_name.encode('ascii').ljust(12, b'\x00')
        time_bytes = b""
        now = self.time_parsed
        time_bytes += (now.year % 100).to_bytes(1, byteorder='little')
        time_bytes += now.month.to_bytes(1, byteorder='little')
        time_bytes += now.day.to_bytes(1, byteorder='little')
        time_bytes += now.hour.to_bytes(1, byteorder='little')
        time_bytes += now.minute.to_bytes(1, byteorder='little')
        time_bytes += now.second.to_bytes(1, byteorder='little')
        time_bytes += round(now.microsecond / 100).to_bytes(2,
                                                            byteorder='little')
        acc_x_bytes = int(self.acc_x * 32768 / 16).to_bytes(2,
                                                            byteorder='little',
                                                            signed=True)
        acc_y_bytes = int(self.acc_y * 32768 / 16).to_bytes(2,
                                                            byteorder='little',
                                                            signed=True)
        acc_z_bytes = int(self.acc_z * 32768 / 16).to_bytes(2,
                                                            byteorder='little',
                                                            signed=True)
        as_x_bytes = int(self.as_x * 32768 / 2000).to_bytes(2,
                                                            byteorder='little',
                                                            signed=True)
        as_y_bytes = int(self.as_y * 32768 / 2000).to_bytes(2,
                                                            byteorder='little',
                                                            signed=True)
        as_z_bytes = int(self.as_z * 32768 / 2000).to_bytes(2,
                                                            byteorder='little',
                                                            signed=True)
        gx_bytes = int(self.gx * 1024 / 100).to_bytes(2,
                                                      byteorder='little',
                                                      signed=True)
        gy_bytes = int(self.gy * 1024 / 100).to_bytes(2,
                                                      byteorder='little',
                                                      signed=True)
        gz_bytes = int(self.gz * 1024 / 100).to_bytes(2,
                                                      byteorder='little',
                                                      signed=True)
        angle_x_bytes = int(self.angle_x * 32768 / 180).to_bytes(
            2, byteorder='little', signed=True)
        angle_y_bytes = int(self.angle_y * 32768 / 180).to_bytes(
            2, byteorder='little', signed=True)
        angle_z_bytes = int(self.angle_z * 32768 / 180).to_bytes(
            2, byteorder='little', signed=True)
        temp_bytes = int(self.temp * 100).to_bytes(2,
                                                   byteorder='little',
                                                   signed=True)
        electric_quantity_bytes = self.electric_quantity.to_bytes(
            2, byteorder='little')
        rssi_bytes = self.rssi.to_bytes(2, byteorder='little', signed=True)
        version_bytes = self.version.to_bytes(2,
                                              byteorder='little',
                                              signed=True)

        return (name_bytes + time_bytes + acc_x_bytes + acc_y_bytes +
                acc_z_bytes + as_x_bytes + as_y_bytes + as_z_bytes + gx_bytes +
                gy_bytes + gz_bytes + angle_x_bytes + angle_y_bytes +
                angle_z_bytes + temp_bytes + electric_quantity_bytes +
                rssi_bytes + version_bytes)

    @classmethod
    def parse(cls, fr: bytes) -> 'Frame':
        """
        Parse a single frame into a Frame object.

        Args:
            fr (bytes): A single frame as bytes.

        Returns:
            Frame: Parsed Frame object.
        """
        device_name = fr[:12].decode('ascii').strip('\x00')
        time_data = "20{}-{}-{} {}:{}:{}.{}".format(fr[12], fr[13], fr[14],
                                                    fr[15], fr[16], fr[17],
                                                    (fr[19] << 8 | fr[18]))
        acc_x = cls.getSignInt16(fr[21] << 8 | fr[20]) / 32768 * 16
        acc_y = cls.getSignInt16(fr[23] << 8 | fr[22]) / 32768 * 16
        acc_z = cls.getSignInt16(fr[25] << 8 | fr[24]) / 32768 * 16
        as_x = cls.getSignInt16(fr[27] << 8 | fr[26]) / 32768 * 2000
        as_y = cls.getSignInt16(fr[29] << 8 | fr[28]) / 32768 * 2000
        as_z = cls.getSignInt16(fr[31] << 8 | fr[30]) / 32768 * 2000
        gx = cls.getSignInt16(fr[33] << 8 | fr[32]) * 100 / 1024
        gy = cls.getSignInt16(fr[35] << 8 | fr[34]) * 100 / 1024
        gz = cls.getSignInt16(fr[37] << 8 | fr[36]) * 100 / 1024
        angle_x = cls.getSignInt16(fr[39] << 8 | fr[38]) / 32768 * 180
        angle_y = cls.getSignInt16(fr[41] << 8 | fr[40]) / 32768 * 180
        angle_z = cls.getSignInt16(fr[43] << 8 | fr[42]) / 32768 * 180
        temp = cls.getSignInt16(fr[45] << 8 | fr[44]) / 100
        electric_quantity = fr[47] << 8 | fr[46]
        rssi = cls.getSignInt16(fr[49] << 8 | fr[48])
        version = cls.getSignInt16(fr[51] << 8 | fr[50])

        return Frame(device_name=device_name,
                     time=time_data,
                     acc_x=acc_x,
                     acc_y=acc_y,
                     acc_z=acc_z,
                     as_x=as_x,
                     as_y=as_y,
                     as_z=as_z,
                     gx=gx,
                     gy=gy,
                     gz=gz,
                     angle_x=angle_x,
                     angle_y=angle_y,
                     angle_z=angle_z,
                     temp=temp,
                     electric_quantity=electric_quantity,
                     rssi=rssi,
                     version=version)

    @staticmethod
    def getSignInt16(num: int):
        if num >= pow(2, 15):
            num -= pow(2, 16)
        return num
