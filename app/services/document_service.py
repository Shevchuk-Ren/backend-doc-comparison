from fastapi import HTTPException, UploadFile


class DocumentService:
    def __init__(self, validator, parser):
        self.validator = validator
        self.parser = parser

    async def process_single(self, file: UploadFile) -> dict:
        validation = await self.validator.validate_file(file)
        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail={"filename": file.filename, "errors": validation["errors"]},
            )

        parsed = await self.parser.parse(file)
        parsed["size"] = validation["size"]

        return parsed
