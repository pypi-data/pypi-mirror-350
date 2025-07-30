"""計算済みスコア."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..sessioncontroll import db


class CalculatedScoreData(db.Model):
    """計算済みスコア.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "calculated_score"
    racehorsekey: Mapped[str] = mapped_column(
        ForeignKey("racehorse.racehorsekey"), primary_key=True
    )
    waku_win_rate: Mapped[float] = mapped_column()
    waku_rentai_rate: Mapped[float] = mapped_column()
