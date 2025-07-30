from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import TypeAlias, List

Percentage: TypeAlias = float
Celsius: TypeAlias = int
Degrees: TypeAlias = float


@dataclass()
class Coordinates:
    latitude: Degrees
    longitude: Degrees


@dataclass()
class Camera:
    id: str
    name: str
    model: str
    modem_firmware: str
    camera_firmware: str
    last_update_time: datetime
    signal: Percentage | None = None
    temperature: Celsius | None = None
    battery: Percentage | None = None
    battery_type: str | None = None
    memory: Percentage | None = None
    notifications: List[str] | None = None
    owner: str | None = None
    coordinates: Coordinates | None = None

    @property
    def is_online(self) -> bool:
        now = datetime.now().astimezone()
        diff = now - self.last_update_time
        return diff <= timedelta(hours=24)

    def __str__(self) -> str:
        return (f"Camera(id={self.id}, name={self.name}, model={self.model}, "
                f"modem_firmware={self.modem_firmware}, camera_firmware={self.camera_firmware}, "
                f"last_update_time={self.last_update_time}, signal={self.signal}, "
                f"temperature={self.temperature}, battery={self.battery}, battery_type={self.battery_type}, "
                f"memory={self.memory}, notifications={self.notifications}, "
                f"online={self.is_online}), owner={self.owner}, coordinates={self.coordinates})")
