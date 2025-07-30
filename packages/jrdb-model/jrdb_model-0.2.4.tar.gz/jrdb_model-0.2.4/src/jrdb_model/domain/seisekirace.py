"""成績レースデータ."""

from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from ..sessioncontroll import db


class SeisekiRaceData(db.Model):
    """成績レースデータ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "seisekirace"
    racekey: Mapped[str] = mapped_column(primary_key=True)
    furlongtime1: Mapped[int] = mapped_column()
    furlongtime2: Mapped[int] = mapped_column()
    furlongtime3: Mapped[int] = mapped_column()
    furlongtime4: Mapped[int] = mapped_column()
    furlongtime5: Mapped[int] = mapped_column()
    furlongtime6: Mapped[int] = mapped_column()
    furlongtime7: Mapped[int] = mapped_column()
    furlongtime8: Mapped[int] = mapped_column()
    furlongtime9: Mapped[int] = mapped_column()
    furlongtime10: Mapped[int] = mapped_column()
    furlongtime11: Mapped[int] = mapped_column()
    furlongtime12: Mapped[int] = mapped_column()
    furlongtime13: Mapped[int] = mapped_column()
    furlongtime14: Mapped[int] = mapped_column()
    furlongtime15: Mapped[int] = mapped_column()
    furlongtime16: Mapped[int] = mapped_column()
    furlongtime17: Mapped[int] = mapped_column()
    furlongtime18: Mapped[int] = mapped_column()
    corner1: Mapped[str] = mapped_column()
    corner2: Mapped[str] = mapped_column()
    corner3: Mapped[str] = mapped_column()
    corner4: Mapped[str] = mapped_column()
    paceupposition: Mapped[int] = mapped_column()
    truckbias1_in: Mapped[str] = mapped_column()
    truckbias1_center: Mapped[str] = mapped_column()
    truckbias1_out: Mapped[str] = mapped_column()
    truckbias2_in: Mapped[str] = mapped_column()
    truckbias2_center: Mapped[str] = mapped_column()
    truckbias2_out: Mapped[str] = mapped_column()
    truckbias_muko_in: Mapped[str] = mapped_column()
    truckbias_muko_center: Mapped[str] = mapped_column()
    truckbias_muko_out: Mapped[str] = mapped_column()
    truckbias3_in: Mapped[str] = mapped_column()
    truckbias3_center: Mapped[str] = mapped_column()
    truckbias3_out: Mapped[str] = mapped_column()
    truckbias4_saiuchi: Mapped[str] = mapped_column()
    truckbias4_in: Mapped[str] = mapped_column()
    truckbias4_center: Mapped[str] = mapped_column()
    truckbias4_out: Mapped[str] = mapped_column()
    truckbias4_oosoto: Mapped[str] = mapped_column()
    truckbias_straight_saiuchi: Mapped[str] = mapped_column()
    truckbias_straight_in: Mapped[str] = mapped_column()
    truckbias_straight_center: Mapped[str] = mapped_column()
    truckbias_straight_out: Mapped[str] = mapped_column()
    truckbias_straight_oosoto: Mapped[str] = mapped_column()
    comment: Mapped[str] = mapped_column(Text)
