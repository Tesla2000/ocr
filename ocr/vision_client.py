from pathlib import Path
from typing import Any

from google.auth.api_key import Credentials
from google.cloud import vision_v1
from google.cloud.vision_v1 import ImageAnnotatorClient
from pydantic import BaseModel
from pydantic import SecretStr


class VisionClient(BaseModel):
    token: SecretStr
    _client: ImageAnnotatorClient

    def model_post_init(self, context: Any, /) -> None:
        self._client = ImageAnnotatorClient(
            credentials=Credentials(token=self.token.get_secret_value())  # type: ignore[no-untyped-call]
        )

    def extract_text(self, image_path: Path) -> str:
        image_content = image_path.read_bytes()
        image = vision_v1.Image(content=image_content)
        response = self._client.text_detection(image=image)
        if response.error.message:
            raise RuntimeError(f"Vision API error: {response.error.message}")
        if not response.text_annotations:
            return ""
        description = response.text_annotations[0].description
        return str(description) if description else ""
