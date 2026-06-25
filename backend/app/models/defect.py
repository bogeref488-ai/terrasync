from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db.session import Base


class Defect(Base):
    __tablename__ = "defects"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    defect_no: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    report_no: Mapped[str] = mapped_column(String(80), index=True)
    site_id: Mapped[str] = mapped_column(String(50), index=True)
    category: Mapped[str] = mapped_column(String(120))
    severity: Mapped[str] = mapped_column(String(50))
    description: Mapped[str] = mapped_column(Text)
    recommendation: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="Open")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
