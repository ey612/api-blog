# tests/conftest.py
import os
import tempfile
from pathlib import Path

import pytest

# app.py를 import하면 모듈 수준에서 기본 앱이 생성되므로,
# 실제 DB에 접근하지 않도록 import 전에 테스트용 DB 환경변수를 설정
_import_db_dir = tempfile.TemporaryDirectory()
_import_db_path = Path(_import_db_dir.name) / "import_test.db"

os.environ["DATABASE_URL"] = f"sqlite:///{_import_db_path}"
os.environ["SECRET_KEY"] = "pytest-only-secret-key"

from app import create_app  # noqa: E402
from models import db  # noqa: E402


@pytest.fixture
def app(tmp_path):
    # 테스트 간 데이터 간섭을 방지하기 위해 테스트마다 독립적인 SQLite DB를 생성
    db_path = tmp_path / "test_blog.db"

    test_app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}",
        "SECRET_KEY": "pytest-only-secret-key",
    })

    yield test_app

    # 테스트 종료 후 세션과 DB 연결 정리
    with test_app.app_context():
        db.session.remove()
        db.engine.dispose()


@pytest.fixture
def client(app):
    with app.test_client() as test_client:
        yield test_client