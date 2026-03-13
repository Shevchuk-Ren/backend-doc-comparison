from pathlib import Path
from io import BytesIO
from fastapi import UploadFile, HTTPException, status
import pdfplumber
from docx import Document


class DocumentParser:
    async def parse(self, file: UploadFile) -> dict:
        if not file.filename:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="File has no name"
            )

        ext = Path(file.filename).suffix.lower()

        content = await file.read()
        await file.seek(0)

        if ext == ".txt":
            text = self._parse_txt(content)

        elif ext == ".pdf":
            text = self._parse_pdf(content)

        elif ext == ".docx":
            text = self._parse_docx(content)

        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported file type: {ext}",
            )

        normalized_text = self._normalize_text(text)

        if not normalized_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"No text could be extracted from {file.filename}",
            )

        return {
            "filename": file.filename,
            "file_type": ext.replace(".", ""),
            "chars_count": len(normalized_text),
            "preview": normalized_text[:300],
            "text": normalized_text,
            "status": "parsed",
        }

    def _parse_txt(self, content: bytes) -> str:
        try:
            return content.decode("utf-8")
        except UnicodeDecodeError:
            return content.decode("utf-8", errors="ignore")

    def _parse_pdf(self, content: bytes) -> str:
        text_parts = []

        with pdfplumber.open(BytesIO(content)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        return "\n".join(text_parts)

    def _parse_docx(self, content: bytes) -> str:
        doc = Document(BytesIO(content))
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)

    def _normalize_text(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines()]
        cleaned = "\n".join(line for line in lines if line)
        return cleaned.strip()
