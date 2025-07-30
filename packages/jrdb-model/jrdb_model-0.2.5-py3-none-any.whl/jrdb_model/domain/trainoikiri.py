"""調教追い切りデータ."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from ..sessioncontroll import db


class TrainOikiriData(db.Model):
    """調教追い切りデータ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "train_oikiri"
    racehorsekey: Mapped[str] = mapped_column(
        ForeignKey("racehorse.racehorsekey"), primary_key=True
    )
    racekey: Mapped[str] = mapped_column()
    num: Mapped[int] = mapped_column()
    day_of_week: Mapped[str] = mapped_column()
    train_date: Mapped[str] = mapped_column()
    kaisu: Mapped[int] = mapped_column()
    train_course_code: Mapped[str] = mapped_column()
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
    awase_result: Mapped[str] = mapped_column()
    aite_oikiri_kind: Mapped[int] = mapped_column()
    aite_age: Mapped[int] = mapped_column()
    aite_class: Mapped[str] = mapped_column()
