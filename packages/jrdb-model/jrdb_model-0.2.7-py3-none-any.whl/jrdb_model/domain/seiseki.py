"""成績データ."""

from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from ..sessioncontroll import db
from .seisekirace import SeisekiRaceData


class SeisekiData(db.Model):
    """成績データ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "seiseki"
    racehorsekey: Mapped[str] = mapped_column(
        String(255), ForeignKey("racehorse.racehorsekey"), primary_key=True
    )
    racekey: Mapped[str] = mapped_column(String(255), ForeignKey("seisekirace.racekey"))
    bacode: Mapped[int] = mapped_column()
    year: Mapped[int] = mapped_column()
    kai: Mapped[int] = mapped_column()
    day: Mapped[str] = mapped_column(String(255))
    raceno: Mapped[int] = mapped_column()
    num: Mapped[int] = mapped_column()
    raceseisekikey: Mapped[str] = mapped_column(String(255))
    blood: Mapped[int] = mapped_column()
    ymd: Mapped[str] = mapped_column(String(255))
    horse: Mapped[str] = mapped_column(String(255))
    distance: Mapped[int] = mapped_column()
    tdscode: Mapped[int] = mapped_column()
    right_left: Mapped[int] = mapped_column()
    in_out: Mapped[int] = mapped_column()
    baba: Mapped[int] = mapped_column()
    baba_abst: Mapped[int] = mapped_column()
    baba_detail: Mapped[int] = mapped_column()
    shubetsu: Mapped[int] = mapped_column()
    joken: Mapped[str] = mapped_column(String(255))
    kigo: Mapped[int] = mapped_column()
    juryo: Mapped[int] = mapped_column()
    grade: Mapped[int] = mapped_column()
    racename: Mapped[str] = mapped_column(String(255))
    num_of_all_horse: Mapped[int] = mapped_column()
    racename_ryaku: Mapped[str] = mapped_column(String(255))
    order_of_arrival: Mapped[int] = mapped_column()
    ijo_kbn: Mapped[int] = mapped_column()
    time: Mapped[int] = mapped_column()
    kinryo: Mapped[int] = mapped_column()
    jockey_name: Mapped[str] = mapped_column(String(255))
    trainer_name: Mapped[str] = mapped_column(String(255))
    decided_odds: Mapped[float] = mapped_column()
    decided_pop_order: Mapped[int] = mapped_column()
    idm: Mapped[int] = mapped_column()
    natural_score: Mapped[int] = mapped_column()
    baba_sa: Mapped[int] = mapped_column()
    pace: Mapped[int] = mapped_column()
    start_late: Mapped[int] = mapped_column()
    position: Mapped[int] = mapped_column()
    furi: Mapped[int] = mapped_column()
    mae_furi: Mapped[int] = mapped_column()
    naka_furi: Mapped[int] = mapped_column()
    ushiro_furi: Mapped[int] = mapped_column()
    race: Mapped[int] = mapped_column()
    course_position: Mapped[int] = mapped_column()
    up_code: Mapped[int] = mapped_column()
    class_code: Mapped[int] = mapped_column()
    batai_code: Mapped[int] = mapped_column()
    kehai_code: Mapped[int] = mapped_column()
    racepace: Mapped[str] = mapped_column(String(255))
    umapace: Mapped[str] = mapped_column(String(255))
    ten_score: Mapped[float] = mapped_column()
    up_score: Mapped[float] = mapped_column()
    pace_score: Mapped[float] = mapped_column()
    racep_score: Mapped[float] = mapped_column()
    win_horse_name: Mapped[str] = mapped_column(String(255))
    time_sa: Mapped[int] = mapped_column()
    mae3f_time: Mapped[int] = mapped_column()
    agari3f_time: Mapped[int] = mapped_column()
    biko: Mapped[str] = mapped_column(String(255))
    yobi: Mapped[str] = mapped_column(String(255))
    decided_place_odds: Mapped[float] = mapped_column()
    juji_win_odds: Mapped[float] = mapped_column()
    juji_place_odds: Mapped[float] = mapped_column()
    corner_order1: Mapped[int] = mapped_column()
    corner_order2: Mapped[int] = mapped_column()
    corner_order3: Mapped[int] = mapped_column()
    corner_order4: Mapped[int] = mapped_column()
    mae3f_sa: Mapped[int] = mapped_column()
    agari3f_sa: Mapped[int] = mapped_column()
    jockey_code: Mapped[int] = mapped_column()
    trainer_code: Mapped[int] = mapped_column()
    weight: Mapped[int] = mapped_column()
    weight_increase: Mapped[int] = mapped_column()
    tenko: Mapped[int] = mapped_column()
    course: Mapped[int] = mapped_column()
    race_leg_type: Mapped[str] = mapped_column(String(255))
    win_ret: Mapped[int] = mapped_column()
    place_ret: Mapped[int] = mapped_column()
    this_money: Mapped[int] = mapped_column()
    earned_money: Mapped[int] = mapped_column()
    race_pace_flow: Mapped[int] = mapped_column()
    horse_pace_flow: Mapped[int] = mapped_column()
    corner4_course_position: Mapped[int] = mapped_column()

    seisekirace: Mapped[Optional["SeisekiRaceData"]] = relationship(
        "SeisekiRaceData", uselist=False, backref=backref("seiseki"), default=None
    )
