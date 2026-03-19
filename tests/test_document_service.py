import pytest
from fastapi import HTTPException, UploadFile
from io import BytesIO

from app.services.document_service import DocumentService


class FakeValidator:
    async def validate_file(self, file):
        return {"valid": True, "size": 123, "errors": []}


class FakeInvalidValidator:
    async def validate_file(self, file):
        return {"valid": False, "size": 0, "errors": ["bad format"]}


class FakeParser:
    async def parse(self, file):
        return {
            "filename": file.filename,
            "preview": "preview text",
            "text": "full text",
        }


@pytest.mark.asyncio
async def test_returns_parsed_file_with_size():
    service = DocumentService(FakeValidator(), FakeParser(), object, object)
    file = UploadFile(filename="test.txt", file=BytesIO(b"hello"))

    result = await service.process_single(file)

    assert result["filename"] == "test.txt"
    assert result["preview"] == "preview text"
    assert result["text"] == "full text"
    assert result["size"] == 123


@pytest.mark.asyncio
async def test_raises_for_invalid_file():
    service = DocumentService(FakeInvalidValidator(), FakeParser(), object, object)
    file = UploadFile(filename="bad.exe", file=BytesIO(b"oops"))

    with pytest.raises(HTTPException) as exc:
        await service.process_single(file)

    assert exc.value.status_code == 400
    assert exc.value.detail["filename"] == "bad.exe"
