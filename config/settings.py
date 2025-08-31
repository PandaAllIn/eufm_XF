from pydantic_settings import BaseSettings
from typing import List
from enum import Enum
import os
from pathlib import Path
from dotenv import load_dotenv

# Determine the project root and load the .env file explicitly at the top
PROJECT_ROOT = Path(__file__).resolve().parents[2]
dotenv_path = PROJECT_ROOT / '.gemini' / '.env'
load_dotenv(dotenv_path=dotenv_path)

class EnvironmentType(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class AIServiceSettings(BaseSettings):
    google_api_key: str = "AIzaSyBMXkjP7uOjm1bPl5a2l-lABE1sqmvjBwA"
    openai_api_key: str = "not_set"
    perplexity_api_key: str = "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"
    default_model: str = "gemini-2.5-pro"

class ApplicationSettings(BaseSettings):
    PROJECT_ROOT: Path = PROJECT_ROOT
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEVELOPMENT
    DEBUG: bool = True
    
    @property
    def DOCS_DIR(self) -> Path:
        return self.PROJECT_ROOT / "docs"

    @property
    def WBS_DIR(self) -> Path:
        return self.PROJECT_ROOT / "wbs"

class Settings(BaseSettings):
    app: ApplicationSettings = ApplicationSettings()
    ai: AIServiceSettings = AIServiceSettings()

def get_settings() -> Settings:
    return Settings()

class ApplicationSettings(BaseSettings):
    PROJECT_ROOT: Path = PROJECT_ROOT
    ENVIRONMENT: EnvironmentType = EnvironmentType.DEVELOPMENT
    DEBUG: bool = True
    
    # Paths derived from PROJECT_ROOT
    @property
    def DOCS_DIR(self) -> Path:
        return self.PROJECT_ROOT / "docs"

    @property
    def SRC_DIR(self) -> Path:
        return self.PROJECT_ROOT / "src"

    @property
    def WBS_DIR(self) -> Path:
        return self.PROJECT_ROOT / "wbs"

class Settings(BaseSettings):
    app: ApplicationSettings = ApplicationSettings()
    ai: AIServiceSettings = AIServiceSettings()

def get_settings() -> Settings:
    return Settings()

# Example of how to use it:
# from config.settings import get_settings
# settings = get_settings()
# print(settings.app.PROJECT_ROOT)
# print(settings.ai.google_api_key)
