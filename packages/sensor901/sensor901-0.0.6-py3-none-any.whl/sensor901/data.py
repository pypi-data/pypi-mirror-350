from dataclasses import dataclass
from datetime import datetime


@dataclass
class Time:
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    millisecond: int

    def __str__(self) -> str:
        """Format the time as a string in the format 'YYYY-MM-DD HH:MM:SS.mmm'"""
        return f"20{self.year:02d}-{self.month:02d}-{self.day:02d} {self.hour:02d}:{self.minute:02d}:{self.second:02d}.{self.millisecond:03d}"

    def to_datetime(self) -> datetime:
        """Convert the Time object to a datetime object"""
        return datetime(2000 + self.year, self.month, self.day, self.hour,
                        self.minute, self.second, self.millisecond * 1000)

    @classmethod
    def from_string(cls, time_str: str) -> 'Time':
        """
        Parse a time string into a Time object.
        
        Args:
            time_str (str): Time string in the format of "YYYY-MM-DD HH:MM:SS.SSS".
            
        Returns:
            Time: Parsed Time object.
        """
        try:
            dt = datetime.fromisoformat(time_str)
        except ValueError:
            dt = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")

        return cls(year=dt.year % 100,
                   month=dt.month,
                   day=dt.day,
                   hour=dt.hour,
                   minute=dt.minute,
                   second=dt.second,
                   millisecond=dt.microsecond // 1000)

    @classmethod
    def from_bytes(cls, time_bytes: bytes) -> 'Time':
        """
        Parse time bytes into a Time object.
        
        Args:
            time_bytes (bytes): 8 bytes representing time components.
            
        Returns:
            Time: Parsed Time object.
        """
        assert len(time_bytes) == 8
        return cls(
            year=time_bytes[0],
            month=time_bytes[1],
            day=time_bytes[2],
            hour=time_bytes[3],
            minute=time_bytes[4],
            second=time_bytes[5],
            millisecond=int.from_bytes(time_bytes[6:8], byteorder='little') //
            10)

    def to_bytes(self) -> bytes:
        """
        Convert the Time object to bytes.
        
        Returns:
            bytes: 8 bytes representing time components.
        """
        result = bytearray()
        result.append(self.year)
        result.append(self.month)
        result.append(self.day)
        result.append(self.hour)
        result.append(self.minute)
        result.append(self.second)
        result.extend((self.millisecond).to_bytes(2, byteorder='little'))
        return bytes(result)


@dataclass
class Frame:
    device_name: str
    time: Time
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
                and self.time == other.time and self.acc_x == other.acc_x
                and self.acc_y == other.acc_y and self.acc_z == other.acc_z
                and self.as_x == other.as_x and self.as_y == other.as_y
                and self.as_z == other.as_z and self.gx == other.gx
                and self.gy == other.gy and self.gz == other.gz
                and self.angle_x == other.angle_x
                and self.angle_y == other.angle_y
                and self.angle_z == other.angle_z and self.temp == other.temp
                and self.electric_quantity == other.electric_quantity
                and self.rssi == other.rssi and self.version == other.version)

    @property
    def time_parsed(self) -> datetime:
        """
        Get the timestamp of the frame.

        Returns:
            datetime: Timestamp of the frame.
        """
        return self.time.to_datetime()

    def serialize(self) -> bytes:
        # Simulate serialization to bytes
        name_bytes = self.device_name.encode('ascii').ljust(12, b'\x00')
        time_bytes = self.time.to_bytes()
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
        time_data = Time.from_bytes(fr[12:20])
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
