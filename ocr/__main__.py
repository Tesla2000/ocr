from ocr.services.image_finder import ImageFinder
from ocr.services.text_extractor import TextExtractor
from ocr.services.writers import AnyWriter
from pydantic_settings import BaseSettings
from pydantic_settings import CliApp
from pydantic_settings import SettingsConfigDict


class OCR(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        cli_parse_args=True,
        cli_kebab_case=True,
        cli_ignore_unknown_args=False,
    )

    image_finder: ImageFinder
    text_extractor: TextExtractor
    file_writer: AnyWriter

    async def cli_cmd(self) -> None:
        images = self.image_finder.find_images()
        if not images:
            return
        results = await self.text_extractor.extract_from_images(images)
        self.file_writer.write_results(results)


if __name__ == "__main__":
    CliApp.run(OCR)
