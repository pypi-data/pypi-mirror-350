"""競走馬データ."""

from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, backref, mapped_column, relationship

from ..master.horsebase import HorsebaseData
from ..sessioncontroll import db
from .calculated_score import CalculatedScoreData
from .predict import PredictData
from .seiseki import SeisekiData
from .trainanalysis import TrainAnalysisData
from .trainoikiri import TrainOikiriData


class RacehorseData(db.Model):
    """競走馬データ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "racehorse"
    __table_args__ = {"mariadb_row_format": "DYNAMIC"}
    racehorsekey: Mapped[str] = mapped_column(String(255), primary_key=True)
    # 親に対して
    racekey: Mapped[str] = mapped_column(String(255), ForeignKey("bangumi.racekey"))
    bacode: Mapped[int] = mapped_column()
    year: Mapped[int] = mapped_column()
    kai: Mapped[int] = mapped_column()
    day: Mapped[str] = mapped_column(String(255))
    race: Mapped[int] = mapped_column()
    num: Mapped[int] = mapped_column()
    blood: Mapped[int] = mapped_column(ForeignKey("horsebase.blood"))
    horse: Mapped[str] = mapped_column(String(255))
    idm: Mapped[float] = mapped_column()
    jockey_score: Mapped[float] = mapped_column()
    info_score: Mapped[float] = mapped_column()
    yobi1: Mapped[str] = mapped_column(String(255))
    yobi2: Mapped[str] = mapped_column(String(255))
    yobi3: Mapped[str] = mapped_column(String(255))
    sogo_score: Mapped[float] = mapped_column()
    leg_type: Mapped[int] = mapped_column()
    distance_adjust: Mapped[int] = mapped_column()
    up_degree: Mapped[int] = mapped_column()
    routin: Mapped[int] = mapped_column()
    cri_odds: Mapped[float] = mapped_column()
    cri_popular_order: Mapped[int] = mapped_column()
    cri_fukusho_odds: Mapped[float] = mapped_column()
    cri_fukusho_popluar_order: Mapped[int] = mapped_column()
    specific_info_1: Mapped[int] = mapped_column()
    specific_info_2: Mapped[int] = mapped_column()
    specific_info_3: Mapped[int] = mapped_column()
    specific_info_4: Mapped[int] = mapped_column()
    specific_info_5: Mapped[int] = mapped_column()
    sogo_info_1: Mapped[int] = mapped_column()
    sogo_info_2: Mapped[int] = mapped_column()
    sogo_info_3: Mapped[int] = mapped_column()
    sogo_info_4: Mapped[int] = mapped_column()
    sogo_info_5: Mapped[int] = mapped_column()
    pop_score: Mapped[float] = mapped_column()
    train_score: Mapped[float] = mapped_column()
    trainer_score: Mapped[float] = mapped_column()
    train_code: Mapped[int] = mapped_column()
    trainer_hyoka_code: Mapped[int] = mapped_column()
    jockey_rate_rentai: Mapped[float] = mapped_column()
    gekiso_score: Mapped[float] = mapped_column()
    hidume_code: Mapped[int] = mapped_column()
    hidume_shape: Mapped[int] = mapped_column()
    hidume_size: Mapped[int] = mapped_column()
    omotekisei_code: Mapped[int] = mapped_column()
    class_code: Mapped[int] = mapped_column()
    yobi4: Mapped[str] = mapped_column(String(255))
    brinkers: Mapped[str] = mapped_column(String(255))
    jockey_name: Mapped[str] = mapped_column(String(255))
    kinryo: Mapped[int] = mapped_column()
    minarai: Mapped[int] = mapped_column()
    trainer_name: Mapped[str] = mapped_column(String(255))
    trainer_shozoku: Mapped[str] = mapped_column(String(255))
    zenso_seiseki_key_1: Mapped[str] = mapped_column(String(255))
    zenso_seiseki_key_2: Mapped[str] = mapped_column(String(255))
    zenso_seiseki_key_3: Mapped[str] = mapped_column(String(255))
    zenso_seiseki_key_4: Mapped[str] = mapped_column(String(255))
    zenso_seiseki_key_5: Mapped[str] = mapped_column(String(255))
    zenso_racekey_1: Mapped[str] = mapped_column(String(255))
    zenso_racekey_2: Mapped[str] = mapped_column(String(255))
    zenso_racekey_3: Mapped[str] = mapped_column(String(255))
    zenso_racekey_4: Mapped[str] = mapped_column(String(255))
    zenso_racekey_5: Mapped[str] = mapped_column(String(255))
    waku: Mapped[int] = mapped_column()
    yobi5: Mapped[str] = mapped_column(String(255))
    sogo_shirushi: Mapped[int] = mapped_column()
    idm_shiruishi: Mapped[int] = mapped_column()
    info_shirushi: Mapped[int] = mapped_column()
    jockey_shirushi: Mapped[int] = mapped_column()
    trainer_shirushi: Mapped[int] = mapped_column()
    train_shirushi: Mapped[int] = mapped_column()
    gekiso_shirushi: Mapped[int] = mapped_column()
    turf_adjust_code: Mapped[int] = mapped_column()
    dart_adjust_code: Mapped[int] = mapped_column()
    jockey_code: Mapped[int] = mapped_column()
    trainer_code: Mapped[int] = mapped_column()
    yobi6: Mapped[str] = mapped_column(String(255))
    kakutoku_money: Mapped[int] = mapped_column()
    shukaku_money: Mapped[int] = mapped_column()
    joken: Mapped[int] = mapped_column()
    ten_score: Mapped[float] = mapped_column()
    pace_score: Mapped[float] = mapped_column()
    up_score: Mapped[float] = mapped_column()
    position_score: Mapped[float] = mapped_column()
    pace_predict: Mapped[str] = mapped_column(String(255))
    dochu_order: Mapped[int] = mapped_column()
    dochu_sa: Mapped[int] = mapped_column()
    dochu_in_out: Mapped[int] = mapped_column()
    last_order: Mapped[int] = mapped_column()
    last_sa: Mapped[int] = mapped_column()
    last_in_out: Mapped[int] = mapped_column()
    order: Mapped[int] = mapped_column()
    sa: Mapped[int] = mapped_column()
    in_out: Mapped[int] = mapped_column()
    tenkai: Mapped[str] = mapped_column(String(255))
    distance_adjust2: Mapped[int] = mapped_column()
    commit_weight: Mapped[int] = mapped_column()
    commit_weight_increase: Mapped[int] = mapped_column()
    torikeshi: Mapped[int] = mapped_column()
    sex: Mapped[int] = mapped_column()
    owner_name: Mapped[str] = mapped_column(String(255))
    banushikai_code: Mapped[int] = mapped_column()
    umakigo_code: Mapped[int] = mapped_column()
    gekiso_order: Mapped[int] = mapped_column()
    ls_score_order: Mapped[int] = mapped_column()
    ten_score_order: Mapped[int] = mapped_column()
    pace_score_order: Mapped[int] = mapped_column()
    up_score_order: Mapped[int] = mapped_column()
    position_score_order: Mapped[int] = mapped_column()
    expect_jokey_win_rate: Mapped[float] = mapped_column()
    expect_jokey_rentai_rate: Mapped[float] = mapped_column()
    yuso: Mapped[str] = mapped_column(String(255))
    soho: Mapped[int] = mapped_column()
    taikei_data: Mapped[str] = mapped_column(String(255))
    taikei: Mapped[int] = mapped_column()
    senaka: Mapped[int] = mapped_column()
    do: Mapped[int] = mapped_column()
    siri: Mapped[int] = mapped_column()
    tomo: Mapped[int] = mapped_column()
    harabukuro: Mapped[int] = mapped_column()
    head: Mapped[int] = mapped_column()
    neck: Mapped[int] = mapped_column()
    breast: Mapped[int] = mapped_column()
    shoulder: Mapped[int] = mapped_column()
    zencho: Mapped[int] = mapped_column()
    kocho: Mapped[int] = mapped_column()
    maehaba: Mapped[int] = mapped_column()
    ushirohaba: Mapped[int] = mapped_column()
    maetsunagi: Mapped[int] = mapped_column()
    ushirotsunagi: Mapped[int] = mapped_column()
    tail: Mapped[int] = mapped_column()
    furikata: Mapped[int] = mapped_column()
    taikei_sogo1: Mapped[int] = mapped_column()
    taikei_sogo2: Mapped[int] = mapped_column()
    taikei_sogo3: Mapped[int] = mapped_column()
    umatokki1: Mapped[int] = mapped_column()
    umatokki2: Mapped[int] = mapped_column()
    umatokki3: Mapped[int] = mapped_column()
    horse_start_score: Mapped[float] = mapped_column()
    horse_latestart_rate: Mapped[float] = mapped_column()
    sanko_zenso: Mapped[int] = mapped_column()
    sanko_zenso_jockey_code: Mapped[str] = mapped_column(String(255))
    mambaken_score: Mapped[float] = mapped_column()
    mambaken_shirushi: Mapped[int] = mapped_column()
    kokyu_flg: Mapped[int] = mapped_column()
    gekiso_type: Mapped[str] = mapped_column(String(255))
    rest_reason_code: Mapped[int] = mapped_column()
    flg: Mapped[str] = mapped_column(String(255))
    turf_dart_steeple_flg: Mapped[int] = mapped_column()
    distance_flg: Mapped[int] = mapped_column()
    class_flg: Mapped[int] = mapped_column()
    tenkyu_flg: Mapped[int] = mapped_column()
    kyosei_flg: Mapped[int] = mapped_column()
    norikae_flg: Mapped[int] = mapped_column()
    runtimes_first_train: Mapped[int] = mapped_column()
    date_first_train: Mapped[int] = mapped_column()
    days_after_first_train: Mapped[int] = mapped_column()
    hobokusaki: Mapped[str] = mapped_column(String(255))
    hobokusaki_rank: Mapped[str] = mapped_column(String(255))
    trainer_rank: Mapped[int] = mapped_column()

    # 1:1
    trainanalysis: Mapped[Optional["TrainAnalysisData"]] = relationship(
        "TrainAnalysisData",
        uselist=False,
        backref=backref("racehorse"),
        innerjoin=True,
        default=None,
    )
    trainoikiri: Mapped[Optional["TrainOikiriData"]] = relationship(
        "TrainOikiriData",
        uselist=False,
        backref=backref("racehorse"),
        innerjoin=True,
        default=None,
    )
    horse_base: Mapped[Optional["HorsebaseData"]] = relationship(
        "HorsebaseData",
        uselist=False,
        backref=backref("racehorse"),
        innerjoin=True,
        default=None,
    )
    result: Mapped[Optional["SeisekiData"]] = relationship(
        "SeisekiData",
        uselist=False,
        backref=backref("racehorse"),
        innerjoin=False,
        default=None,
    )
    predict: Mapped[Optional["PredictData"]] = relationship(
        "PredictData",
        uselist=False,
        backref=backref("racehorse"),
        innerjoin=False,
        default=None,
    )
    calculated_score: Mapped[Optional["CalculatedScoreData"]] = relationship(
        "CalculatedScoreData",
        uselist=False,
        backref=backref("racehorse"),
        innerjoin=False,
        default=None,
    )
