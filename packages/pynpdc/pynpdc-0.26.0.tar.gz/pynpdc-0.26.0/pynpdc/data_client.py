from datetime import date, datetime
import json
import mimetypes
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder  # type: ignore
import requests
import shutil
from typing import Any, Dict, List, Optional, Tuple, cast
from typing_extensions import Unpack
import urllib3
import uuid
from werkzeug.utils import secure_filename

from .exception import APIException, MissingAccountException
from .utils import guard_dir, guard_path, guard_utc_datetime
from .models import (
    Attachment,
    AttachmentCollection,
    AttachmentQuery,
    AttachmentZIPQuery,
    AttachmentZIPQuerySerializer,
    AuthContainer,
    Content,
    Dataset,
    DatasetCollection,
    DatasetQuery,
    Label,
    LabelCollection,
    LabelQuery,
    Permission,
    PermissionAPIResponse,
    PermissionCollection,
    PrefixCollection,
    PrefixQuery,
    Record,
    RecordCollection,
    RecordCreationInfo,
    RecordCreateDTO,
    RecordCreateDTOEncoder,
    RecordQuery,
    RecordType,
    AttachmentCreateDTO,
    AttachmentCreationInfo,
    DEFAULT_CHUNK_SIZE,
)

DATA_STAGING_ENTRYPOINT = "https://beta.data.npolar.no/-/api/"
DATA_LIFE_ENTRYPOINT = "https://next.api.npolar.no/"


