from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class WorkOrder(Base):
    __tablename__ = "work_orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    work_order_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )

    site_id: Mapped[str] = mapped_column(
        String,
        index=True,
        nullable=False,
    )

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    priority: Mapped[str] = mapped_column(String, default="Medium")
    status: Mapped[str] = mapped_column(String, default="Open")
    assigned_to: Mapped[str] = mapped_column(String, nullable=False)