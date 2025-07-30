"""レースデータ."""

from typing import List, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from ..sessioncontroll import db
from .predict_race import PredictRaceData
from .racehorse import RacehorseData
from .returninfo import ReturninfoData
from .umaren_odds import UmarenOddsData
from .wakuren_odds import WakurenOddsData
from .wide_odds import WideOddsData


class BangumiData(db.Model):
    """レースデータ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "bangumi"
    racekey: Mapped[str] = mapped_column(String(255), primary_key=True)
    # 親に対して
    kaisaikey: Mapped[str] = mapped_column(String(255), ForeignKey("kaisai.kaisaikey"))
    ymd: Mapped[str] = mapped_column(String(255))
    start_time: Mapped[str] = mapped_column(String(255))
    distance: Mapped[int] = mapped_column()
    tdscode: Mapped[int] = mapped_column()
    right_left: Mapped[int] = mapped_column()
    in_out: Mapped[int] = mapped_column()
    shubetsu: Mapped[int] = mapped_column()
    joken: Mapped[str] = mapped_column(String(255))
    kigo: Mapped[int] = mapped_column()
    horse_kind_joken: Mapped[int] = mapped_column()
    horse_sex_joken: Mapped[int] = mapped_column()
    inter_race_joken: Mapped[int] = mapped_column()
    juryo: Mapped[int] = mapped_column()
    grade: Mapped[int] = mapped_column()
    race_name: Mapped[str] = mapped_column(String(255))
    kai: Mapped[str] = mapped_column(String(255))
    num_of_all_horse: Mapped[int] = mapped_column()
    course: Mapped[int] = mapped_column()
    kaisai_kbn: Mapped[int] = mapped_column()
    race_name_short: Mapped[str] = mapped_column(String(255))
    race_name_9char: Mapped[str] = mapped_column(String(255))
    data_kbn: Mapped[int] = mapped_column()
    money1st: Mapped[int] = mapped_column()
    money2nd: Mapped[int] = mapped_column()
    money3rd: Mapped[int] = mapped_column()
    money4th: Mapped[int] = mapped_column()
    money5th: Mapped[int] = mapped_column()
    sannyu_money1st: Mapped[int] = mapped_column()
    sannyu_money2nd: Mapped[int] = mapped_column()
    sellflg_tansho: Mapped[int] = mapped_column()
    sellflg_fukusho: Mapped[int] = mapped_column()
    sellflg_wakuren: Mapped[int] = mapped_column()
    sellflg_umaren: Mapped[int] = mapped_column()
    sellflg_umatan: Mapped[int] = mapped_column()
    sellflg_wide: Mapped[int] = mapped_column()
    sellflg_sanrenpuku: Mapped[int] = mapped_column()
    sellflg_sanrentan: Mapped[int] = mapped_column()
    yobi: Mapped[int] = mapped_column()
    win5flg: Mapped[int] = mapped_column()

    # 子に対して
    racehorses: Mapped[Optional[List["RacehorseData"]]] = relationship(
        "RacehorseData",
        backref=backref("bangumi"),
        innerjoin=True,
        default_factory=list,
    )

    # 1:1
    returninfo: Mapped[Optional["ReturninfoData"]] = relationship(
        "ReturninfoData", uselist=False, backref=backref("bangumi"), default=None
    )
    umaren_odds: Mapped[Optional["UmarenOddsData"]] = relationship(
        "UmarenOddsData", uselist=False, backref=backref("bangumi"), default=None
    )
    wide_odds: Mapped[Optional["WideOddsData"]] = relationship(
        "WideOddsData", uselist=False, backref=backref("bangumi"), default=None
    )
    wakuren_odds: Mapped[Optional["WakurenOddsData"]] = relationship(
        "WakurenOddsData", uselist=False, backref=backref("bangumi"), default=None
    )
    predict_race: Mapped[Optional["PredictRaceData"]] = relationship(
        "PredictRaceData", uselist=False, backref=backref("bangumi"), default=None
    )
