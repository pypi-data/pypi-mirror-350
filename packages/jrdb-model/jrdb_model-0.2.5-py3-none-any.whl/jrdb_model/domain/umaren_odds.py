"""馬連オッズデータ."""

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..sessioncontroll import db


class UmarenOddsData(db.Model):
    """馬連オッズデータ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "umaren_odds"
    racekey: Mapped[str] = mapped_column(
        ForeignKey("bangumi.racekey"), primary_key=True
    )
    data_kbn: Mapped[int] = mapped_column()
    registered_horses: Mapped[int] = mapped_column()
    ran_horses: Mapped[int] = mapped_column()
    sold_flg: Mapped[int] = mapped_column()
    all_odds: Mapped[str] = mapped_column(type_=JSON)
    sum_of_all_bought_count: Mapped[int] = mapped_column()
