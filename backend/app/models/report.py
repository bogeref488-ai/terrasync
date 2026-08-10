from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class Report(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    report_id: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    work_order_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    site_id: Mapped[str] = mapped_column(String, index=True, nullable=False)

    template_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    template_name: Mapped[str] = mapped_column(String, nullable=False)

    inspector_name: Mapped[str] = mapped_column(String, nullable=False)
    inspector_company: Mapped[str] = mapped_column(String, nullable=True)

    inspection_status: Mapped[str] = mapped_column(String, default="Completed")
    approval_status: Mapped[str] = mapped_column(String, default="Pending Review")

    coordinator_name: Mapped[str] = mapped_column(String, nullable=True)
    coordinator_comment: Mapped[str] = mapped_column(Text, nullable=True)
    reviewed_at: Mapped[str] = mapped_column(String, nullable=True)

    findings: Mapped[str] = mapped_column(Text, nullable=True)
    recommendations: Mapped[str] = mapped_column(Text, nullable=True)

    answers: Mapped[str] = mapped_column(Text, nullable=False)
    defects: Mapped[str] = mapped_column(Text, nullable=True)

    created_at: Mapped[str] = mapped_column(String, nullable=False)