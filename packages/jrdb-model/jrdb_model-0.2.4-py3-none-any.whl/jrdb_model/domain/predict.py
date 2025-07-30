from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..sessioncontroll import db


class PredictData(db.Model):
    """予想データ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "predict"
    racehorsekey: Mapped[str] = mapped_column(
        ForeignKey("racehorse.racehorsekey"), primary_key=True
    )
    pp_icchaku: Mapped[float] = mapped_column()
    pp_nichaku: Mapped[float] = mapped_column()
    pp_sanchaku: Mapped[float] = mapped_column()
    rentai_rate: Mapped[float] = mapped_column()
    fukusho_rate: Mapped[float] = mapped_column()
    tansho_odds: Mapped[float] = mapped_column()
    fukusho_odds: Mapped[float] = mapped_column()
