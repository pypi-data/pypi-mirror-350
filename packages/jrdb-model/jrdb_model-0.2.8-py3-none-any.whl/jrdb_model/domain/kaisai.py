"""開催データ定義."""

from typing import List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from jrdb_model import BangumiData

from ..sessioncontroll import db


class KaisaiData(db.Model):
    """開催データ."""

    __tablename__ = "kaisai"
    kaisaikey: Mapped[str] = mapped_column(String(255), primary_key=True)
    ymd: Mapped[int] = mapped_column()
    kaisai_kbn: Mapped[int] = mapped_column()
    day_of_week: Mapped[str] = mapped_column(String(255))
    course_name: Mapped[str] = mapped_column(String(255))
    tenko: Mapped[int] = mapped_column()
    turf_baba: Mapped[int] = mapped_column()
    turf_baba_abst: Mapped[int] = mapped_column()
    turf_baba_detail: Mapped[int] = mapped_column()
    turf_baba_in: Mapped[int] = mapped_column()
    turf_baba_center: Mapped[int] = mapped_column()
    turf_baba_out: Mapped[int] = mapped_column()
    turf_baba_sa: Mapped[int] = mapped_column()
    turf_baba_straight_saiuchi: Mapped[int] = mapped_column()
    turf_baba_straight_in: Mapped[int] = mapped_column()
    turf_baba_straight_center: Mapped[int] = mapped_column()
    turf_baba_straight_out: Mapped[int] = mapped_column()
    turf_baba_straight_oosoto: Mapped[int] = mapped_column()
    dart_baba: Mapped[int] = mapped_column()
    dart_baba_abst: Mapped[int] = mapped_column()
    dart_baba_detail: Mapped[int] = mapped_column()
    dart_baba_in: Mapped[int] = mapped_column()
    dart_baba_center: Mapped[int] = mapped_column()
    dart_baba_out: Mapped[int] = mapped_column()
    dart_baba_sa: Mapped[int] = mapped_column()
    data_kbn: Mapped[int] = mapped_column()
    renzoku_day: Mapped[int] = mapped_column()
    turf_kind: Mapped[int] = mapped_column()
    turf_length: Mapped[int] = mapped_column()
    tennatsu: Mapped[int] = mapped_column()
    stopfreeze: Mapped[int] = mapped_column()
    precipitation: Mapped[int] = mapped_column()

    # 子に対して
    races: Mapped[Optional[List["BangumiData"]]] = relationship(
        "BangumiData", backref=backref("kaisai"), innerjoin=True, default=None
    )
