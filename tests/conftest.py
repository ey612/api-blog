# tests/conftest.py
import os
import tempfile
from pathlib import Path

import pytest

# app.py를 import하면 기본 앱이 즉시 생성되므로,
# import 전에 기본 앱도 테스트용 DB를 사용하도록 설정
_import_db_dir = tempfile.TemporaryDirectory()
_import_db_path = Path(_import_db_dir.name) / "import_test.db"

os.environ["DATABASE_URL"] = f"sqlite:///{_import_db_path}"
os.environ["SECRET_KEY"] = "pytest-only-secret-key"

from app import create_app  # noqa: E402
from models import db  # noqa: E402


@pytest.fixture
def app(tmp_path):
    # 테스트마다 서로 다른 임시 SQLite DB 사용
    db_path = tmp_path / "test_blog.db"

    test_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "SECRET_KEY": "pytest-only-secret-key",
    })

    yield test_app

    # 테스트 종료 후 DB 연결 정리
    with test_app.app_context():
        db.session.remove()
        db.engine.dispose()


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client