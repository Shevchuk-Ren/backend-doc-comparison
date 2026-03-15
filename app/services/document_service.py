from fastapi import HTTPException, status
from app.core.validators import DocumentValidator
from app.services.document_parser import DocumentParser


class DocumentService:
    def __init__(self):
        self.validator = DocumentValidator()
        self.parser = DocumentParser()

    async def doc_processed(self, files) -> dict:
        if len(files) < 2 or len(files) > 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You must upload from 2 to 5 documents.",
            )

        parsed_files = []

        for file in files:
            validation = await self.validator.validate_file(file)

            if not validation["valid"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"filename": file.filename, "errors": validation["errors"]},
                )

            parsed = await self.parser.parse(file)
            parsed["size"] = validation["size"]
            parsed_files.append(parsed)

        return {"documents": parsed_files}
