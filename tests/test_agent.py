"""Tests for verifying basic agent setup without network calls."""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import pytest


@pytest.fixture(autouse=True)
def _load_env():
    """Load environment variables for tests."""
    load_dotenv()


def test_environment_setup():
    """Required environment variables should be present."""
    api_keys = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "SERPER_API_KEY": os.getenv("SERPER_API_KEY"),
    }
    missing = [k for k, v in api_keys.items() if not v]
    assert not missing, f"Missing environment vars: {', '.join(missing)}"


def test_llm_initialization():
    """The language model should initialize without errors."""
    llm = ChatOpenAI(model="gpt-4o", temperature=0, max_tokens=100)
    assert llm is not None
