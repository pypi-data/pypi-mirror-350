from datetime import date
import json
from typing import List, Tuple
import unittest
import uuid

from pynpdc.models import (
    AccessLevel,
    AccountWithToken,
    AttachmentQuery,
    AttachmentQuerySerializer,
    AttachmentZIPQuery,
    AttachmentZIPQuerySerializer,
    DatasetQuery,
    DatasetQuerySerializer,
    RecordCreateDTO,
    RecordCreateDTOEncoder,
    RecordQuery,
    RecordQuerySerializer,
    RecordType,
)

# ------------------------------------------------------------------------------
# Account and auth models
# ------------------------------------------------------------------------------


class TestAccountWithToken(unittest.TestCase):
    def test_update_token(self) -> None:
        account = AccountWithToken(
            {
                "id": str(uuid.uuid4()),
                "email": "test@example.org",
                "accessLevel": AccessLevel.EXTERNAL.value,
                "token": "token-123",
                "directoryUser": False,
            }
        )

        self.assertEqual(account.token, "token-123")
        self.assertDictEqual(account.headers, {"Authorization": "Bearer token-123"})

        account.token = "token-124"
        self.assertEqual(account.token, "token-124")


# ------------------------------------------------------------------------------
# Queries
# ------------------------------------------------------------------------------


class TestAttachmentQuerySerializer(unittest.TestCase):
    def test(self) -> None:
        tests: List[Tuple[AttachmentQuery, str]] = [
            ({}, ""),
            ({"skip": 25}, "?skip=25"),
            ({"take": 50}, "?take=50"),
            ({"count": True}, "?count=true"),
            ({"recursive": True}, "?recursive=true"),
            ({"from": date(2024, 10, 2)}, "?from=2024-10-02"),
            ({"until": date(2024, 10, 3)}, "?until=2024-10-03"),
        ]

        ser = AttachmentQuerySerializer()

        for query, result in tests:
            self.assertEqual(ser(query), result)


class TestAttachmentZIPQuerySerializer(unittest.TestCase):
    def test(self) -> None:
        tests: List[Tuple[AttachmentZIPQuery, str]] = [
            ({}, ""),
            ({"skip": 25}, "?skip=25"),
            ({"take": 50}, "?take=50"),
            ({"count": True}, "?count=true"),
            ({"recursive": True}, "?recursive=true"),
            ({"zip": True}, "?zip=true"),
        ]

        ser = AttachmentZIPQuerySerializer()

        for query, result in tests:
            self.assertEqual(ser(query), result)


class TestDatasetQuerySerializer(unittest.TestCase):
    def test(self) -> None:
        tests: List[Tuple[DatasetQuery, str]] = [
            ({}, ""),
            ({"skip": 25}, "?skip=25"),
            ({"take": 50}, "?take=50"),
            ({"count": True}, "?count=true"),
            ({"from": date(2024, 10, 2)}, "?from=2024-10-02"),
            ({"until": date(2024, 10, 3)}, "?until=2024-10-03"),
            (
                {"count": True, "from": date(2024, 10, 2), "until": date(2024, 10, 3)},
                "?count=true&from=2024-10-02&until=2024-10-03",
            ),
        ]

        ser = DatasetQuerySerializer()

        for query, result in tests:
            self.assertEqual(ser(query), result)


class TestRecordQuerySerializer(unittest.TestCase):
    def test(self) -> None:
        tests: List[Tuple[RecordQuery, str]] = [
            ({}, ""),
            ({"skip": 25}, "?skip=25"),
            ({"take": 50}, "?take=50"),
            ({"count": True}, "?count=true"),
            ({"from": date(2024, 10, 2)}, "?from=2024-10-02"),
            ({"until": date(2024, 10, 3)}, "?until=2024-10-03"),
            (
                {"count": True, "from": date(2024, 10, 2), "until": date(2024, 10, 3)},
                "?count=true&from=2024-10-02&until=2024-10-03",
            ),
        ]

        ser = RecordQuerySerializer()

        for query, result in tests:
            self.assertEqual(ser(query), result)


# ------------------------------------------------------------------------------
# Record DTOs
# ------------------------------------------------------------------------------


class TestRecordCreateDTOEncoder(unittest.TestCase):
    def test(self) -> None:
        record = uuid.uuid4()
        parent_id = uuid.uuid4()
        ru = RecordCreateDTO(
            content={"id": 0},
            type=RecordType.UNKNOWN,
            id=record,
            parent_id=parent_id,
        )
        j = json.dumps(ru, cls=RecordCreateDTOEncoder)

        self.assertEqual(
            j,
            json.dumps(
                {
                    "content": {"id": 0},
                    "type": RecordType.UNKNOWN.value,
                    "id": str(record),
                    "parentId": str(parent_id),
                }
            ),
        )
