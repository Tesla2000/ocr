from ocr.input import AnyInput
from ocr.output import AnyOutput
from ocr.text_extractor import TextExtractor
from pydantic_settings import BaseSettings
from pydantic_settings import CliApp
from pydantic_settings import SettingsConfigDict


class OCR(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        cli_parse_args=True,
        cli_kebab_case=True,
        cli_ignore_unknown_args=False,
    )

    input: AnyInput
    text_extractor: TextExtractor
    output: AnyOutput

    async def cli_cmd(self) -> None:
        images = self.input.get_images()
        if not images:
            return
        results = await self.text_extractor.extract_from_images(images)
        await self.output.save_results(results)


if __name__ == "__main__":
    CliApp.run(OCR)
