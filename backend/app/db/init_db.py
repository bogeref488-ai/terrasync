from app.db.session import Base, engine

# Import models so SQLAlchemy registers them.
from app.models.user import User  # noqa: F401
from app.models.site import Site  # noqa: F401
from app.models.work_order import WorkOrder  # noqa: F401
from app.models.report import InspectionReport  # noqa: F401
from app.models.defect import Defect  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
