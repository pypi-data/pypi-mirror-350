"""予想レースデータ."""

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..sessioncontroll import db


class PredictRaceData(db.Model):
    """予想レースデータ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "predict_race"
    racekey: Mapped[str] = mapped_column(
        ForeignKey("bangumi.racekey"), primary_key=True
    )
    umaren: Mapped[str] = mapped_column(type_=JSON)
    wide: Mapped[str] = mapped_column(type_=JSON)
    wakuren: Mapped[str] = mapped_column(type_=JSON)
