import grpc
from proto import mongo_pb2
from proto import mongo_pb2_grpc
import json
import grpc
from typing import Any, Dict, List, Callable

from .exceptions import *
from .wrappers.database import DatabaseClient


def grpc_call(func: Callable) -> Callable:
    def wrapper(self, *args, **kwargs):
        if not self.metadata:
            raise NotAuthenticatedException("Please login(username,password) before.")
        try:
            return func(self, *args, **kwargs)
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                try:
                    details = json.loads(e.details())
                    raise ValidationException(details.get("validation_errors", []))
                except Exception as parsing_error:
                    raise parsing_error
            elif e.code() == grpc.StatusCode.ALREADY_EXISTS:
                raise AlreadyExistsException(e)
            else:
                raise AfhException(e)
    return wrapper

class AbstractFrameHubClient():
    def __init__(self, host: str = "localhost", port: int = 42042) -> None:
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = mongo_pb2_grpc.MongoServiceStub(self.channel)
        self.adminstub = mongo_pb2_grpc.AdminStub(self.channel)
        self.metadata: List[tuple[str, str]] = []

    def database(self, database: str) -> "DatabaseClient":
        return DatabaseClient(self, database)

    # ========== 🔐 Auth / Users ==========
    def login(self, username: str, password: str) -> str:
        response = self.stub.Login(request=mongo_pb2.LoginRequest(
            username=username,
            password=password
        ))
        self.metadata = [("token", response.token)]
        return response.token

    @grpc_call
    def add_user(self, document_json: Dict[str, Any]) -> bool:
        response = self.adminstub.CreateUser(request=mongo_pb2.InsertUserRequest(
            document_json=json.dumps(document_json)
        ), metadata=self.metadata)
        return response.success

    @grpc_call
    def update_user(self, document_json: Dict[str, Any]) -> bool:
        response = self.adminstub.UpdateUser(request=mongo_pb2.UpdateUserRequest(
            document_json=json.dumps(document_json)
        ), metadata=self.metadata)
        return response.success

    @grpc_call
    def drop_user(self, username: str) -> bool:
        response = self.adminstub.DropUser(request=mongo_pb2.DropUserRequest(
            username=username
        ), metadata=self.metadata)
        return response.success

    @grpc_call
    def authenticate_user(self, database: str, collection: str, filter_json: Dict[str, Any],
                          password_field: str, password: str) -> bool:
        user = self.find_one(database, collection, filter_json)
        return user.get(password_field) == password

    # ========== 🗃️ Database ==========
    @grpc_call
    def create_database(self, name: str) -> bool:
        response = self.adminstub.CreateDatabase(request=mongo_pb2.InsertDatabaseRequest(name=name), metadata=self.metadata)
        return response.success

    @grpc_call
    def drop_database(self, name: str) -> bool:
        response = self.adminstub.DropDatabase(request=mongo_pb2.DropDatabaseRequest(name=name), metadata=self.metadata)
        return response.success

    # ========== 📄 Operation MongoDB ==========
    @grpc_call
    def insert_one(self, database: str, collection: str, document_json: Dict[str, Any]) -> str:
        response = self.stub.InsertOne(request=mongo_pb2.InsertRequest(
            database=database,
            collection=collection,
            document_json=json.dumps(document_json)
        ), metadata=self.metadata)
        return response.inserted_id

    @grpc_call
    def insert_many(self, database: str, collection: str, documents_json: List[Dict[str, Any]]) -> List[str]:
        response = self.stub.InsertMany(request=mongo_pb2.InsertManyRequest(
            database=database,
            collection=collection,
            documents_json=json.dumps(documents_json)
        ), metadata=self.metadata)
        return response.inserted_ids

    @grpc_call
    def find_one(self, database: str, collection: str, filter_json: Dict[str, Any]) -> Dict[str, Any]:
        response = self.stub.FindOne(request=mongo_pb2.MongoRequest(
            database=database,
            collection=collection,
            filter_json=json.dumps(filter_json)
        ), metadata=self.metadata)
        return json.loads(response.document_json)

    @grpc_call
    def find(self, database: str, collection: str,
             filter_json: Dict[str, Any] = {}, find_options_json: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        response = self.stub.FindMany(request=mongo_pb2.MongoRequest(
            database=database,
            collection=collection,
            filter_json=json.dumps(filter_json),
            find_options_json=json.dumps(find_options_json)
        ), metadata=self.metadata)
        return json.loads(response.documents_json)

    @grpc_call
    def update_one(self, database: str, collection: str,
                   filter_json: Dict[str, Any], update_json: Dict[str, Any]) -> int:
        response = self.stub.UpdateOne(request=mongo_pb2.UpdateRequest(
            database=database,
            collection=collection,
            filter_json=json.dumps(filter_json),
            update_json=json.dumps(update_json)
        ), metadata=self.metadata)
        return response.modified_count

    @grpc_call
    def update_many(self, database: str, collection: str,
                    filter_json: Dict[str, Any], update_json: Dict[str, Any]) -> int:
        response = self.stub.UpdateMany(request=mongo_pb2.UpdateRequest(
            database=database,
            collection=collection,
            filter_json=json.dumps(filter_json),
            update_json=json.dumps(update_json)
        ), metadata=self.metadata)
        return response.modified_count

    @grpc_call
    def delete_one(self, database: str, collection: str, filter_json: Dict[str, Any]) -> int:
        response = self.stub.DeleteOne(request=mongo_pb2.DeleteRequest(
            database=database,
            collection=collection,
            filter_json=json.dumps(filter_json)
        ), metadata=self.metadata)
        return response.deleted_count

    @grpc_call
    def delete_many(self, database: str, collection: str, filter_json: Dict[str, Any]) -> int:
        response = self.stub.DeleteMany(request=mongo_pb2.DeleteRequest(
            database=database,
            collection=collection,
            filter_json=json.dumps(filter_json)
        ), metadata=self.metadata)
        return response.deleted_count

    # ========== 📦 Schema & Transform ==========
    @grpc_call
    def schemas(self, document_json: Dict[str, Any]) -> bool:
        response = self.adminstub.Schema(request=mongo_pb2.InsertSchemaRequest(
            document_json=json.dumps(document_json)
        ), metadata=self.metadata)
        return response.success

    @grpc_call
    def transforms(self, document_json: Dict[str, Any]) -> bool:
        response = self.adminstub.Transform(request=mongo_pb2.InsertTransformRequest(
            document_json=json.dumps(document_json)
        ), metadata=self.metadata)
        return response.success