class DataClient:
    """
    A client to communicate with the NPDC dataset module

    Attributes:
        entrypoint (str): The entrypoint of the Rest API with a trailing slash
        verify_ssl (bool): Set to false, when the Rest API has a self signed
            certificate
        token (str | None): A login token as returned from AuthClient.login.
            This is needed for accessing non-public data or changing data.
    """

    def __init__(
        self,
        entrypoint: str,
        *,
        verify_ssl: bool = True,
        auth: Optional[AuthContainer] = None,
    ) -> None:
        """
        Create a new DataClient.

        Args:
            entrypoint (str): The entrypoint of the Rest API with a trailing
                slash
            verify_ssl (bool): Set to false, when the Rest API has a self signed
                certificate
            auth (AuthContainer): An optional Account object used for
                authentification.
        """
        self.entrypoint: str = entrypoint
        self.auth: Optional[AuthContainer] = auth
        self.verify_ssl: bool = verify_ssl

    def _exec_request(
        self, method: str, endpoint: str, *, data: Any = None, stream: bool = False
    ) -> requests.Response:
        if method != "GET" and self.auth is None:
            raise MissingAccountException

        kwargs: Dict[str, Any] = {"verify": self.verify_ssl, "stream": stream}

        if self.auth is not None:
            kwargs["headers"] = self.auth.headers

        if type(data) is MultipartEncoder:
            kwargs["headers"]["Content-Type"] = data.content_type
            kwargs["data"] = data
        elif type(data) is dict:
            kwargs["json"] = data
        elif self._is_list_of_dicts(data):
            kwargs["headers"]["Content-Type"] = "application/json-seq"
            kwargs["data"] = "\n".join([json.dumps(item) for item in data])
        elif data is not None:
            raise ValueError("Unknown data format")

        response = requests.request(method, endpoint, **kwargs)

        if response.status_code not in [200, 201, 204, 207]:
            raise APIException(response)

        return response

    def _is_list_of_dicts(self, data: Any) -> bool:
        if type(data) is not list:
            return False
        for item in data:
            if type(item) is not dict:
                return False
        return True

    def get_api_version(self) -> str:
        """
        Returns the version of the Dataset API (aka Kinko)

        Returns:
            str: the short GIT sha of the API
        """

        response = self._exec_request("GET", self.entrypoint)
        return str(response.json().get("version", "undefined"))

    # ==========================================================================
    # DATASETS
    # ==========================================================================

    # !IMPL POST /dataset/
    def create_dataset(self, content: Content) -> Dataset:
        """
        Save a new dataset in the NPDC dataset module.

        Args:
            content (Content): The user generated dataset content.

        Returns:
            Dataset: the created dataset including the ID and file metadata

        Raises:
            ValueError: if the content arg is not a dict
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.

        """
        if not isinstance(content, dict):
            raise ValueError("content has to be a dict")

        endpoint = f"{self.entrypoint}dataset/"
        response = self._exec_request("POST", endpoint, data=content)
        return Dataset(response.json(), client=self)

    # !IMPL GET /dataset/
    def get_datasets(
        self,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        from_: Optional[date | datetime] = None,
        **query: Unpack[DatasetQuery],
    ) -> DatasetCollection:
        """
        Retrieve a list of datasets by query.

        The return value is a DatasetCollection that yields the Datasets when
        used in a for loop.

        Example:
            client = DataClient(DATA_LIFE_ENTRYPOINT)
            query = "fimbulisen"
            for dataset in client.get_datasets(q=query):
                print(dataset.id, dataset.content["title"])

        Args:
            chunk_size (int): the number of models fetched per chunk size
            from_: replacement for from query. (from is reserved and cannot be
                used as a kwarg.)
            query (dict):
                the query for the dataset retreival. See
                https://docs.data.npolar.no/api/#/dataset/get_dataset_
                for details

        Returns:
            DatasetCollection an iterator to fetch the Dataset objects
        """

        if from_ is not None and query.get("from") is None:
            query["from"] = from_

        return DatasetCollection(client=self, query=query, chunk_size=chunk_size)

    # !IMPL GET /dataset/{datasetID}
    def get_dataset(self, dataset_id: uuid.UUID) -> Optional[Dataset]:
        """
        Retrieve a single dataset by ID.

        When the dataset is not found, None is returned.

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset

        Returns:
            Dataset | None

        Raises:
            APIException: If HTTP status code is neither 200 or 404. Mostly this
                will be an authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}"

        try:
            response = self._exec_request("GET", endpoint)
        except APIException as e:
            if e.status_code == 404:
                return None
            raise e

        return Dataset(response.json(), client=self)

    # !IMPL PUT /dataset/{datasetID}
    def update_dataset(self, dataset_id: uuid.UUID, content: Content) -> Dataset:
        """
        Update the metadata of a dataset.

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            content (Content): The user generated dataset content.

        Returns:
            Dataset: the updated dataset

        Raises:
            ValueError: if the content arg is not a dict
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        if not isinstance(content, dict):
            raise ValueError("content has to be a dict")

        endpoint = f"{self.entrypoint}dataset/{dataset_id}"
        response = self._exec_request("PUT", endpoint, data=content)
        return Dataset(response.json(), client=self)

    # !IMPL DELETE /dataset/{datasetID}
    def delete_dataset(self, dataset_id: uuid.UUID) -> None:
        """
        Delete the dataset.

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}"
        self._exec_request("DELETE", endpoint)

    # ==========================================================================
    # ATTACHMENTS
    # ==========================================================================

    # !IMPL GET /dataset/{datasetID}/attachment/
    def get_attachments(
        self,
        dataset_id: uuid.UUID,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        from_: Optional[date | datetime] = None,
        **query: Unpack[AttachmentQuery],
    ) -> AttachmentCollection:
        """
        Retrieve a list of attachments by query

        The return value is an AttachmentCollection that yields the Attachments
        when used in a for loop.

        Args:
            dataset_id (uuid.UUID): the UUID of the related dataset
            chunk_size (int): the number of models fetched per chunk size
            from_: replacement for from query. (from is reserved and cannot be
                used as a kwarg.)
            query (dict):
                the query for the attachment retreival. See
                https://docs.data.npolar.no/api/#/attachment/get_dataset__datasetId__attachment_
                for details

        Returns:
            AttachmentCollection  an iterator to fetch the Attachment objects
        """

        if from_ is not None and query.get("from") is None:
            query["from"] = from_

        return AttachmentCollection(
            dataset_id, client=self, query=query, chunk_size=chunk_size
        )

    # !IMPL GET /dataset/{datasetID}/attachment/{attachmentID}
    def get_attachment(
        self, dataset_id: uuid.UUID, attachment_id: uuid.UUID
    ) -> Optional[Attachment]:
        """
        Retrieve a single attachment by dataset and attachment ID.

        When the attachment is not found, None is returned.

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            attachment_id (uuid.UUID): the UUID of the attachment

        Returns:
            Attachment | None

        Raises:
            APIException: If HTTP status code is neither 200 or 404. Mostly this
                will be an authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/attachment/{attachment_id}"

        try:
            response = self._exec_request("GET", endpoint)
        except APIException as e:
            if e.status_code == 404:
                return None
            raise e

        return Attachment(response.json(), client=self)

    def get_attachment_reader(
        self, dataset_id: uuid.UUID, attachment_id: uuid.UUID
    ) -> urllib3.response.HTTPResponse:
        """
        Retrieve a reader to stream the attachment content.

        When the attachment should be downloaded it is simpler to use the method
        download_attachment or download_attachments.

        Args:
            dataset_id (str): The dataset id in form of a UUID
            attachment_id (str): The attachment id in form of a UUID

        Returns:
            stream: A reader to access the attachment content
        """
        endpoint = (
            f"{self.entrypoint}dataset/{dataset_id}/attachment/{attachment_id}/_blob"
        )

        resp = self._exec_request("GET", endpoint, stream=True)
        resp.raw.decode_content = True
        return cast(urllib3.response.HTTPResponse, resp.raw)

    def create_file_upload(self, path: str) -> AttachmentCreateDTO:
        """
        Create and return an AttachmentCreateDTO instance that represents a file
        upload including a reader to fetch the data and meta data as filename
        and mime type

        Args:
            path (str): The path of the file to upload. Best practice is to use
                an absolute path

        Returns:
            AttachmentCreateDTO: An AttachmentCreateDTO instance

        """
        return AttachmentCreateDTO(
            open(path, "rb"),
            os.path.basename(path),
            mime_type=mimetypes.guess_type(path)[0],
        )

    def add_attachment(
        self, dataset_id: uuid.UUID, upload: AttachmentCreateDTO
    ) -> AttachmentCreationInfo:
        """
        Add a single attachments to a dataset

        Args:
            dataset_id (uuid.UUID): The dataset id in form of a UUID
            upload: (AttachmentCreateDTO) An AttachmentCreateDTO instance

        Returns:
            AttachmentCreateInfo

        Raises:
            MissingAccountException: If no account is available
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        return self.add_attachments(dataset_id, [upload])[0]

    # !IMPL POST /dataset/{datasetID}/attachment/
    def add_attachments(
        self, dataset_id: uuid.UUID, uploads: List[AttachmentCreateDTO]
    ) -> List[AttachmentCreationInfo]:
        """
        Add several attachments to a dataset

        Args:
            dataset_id (uuid.UUID): The dataset id in form of a UUID
            uploads: (AttachmentCreateDTO[]) A list of AttachmentCreateDTO
                instances

        Returns:
            AttachmentCreateInfo[]

        Raises:
            MissingAccountException: If no account is available
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/attachment/"
        data: List[Tuple[Any, ...]] = []
        for upload in uploads:
            data = [*data, *upload._get_multiparts()]
        multipart = MultipartEncoder(data)

        response = self._exec_request("POST", endpoint, data=multipart, stream=True)
        response_data = response.json()

        if response.status_code == 207:
            # if there is at least one response object with id == "" it means
            # that the request was only partially successful.
            if len([item for item in response_data if item["id"] == ""]) > 0:
                raise APIException(response)

        return [AttachmentCreationInfo(item) for item in response_data]

    # !IMPL PUT /dataset/{datasetID}/attachment/{attachmentID}
    def update_attachment(
        self,
        dataset_id: uuid.UUID,
        attachment_id: uuid.UUID,
        *,
        description: str,
        filename: str,
        prefix: str,
        released: Optional[datetime],
        title: str,
    ) -> Attachment:
        """
        Update the attachment metadata

        Args:
            dataset_id (uuid.UUID): The dataset id in form of a UUID
            attachment_id (uuid.UUID): The attachment id in form of a UUID
            description (str): the description
            filename (str): the file name
            prefix: (str) the prefix of the file
            released: (datetime) the released date or None for "private"
                attachments
            title (str): the title

        Returns:
            Attachment: The updated Attachment metadata

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
            ValueError: when the released arg does not have timezone UTC
        """

        guard_utc_datetime(released)

        endpoint = f"{self.entrypoint}dataset/{dataset_id}/attachment/{attachment_id}"
        payload = {
            "description": description,
            "filename": filename,
            "prefix": prefix,
            "title": title,
            "released": None,
        }
        if released is not None:
            payload["released"] = released.isoformat().replace("+00:00", "Z")

        response = self._exec_request("PUT", endpoint, data=payload)
        return Attachment(response.json(), client=self)

    # !IMPL DELETE /dataset/{datasetID}/attachment/{attachmentID}
    def delete_attachment(
        self, dataset_id: uuid.UUID, attachment_id: uuid.UUID
    ) -> None:
        """
        Delete the attachment.

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            attachment_id (uuid.UUID): the UUID of the attachment

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/attachment/{attachment_id}"
        self._exec_request("DELETE", endpoint)

    # !IMPL GET /dataset/{datasetID}/attachment/_blob
    def download_attachments_as_zip(
        self,
        dataset_id: uuid.UUID,
        target_dir: str,
        **query: Unpack[AttachmentZIPQuery],
    ) -> str:
        """
        Download dataset attachments as a zip file.

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            target_dir (str): the directory the zip file is downloaded to
            query (dict):
                the query for including/excluding attachments in the ZIP file.
                See
                https://docs.data.npolar.no/api/#/attachment/get_dataset__datasetID__attachment__blob
                for details

        Returns:
            str: the path of the zip file

        Raises:
            FileNotFoundError: target_dir is not a directory
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        guard_dir(target_dir)

        ser = AttachmentZIPQuerySerializer()
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/attachment/_blob{ser(query)}"
        resp = self._exec_request("GET", endpoint, stream=True)
        resp.raw.decode_content = True

        filename = f"{dataset_id}_files.zip"
        path = os.path.join(target_dir, filename)
        with resp.raw as src:
            with open(path, "wb") as dest:
                shutil.copyfileobj(src, dest)

        return path

    # !IMPL GET /dataset/{datasetID}/attachment/{attachmentID}/_blob
    def download_attachment(
        self, dataset_id: uuid.UUID, attachment_id: uuid.UUID, target_dir: str
    ) -> Optional[str]:
        """
        Download an attachment of a dataset.

        For security reasons the filename of the downloaded file may differ
        from the filename in the attachment metadata

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            attachment_id (uuid.UUID): the UUID of the attachment
            target_dir (str): the directory the attachments is downloaded to

        Returns:
            str: the path of the file

        Raises:
            FileNotFoundError: target_dir is not a directory
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        guard_dir(target_dir)

        attachment = self.get_attachment(dataset_id, attachment_id)
        if attachment is None:
            return None

        filename = secure_filename(attachment.filename)

        path = os.path.join(target_dir, filename)
        with attachment.reader() as src:
            with open(path, "wb") as dest:
                shutil.copyfileobj(src, dest)

        return path

    def upload_attachments(
        self, dataset_id: uuid.UUID, paths: List[str]
    ) -> List[AttachmentCreationInfo]:
        """
        Upload a number of attachments to the dataset

        It is not possible to provide title and description. If this is crucial
        use upload_attachment

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            paths (str[]): a list of paths of the files to upload. Best practice
                is to use absolute paths

        Returns:
            AttachmentCreateInfo[]

        Raises:
            FileNotFoundError: one or more paths do not exist
            MissingAccountException: If no account is available
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        map(guard_path, paths)

        uploads = [self.create_file_upload(path) for path in paths]
        return self.add_attachments(dataset_id, uploads)

    def upload_attachment(
        self,
        dataset_id: uuid.UUID,
        path: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        prefix: Optional[str] = None,
        released: Optional[datetime] = None,
    ) -> AttachmentCreationInfo:
        """
        Upload a number of attachments to the dataset

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            path (str): the path of the file to upload. Best practice is to use
                an absolute path
            title (str | None): an optional title
            description (str | None): an optional description
            prefix (str | None): an optional prefix
            released (datetime | None): an optional release date

        Returns:
            AttachmentCreateInfo

        Raises:
            FileNotFoundError: one or more paths do not exist
            MissingAccountException: If no account is available
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        guard_path(path)

        upload = self.create_file_upload(path)
        upload.title = title
        upload.description = description
        upload.prefix = prefix
        upload.released = released

        return self.add_attachment(dataset_id, upload)

    # ==========================================================================
    # RECORDS
    # ==========================================================================

    # !IMPL POST /dataset/{datasetID}/record/
    def add_record(
        self,
        dataset_id: uuid.UUID,
        record: RecordCreateDTO,
    ) -> Record:
        """
        Add a record to a dataset

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            record (RecordCreateDTO): a record upload instance

        Returns:
            RecordCreateInfo

        Raises:
            APIException: If HTTP status code > 207. Mostly this will be an
                authentification or authorisation issue.
        """
        record_dto = RecordCreateDTOEncoder().default(record)
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/record/"
        response = self._exec_request("POST", endpoint, data=record_dto)
        return Record(response.json())

    # !IMPL POST /dataset/{datasetID}/record/_bulk
    def add_records(
        self, dataset_id: uuid.UUID, records: List[RecordCreateDTO]
    ) -> RecordCreationInfo:
        """
        Add several records to a dataset

        Args:
            dataset_id (uuid.UUID): The UUID of the dataset
            records: (RecordCreateDTO[]) A list of RecordCreateDTO instances

        Returns:
            RecordCreateInfo[]

        Raises:
            MissingAccountException: If no account is available
            ValueError: If content is not a dict
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """

        record_dtos = [RecordCreateDTOEncoder().default(record) for record in records]
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/record/_bulk"
        response = self._exec_request("POST", endpoint, data=record_dtos)
        return RecordCreationInfo(response.json())

    # !IMPL GET /dataset/{datasetID}/record/
    def get_records(
        self,
        dataset_id: uuid.UUID,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        from_: Optional[date | datetime] = None,
        **query: Unpack[RecordQuery],
    ) -> RecordCollection:
        """
        Retrieve a list of records by query

        The return value is an RecordCollection that yields the records
        when used in a for loop.

        Args:
            dataset_id (uuid.UUID): the UUID of the related dataset
            chunk_size (int): the number of models fetched per chunk size
            from_: replacement for from query. (from is reserved and cannot be
                used as a kwarg.)
            query (dict):
                the query for the attachment retreival. See
                https://docs.data.npolar.no/api/#/record/get_dataset__datasetID__record_
                for details

        Returns:
            RecordCollection: an iterator to fetch the Record objects
        """

        if from_ is not None and query.get("from") is None:
            query["from"] = from_

        return RecordCollection(
            dataset_id, client=self, query=query, chunk_size=chunk_size
        )

    # !IMPL GET /dataset/{datasetID}/record/{recordID}
    def get_record(
        self, dataset_id: uuid.UUID, record_id: uuid.UUID
    ) -> Optional[Record]:
        """
        Retrieve a single record by dataset and record ID.

        When the record is not found, None is returned.

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            record_id (uuid.UUID): the UUID of the record

        Returns:
            Record | None: a record model or None

        Raises:
            APIException: If HTTP status code is neither 200 or 404. Mostly this
                will be an authentification or authorisation issue.
        """

        endpoint = f"{self.entrypoint}dataset/{dataset_id}/record/{record_id}"

        try:
            response = self._exec_request("GET", endpoint)
        except APIException as e:
            if e.status_code == 404:
                return None
            raise e
        return Record(response.json(), client=self)

    # !IMPL PUT /dataset/{datasetID}/record/{recordID}

    # change only content and type

    def update_record(
        self,
        dataset_id: uuid.UUID,
        record_id: uuid.UUID,
        content: Content,
        type: RecordType,
    ) -> Record:
        """
        Update a dataset record

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            record_id (uuid.UUID): the UUID of the record
            content (Content): The record data
            type (RecordType): The record type

        Returns:
            Record: the updated record

        Raises:
            APIException: If HTTP status code > 200. Mostly this will be an
                authentification or authorisation issue.
        """

        endpoint = f"{self.entrypoint}dataset/{dataset_id}/record/{record_id}"
        data = {"content": content, "type": type.value}
        response = self._exec_request("PUT", endpoint, data=data)
        return Record(response.json(), client=self)

    # !IMPL DELETE /dataset/{datasetID}/record/{recordID}
    def delete_record(self, dataset_id: uuid.UUID, record_id: uuid.UUID) -> None:
        """
        Delete the record.

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            record_id (uuid.UUID): the UUID of the record

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/record/{record_id}"
        self._exec_request("DELETE", endpoint)

    # ==========================================================================
    # PERMISSIONS
    # ==========================================================================

    # !IMPL POST /dataset/{datasetID}/permission/
    def add_permission(
        self,
        dataset_id: uuid.UUID,
        user_id: uuid.UUID,
        *,
        may_read: bool = False,
        may_update: bool = False,
        may_delete: bool = False,
    ) -> Permission:
        """
        Add user permissions to a dataset

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            user_id (uuid.UUID): the UUID of the user account
            may_read (bool): the read permission for this dataset
            may_update (bool): the update permission for this dataset
            may_delete (bool): the delete permission for this dataset

        Returns:
            Permission

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        raw = {
            "userId": str(user_id),
            "mayRead": may_read,
            "mayUpdate": may_update,
            "mayDelete": may_delete,
        }
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/permission/"
        response = self._exec_request("POST", endpoint, data=raw)
        perm_response: PermissionAPIResponse = response.json()
        return Permission(perm_response)

    # !IMPL GET /dataset/{datasetID}/permission/
    def get_permissions(self, dataset_id: uuid.UUID) -> PermissionCollection:
        """
        Retrieve a list of permissions of a dataset

        The return value is an PermissionCollection that yields the Permissions
        when used in a for loop.

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset

        Returns:
            PermissionCollection an iterator to fetch the Permission objects
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/permission/"
        response = self._exec_request("GET", endpoint)
        raw = response.json()
        return PermissionCollection(raw["items"])

    # !IMPL GET /dataset/{datasetID}/permission/{userID}
    def get_permission(
        self, dataset_id: uuid.UUID, user_id: uuid.UUID
    ) -> Optional[Permission]:
        """
        Get user permissions of a dataset

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            user_id (uuid.UUID): the UUID of the user account

        Returns:
            Permission

        Raises:
            APIException: If HTTP status code is neither 200 or 404. Mostly this
                will be an authentification or authorisation issue.

        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/permission/{user_id}"

        try:
            response = self._exec_request("GET", endpoint)
        except APIException as e:
            if e.status_code == 404:
                return None
            raise e

        raw = response.json()
        return Permission(raw)

    # !IMPL PUT /dataset/{datasetID}/permission/{userID}
    def update_permission(
        self,
        dataset_id: uuid.UUID,
        user_id: uuid.UUID,
        *,
        may_read: bool = False,
        may_update: bool = False,
        may_delete: bool = False,
    ) -> Permission:
        """
        Update user permissions of a dataset

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            user_id (uuid.UUID): the UUID of the user account
            may_read (bool): the read permission for this dataset
            may_update (bool): the update permission for this dataset
            may_delete (bool): the delete permission for this dataset

        Returns:
            Permission

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        raw = {
            "mayRead": may_read,
            "mayUpdate": may_update,
            "mayDelete": may_delete,
        }
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/permission/{user_id}"
        response = self._exec_request("PUT", endpoint, data=raw)
        perm_response: PermissionAPIResponse = response.json()
        return Permission(perm_response)

    # !IMPL DELETE /dataset/{datasetID}/permission/{userID}
    def delete_permission(self, dataset_id: uuid.UUID, user_id: uuid.UUID) -> None:
        """
        Delete user permissions of a dataset

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            user_id (uuid.UUID): the UUID of the user account
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/permission/{user_id}"
        self._exec_request("DELETE", endpoint)

    # ==========================================================================
    # PREFIX
    # ==========================================================================

    # !IMPL GET /dataset/{datasetID}/prefix/
    def get_prefixes(
        self,
        dataset_id: uuid.UUID,
        chunk_size: int = DEFAULT_CHUNK_SIZE,
        **query: Unpack[PrefixQuery],
    ) -> PrefixCollection:
        """
        Retrieve a list of attachment prefixes of a dataset. This prefixes are
        used to create a folder-like file structure.

        The return value is a PrefixCollection that yields the Prefixes when
        used in a for loop.

        Args:
            dataset_id (uuid.UUID): the UUID of the dataset
            chunk_size (int): the number of models fetched per chunk size
            query (dict):
                the query for the dataset retreival. See
                https://docs.data.npolar.no/api/#/prefix/get_dataset__datasetID__prefix_
                for details

        Returns:
            PrefixCollection an iterator to fetch the Prefix objects
        """
        return PrefixCollection(
            client=self, dataset_id=dataset_id, query=query, chunk_size=chunk_size
        )

    # ==========================================================================
    # LABEL
    # ==========================================================================

    # !IMPL POST /label/
    def create_label(
        self,
        type: str,
        *,
        title: str,
        url: Optional[str] = None,
    ) -> Label:
        """
        Save a new label in the DB

        Args:
            type (str): The type of the label
            title (str): The title of the label
            url (str | None): The optional url of the label

        Returns:
            Label: the label including the ID and metadata

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.

        """
        raw = {
            "type": type,
            "title": title,
        }
        if url is not None:
            raw["url"] = url

        endpoint = f"{self.entrypoint}label/"
        response = self._exec_request("POST", endpoint, data=raw)
        return Label(response.json(), client=self)

    # !IMPL GET /label/
    def get_labels(
        self, chunk_size: int = DEFAULT_CHUNK_SIZE, **query: Unpack[LabelQuery]
    ) -> LabelCollection:
        """
        Retrieve a list of labels by query.

        The return value is a LabelCollection that yields the Labels when
        used in a for loop.

        Args:
            chunk_size (int): the number of models fetched per chunk size
            query (dict):
                the query for the label retreival.

        Returns:
            LabelCollection an iterator to fetch the Label objects
        """
        return LabelCollection(client=self, query=query, chunk_size=chunk_size)

    # !IMPL GET /label/{labelID}
    def get_label(self, label_id: uuid.UUID) -> Optional[Label]:
        """
        Retrieve a single label by ID.

        When the label is not found, None is returned.

        Args:
            label_id (uuid.UUID): the UUID of the label

        Returns:
            Label | None

        Raises:
            APIException: If HTTP status code is neither 200 or 404.
        """
        endpoint = f"{self.entrypoint}label/{label_id}"

        try:
            response = self._exec_request("GET", endpoint)
        except APIException as e:
            if e.status_code == 404:
                return None
            raise e  # pragma: no cover (should never happen unless Kinko has issues

        return Label(response.json(), client=self)

    # !IMPL PUT /label/{labelID}
    def update_label(
        self,
        label_id: uuid.UUID,
        *,
        type: str,
        title: str,
        url: Optional[str] = None,
    ) -> Label:
        """
        Update the label with the given ID

        Args:
            label_id (uuid.UUID): the UUID of the label
            type (str): The type of the label
            title (str): The title of the label
            url (str | None): The optional url of the label

        Returns:
            Label: the updated label

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """

        raw = {
            "type": type,
            "title": title,
        }
        if url is not None:
            raw["url"] = url

        endpoint = f"{self.entrypoint}label/{label_id}"
        response = self._exec_request("PUT", endpoint, data=raw)
        return Label(response.json(), client=self)

    # !IMPL DELETE /label/{labelID}
    def delete_label(self, label_id: uuid.UUID) -> None:
        """
        Delete the label.

        Args:
            label_id (uuid.UUID): the UUID of the label

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}label/{label_id}"
        self._exec_request("DELETE", endpoint)

    # ==========================================================================
    # LABEL RELATIONS
    # ==========================================================================

    # !IMPL POST /dataset/{datasetID}/label/{labelID}
    def add_label_to_dataset(self, label_id: uuid.UUID, dataset_id: uuid.UUID) -> None:
        """
        Add an existing label to an existing dataset

        Args:
            label_id (uuid.UUID): the UUID of the label
            dataset_id (uuid.UUID): the UUID of the dataset

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/label/{label_id}"
        self._exec_request("POST", endpoint)

    # !IMPL DELETE /dataset/{datasetID}/label/{labelID}
    def remove_label_from_dataset(
        self, label_id: uuid.UUID, dataset_id: uuid.UUID
    ) -> None:
        """
        Remove a label from a dataset

        Args:
            label_id (uuid.UUID): the UUID of the label
            dataset_id (uuid.UUID): the UUID of the dataset

        Raises:
            APIException: If HTTP status code > 201. Mostly this will be an
                authentification or authorisation issue.
        """
        endpoint = f"{self.entrypoint}dataset/{dataset_id}/label/{label_id}"
        self._exec_request("DELETE", endpoint)


# @deprecated. Kept for compatibity with older code
DatasetClient = DataClient
