"""調教追い切りデータ."""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..sessioncontroll import db


class TrainOikiriData(db.Model):
    """調教追い切りデータ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "train_oikiri"
    racehorsekey: Mapped[str] = mapped_column(
        String(255), ForeignKey("racehorse.racehorsekey"), primary_key=True
    )
    racekey: Mapped[str] = mapped_column(String(255))
    num: Mapped[int] = mapped_column()
    day_of_week: Mapped[str] = mapped_column(String(255))
    train_date: Mapped[str] = mapped_column(String(255))
    kaisu: Mapped[int] = mapped_column()
    train_course_code: Mapped[str] = mapped_column(String(255))
    oikiri_kind: Mapped[int] = mapped_column()
    oikiri_state: Mapped[int] = mapped_column()
    rider: Mapped[int] = mapped_column()
    train_f: Mapped[int] = mapped_column()
    ten_f: Mapped[int] = mapped_column()
    mid_f: Mapped[int] = mapped_column()
    end_f: Mapped[int] = mapped_column()
    ten_f_score: Mapped[int] = mapped_column()
    mid_f_score: Mapped[int] = mapped_column()
    end_f_score: Mapped[int] = mapped_column()
    oikiri_score: Mapped[int] = mapped_column()
    awase_result: Mapped[str] = mapped_column(String(255))
    aite_oikiri_kind: Mapped[int] = mapped_column()
    aite_age: Mapped[int] = mapped_column()
    aite_class: Mapped[str] = mapped_column(String(255))
