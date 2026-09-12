from app.core.ids import uuid7
from app.db.base import PKMixin, PublicIdMixin, TimestampMixin


def test_uuid7_has_v7_version_and_monotonic_ms():
    first, second = uuid7(), uuid7()
    assert first.version == 7
    assert second.version == 7
    assert first != second
    assert (second.int >> 80) >= (first.int >> 80)


def test_mixins_expose_expected_columns():
    assert "id" in PKMixin.__annotations__
    assert "public_id" in PublicIdMixin.__annotations__
    assert "created_at" in TimestampMixin.__annotations__
    assert "updated_at" in TimestampMixin.__annotations__
