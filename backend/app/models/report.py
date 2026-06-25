from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db.session import Base


class InspectionReport(Base):
    __tablename__ = "inspection_reports"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    report_no: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    work_order_no: Mapped[str] = mapped_column(String(80), index=True)
    site_id: Mapped[str] = mapped_column(String(50), index=True)
    report_type: Mapped[str] = mapped_column(String(120))
    status: Mapped[str] = mapped_column(String(50), default="Draft")
    summary: Mapped[str | None] = mapped_column(Text, nullable=True)
    submitted_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
