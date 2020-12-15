from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.room import Room

from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional

class RoomListResource(Resource):

    def get(self):
        rooms = Room.get_all_published()

        data = []

        for room in rooms:
            data.append(room.data())

        return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):

        json_data = request.get_json()
        current_user = get_jwt_identity()
        room = Room(name=json_data['name'],
                    description=json_data['description'],
                    date=json_data['date'],
                    start_time=json_data['start_time'],
                    duration=json_data['duration'],
                    user_id=current_user)

        room.save()

        return room.data(), HTTPStatus.CREATED

class RoomResource(Resource):

    @jwt_optional
    def get(self, room_id):
        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if room.is_publish == False and room.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return room.data(), HTTPStatus.OK

    @jwt_required
    def put(self, room_id):

        json_data = request.get_json()

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Access is not allowed.'}, HTTPStatus.FORBIDDEN

        room.name = json_data['name']
        room.description = json_data['description']
        room.date = json_data['date']
        room.start_time = json_data['start_time']
        room.duration = json_data['duration']

        room.save()

        return room.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, room_id):

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Access is not allowed.'}, HTTPStatus.FORBIDDEN

        room.delete()

        return {}, HTTPStatus.NO_CONTENT

class RoomPublishResource(Resource):

    @jwt_required
    def put(self, room_id):

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Access is not allowed.'}, HTTPStatus.FORBIDDEN

        room.is_publish = True
        room.save()

        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, room_id):

        room = Room.get_by_id(room_id=room_id)

        if room is None:
            return {'message': 'Room not found.'}, HTTPStatus.NOT_FOUND

        current_user = get_jwt_identity()

        if current_user != room.user_id:
            return {'message': 'Access is not allowed.'}, HTTPStatus.FORBIDDEN

        room.is_publish = False
        room.save()

        return {}, HTTPStatus.NO_CONTENT