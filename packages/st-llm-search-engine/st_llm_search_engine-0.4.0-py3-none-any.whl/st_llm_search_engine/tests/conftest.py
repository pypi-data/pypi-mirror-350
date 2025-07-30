"""
Pytest配置文件，為測試提供通用的fixtures
"""
import os
import sys
from pathlib import Path

import pytest

# 將項目根目錄添加到sys.path
ROOT_DIR = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# 必須在路徑設置後才能導入
# pylint: disable=wrong-import-position
from st_llm_search_engine.settings import get_settings
# pylint: enable=wrong-import-position


@pytest.fixture(scope="session")
def app_settings():
    """獲取應用程序設置"""
    return get_settings()


@pytest.fixture(scope="session")
def test_env():
    """測試環境配置

    返回包含測試環境配置的字典
    """
    # 配置測試環境變數
    os.environ["ST_LLM_DEBUG"] = "true"
    os.environ["ST_LLM_LOG_LEVEL"] = "debug"

    return {
        "debug": True,
        "log_level": "debug"
    }
