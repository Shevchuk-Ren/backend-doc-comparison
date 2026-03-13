from fastapi import FastAPI, HTTPException, status
from app.core.validators import DocumentValidator

doc_validator = DocumentValidator(max_size=25 * 1024 * 1024)  

async def doc_processed_payload(files) -> dict:
    processed_inputs = []

    if len(files) < 2 or len(files) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Min 3 and max 5 files needed",
)

    for file in files:
        validation = await doc_validator.validate_file(file)
        
        if not validation["valid"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "File validation failed",
                    "errors": validation["errors"]
                    }
                )
        
        processed_inputs.append({
            "filename": file.filename,
            "content_type": file.content_type,
            "size": validation["size"],
        })

    return {"files": processed_inputs}