from datetime import date, datetime, timezone, UTC
import os
import unittest
import uuid

import pytest

from pynpdc.utils import guard_dir, guard_path, guard_utc_datetime, serialize_date


class TestGuardDir(unittest.TestCase):
    def test_with_dir(self) -> None:
        path = os.path.dirname(__file__)
        guard_dir(path)
        self.assertTrue(True)

    def test_with_file(self) -> None:
        path = __file__
        with pytest.raises(FileNotFoundError):
            guard_dir(path)

    def test_with_unknown_path(self) -> None:
        path = f"/tmp/{uuid.uuid4()}"
        with pytest.raises(FileNotFoundError):
            guard_dir(path)


class TestGuardPath(unittest.TestCase):
    def test_with_dir(self) -> None:
        path = os.path.dirname(__file__)
        with pytest.raises(FileNotFoundError):
            guard_path(path)

    def test_with_file(self) -> None:
        path = __file__
        guard_path(path)
        self.assertTrue(True)

    def test_with_unknown_path(self) -> None:
        path = f"/tmp/{uuid.uuid4()}"
        with pytest.raises(FileNotFoundError):
            guard_path(path)


class TestGuardUTCDatetime(unittest.TestCase):
    def test_with_utc(self) -> None:
        dt = datetime.now(tz=timezone.utc)
        guard_utc_datetime(dt)
        self.assertTrue(True)

    def test_without_utc(self) -> None:
        dt = datetime.now()
        with pytest.raises(ValueError):
            guard_utc_datetime(dt)


class TestSerializeDate(unittest.TestCase):
    def test_date(self) -> None:
        d = date(2025, 4, 2)
        ser = serialize_date(d)

        self.assertEqual(ser, "2025-04-02")

    def test_datetime(self) -> None:
        dt = datetime(2025, 4, 2, 11, 13, 17, tzinfo=UTC)
        ser = serialize_date(dt)

        self.assertEqual(ser, "2025-04-02T11:13:17Z")

    def test_invalid_type(self) -> None:
        with pytest.raises(TypeError):
            serialize_date("yesterday")  # type: ignore
