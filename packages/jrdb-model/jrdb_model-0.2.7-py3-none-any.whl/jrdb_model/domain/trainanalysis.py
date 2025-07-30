"""調教分析データ."""

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from ..sessioncontroll import db


class TrainAnalysisData(db.Model):
    """調教分析データ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "train_analysis"
    racehorsekey: Mapped[str] = mapped_column(
        String(255), ForeignKey("racehorse.racehorsekey"), primary_key=True
    )
    racekey: Mapped[str] = mapped_column(String(255))
    num: Mapped[int] = mapped_column()
    train_type: Mapped[str] = mapped_column(String(255))
    train_course_kind: Mapped[str] = mapped_column(String(255))
    saka: Mapped[int] = mapped_column()
    wood: Mapped[int] = mapped_column()
    dart: Mapped[int] = mapped_column()
    turf: Mapped[int] = mapped_column()
    pool: Mapped[int] = mapped_column()
    steeple: Mapped[int] = mapped_column()
    politruck: Mapped[int] = mapped_column()
    train_distance: Mapped[int] = mapped_column()
    train_juten: Mapped[int] = mapped_column()
    oikiri_score: Mapped[int] = mapped_column()
    shiage_score: Mapped[int] = mapped_column()
    train_vol_hyoka: Mapped[str] = mapped_column(String(255))
    shiage_score_change: Mapped[int] = mapped_column()
    train_comment: Mapped[str] = mapped_column(String(255))
    comment_date: Mapped[str] = mapped_column(String(255))
    train_hyoka: Mapped[int] = mapped_column()
