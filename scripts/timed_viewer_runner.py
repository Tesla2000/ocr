from ocr.output import TimedWordsViewer
from pydantic_settings import BaseSettings
from pydantic_settings import CliApp
from pydantic_settings import SettingsConfigDict


class Runner(BaseSettings):
    model_config = SettingsConfigDict(
        cli_parse_args=True,
        cli_kebab_case=True,
    )
    viewer: TimedWordsViewer

    async def cli_cmd(self) -> None:
        await self.viewer.save_results("")


if __name__ == "__main__":
    CliApp.run(Runner)
