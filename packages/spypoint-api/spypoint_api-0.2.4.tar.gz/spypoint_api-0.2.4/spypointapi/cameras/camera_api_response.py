from datetime import datetime
from typing import Dict, Any, List, Optional

from spypointapi import Camera
from spypointapi.cameras.camera import Coordinates


class CameraApiResponse:

    @classmethod
    def from_json(cls, data: List[Dict[str, Any]]) -> List[Camera]:
        return [CameraApiResponse.camera_from_json(d) for d in data]

    @classmethod
    def camera_from_json(cls, data: Dict[str, Any]) -> Camera:
        config = data.get('config', {})
        status = data.get('status', {})
        return Camera(
            id=data['id'],
            name=config['name'],
            model=status['model'],
            modem_firmware=status.get('modemFirmware', ''),
            camera_firmware=status.get('version', ''),
            last_update_time=datetime.fromisoformat(status['lastUpdate'][:-1]).replace(tzinfo=datetime.now().astimezone().tzinfo),
            signal=status.get('signal', {}).get('processed', {}).get('percentage', None),
            temperature=CameraApiResponse.temperature_from_json(status.get('temperature', None)),
            battery=CameraApiResponse.battery_from_json(status.get('batteries', None)),
            battery_type=status.get('batteryType', None),
            memory=CameraApiResponse.memory_from_json(status.get('memory', None)),
            notifications=CameraApiResponse.notifications_from_json(status.get('notifications', None)),
            owner=CameraApiResponse.owner_from_json(data),
            coordinates=CameraApiResponse.coordinates_from_json(status.get('coordinates', None)),
        )

    @classmethod
    def temperature_from_json(cls, temperature: Optional[Dict[str, Any]]) -> Optional[int]:
        if not temperature or None in (temperature.get('unit'), temperature.get('value')):
            return None

        unit = temperature['unit']
        value = temperature['value']
        return value if unit == 'C' else int((value - 32) * 5 / 9)

    @classmethod
    def battery_from_json(cls, batteries: Optional[Dict[str, Any]]) -> Optional[str]:
        if not batteries:
            return None
        return max(batteries)

    @classmethod
    def memory_from_json(cls, memory: Optional[Dict[str, Any]]) -> Optional[float]:
        if not memory:
            return None
        if memory.get('size', 0) == 0:
            return None
        return round(memory.get('used') / memory.get('size') * 100, 2)

    @classmethod
    def notifications_from_json(cls, notifications: Optional[Dict[str, Any]]) -> Optional[List[str]]:
        if notifications is None:
            return None
        return [str(notification) for notification in notifications]

    @classmethod
    def owner_from_json(cls, data):
        owner = data.get('ownerFirstName', None)
        if owner is None:
            return None
        return owner.strip()

    @classmethod
    def coordinates_from_json(cls, coordinates: Optional[List[Any]]) -> Optional[Coordinates]:
        if (coordinates is None
                or len(coordinates) < 1
                or coordinates[0].get('position', {}).get('type', '') != 'Point'
                or len(coordinates[0].get('position', {}).get('coordinates', [])) != 2):
            return None
        lat_lon = coordinates[0]['position']['coordinates']
        return Coordinates(latitude=lat_lon[1], longitude=lat_lon[0])
