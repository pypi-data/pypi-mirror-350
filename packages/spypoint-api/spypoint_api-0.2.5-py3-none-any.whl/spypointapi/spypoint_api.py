import asyncio
from datetime import datetime, timedelta
from http import HTTPStatus
from typing import List
import jwt
from aiohttp import ClientSession, ClientResponse, ClientResponseError

from spypointapi import Camera
from spypointapi.cameras.camera_api_response import CameraApiResponse
from spypointapi.shared_cameras.shared_cameras_api_response import SharedCamerasApiResponse


class SpypointApiError(ClientResponseError):
    pass


class SpypointApiInvalidCredentialsError(SpypointApiError):
    pass


class SpypointApi:
    base_url = 'https://restapi.spypoint.com/api/v3'

    def __init__(self, username: str, password: str, session: ClientSession):
        self.username = username
        self.password = password
        self.session = session
        self.headers = {'Content-Type': 'application/json'}
        self.expires_at = datetime.now() - timedelta(seconds=1)

    async def async_authenticate(self):
        if datetime.now() < self.expires_at:
            return

        json = {'username': self.username, 'password': self.password}
        async with self.session.post(f'{self.base_url}/user/login', json=json, headers=self.headers) as response:
            self._raise_on_authenticate_error(response)
            body = await response.json()
            jwt_token = body['token']
            claimset = jwt.decode(jwt_token, options={"verify_signature": False})
            self.headers['Authorization'] = 'Bearer ' + jwt_token
            self.expires_at = datetime.fromtimestamp(claimset['exp'])

    @staticmethod
    def _raise_on_authenticate_error(response: ClientResponse):
        if response.status == HTTPStatus.UNAUTHORIZED:
            raise SpypointApiInvalidCredentialsError(response.request_info, response.history, status=response.status, message=response.reason, headers=response.headers)
        if not response.ok:
            raise SpypointApiError(response.request_info, response.history, status=response.status, message=response.reason, headers=response.headers)

    async def async_get_cameras(self) -> List[Camera]:
        own_cameras = await self.async_get_own_cameras()
        shared_cameras = await self.async_get_shared_cameras()
        return own_cameras + shared_cameras

    async def async_get_own_cameras(self) -> List[Camera]:
        await self.async_authenticate()
        async with self.session.get(f'{self.base_url}/camera/all', headers=self.headers) as response:
            self._raise_on_get_error(response)
            body = await response.json()
            return CameraApiResponse.from_json(body)

    async def async_get_shared_cameras(self) -> List[Camera]:
        await self.async_authenticate()
        async with self.session.get(f'{self.base_url}/shared-cameras/all', headers=self.headers) as response:
            self._raise_on_get_error(response)
            body = await response.json()
            camera_ids = SharedCamerasApiResponse.from_json(body)
            gets_by_id = [self._async_get_shared_camera(camera_id) for camera_id in camera_ids]
            return await asyncio.gather(*gets_by_id)

    async def _async_get_shared_camera(self, camera_id) -> Camera:
        await self.async_authenticate()
        async with self.session.get(f'{self.base_url}/shared-cameras/{camera_id}', headers=self.headers) as response:
            self._raise_on_get_error(response)
            body = await response.json()
            body['id'] = camera_id
            return CameraApiResponse.camera_from_json(body)

    def _raise_on_get_error(self, response: ClientResponse):
        if response.status == HTTPStatus.UNAUTHORIZED:
            self.expires_at = datetime.now() - timedelta(seconds=1)
            del self.headers['Authorization']

        if not response.ok:
            raise SpypointApiError(response.request_info, response.history, status=response.status, message=response.reason, headers=response.headers)
