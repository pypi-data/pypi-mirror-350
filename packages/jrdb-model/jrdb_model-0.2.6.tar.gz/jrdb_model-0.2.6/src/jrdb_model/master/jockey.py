"""騎手データ."""

from sqlalchemy.orm import Mapped, mapped_column

from ..sessioncontroll import db


class JockeyData(db.Model):
    """騎手データ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "jockey"
    jockey_code: Mapped[int] = mapped_column(primary_key=True)
    delete_flg: Mapped[int] = mapped_column()
    delete_ymd: Mapped[int] = mapped_column()
    jockey_name: Mapped[str] = mapped_column()
    jockey_name_kana: Mapped[str] = mapped_column()
    jockey_name_short: Mapped[str] = mapped_column()
    shozoku_code: Mapped[int] = mapped_column()
    shozoku_region: Mapped[str] = mapped_column()
    birthday: Mapped[int] = mapped_column()
    get_licence_year: Mapped[int] = mapped_column()
    minarai_kbn: Mapped[int] = mapped_column()
    trainer_code: Mapped[int] = mapped_column()
    jockey_comment: Mapped[str] = mapped_column()
    comment_ymd: Mapped[int] = mapped_column()
    this_leading: Mapped[int] = mapped_column()
    this_flat_seiseki_1st: Mapped[int] = mapped_column()
    this_flat_seiseki_2nd: Mapped[int] = mapped_column()
    this_flat_seiseki_3rd: Mapped[int] = mapped_column()
    this_flat_seiseki_out: Mapped[int] = mapped_column()
    this_steeple_seiseki_1st: Mapped[int] = mapped_column()
    this_steeple_seiseki_2nd: Mapped[int] = mapped_column()
    this_steeple_seiseki_3rd: Mapped[int] = mapped_column()
    this_steeple_seiseki_out: Mapped[int] = mapped_column()
    this_tokubetsu_win: Mapped[int] = mapped_column()
    this_jusho_win: Mapped[int] = mapped_column()
    last_leading: Mapped[int] = mapped_column()
    last_flat_seiseki_1st: Mapped[int] = mapped_column()
    last_flat_seiseki_2nd: Mapped[int] = mapped_column()
    last_flat_seiseki_3rd: Mapped[int] = mapped_column()
    last_flat_seiseki_out: Mapped[int] = mapped_column()
    last_steeple_seiseki_1st: Mapped[int] = mapped_column()
    last_steeple_seiseki_2nd: Mapped[int] = mapped_column()
    last_steeple_seiseki_3rd: Mapped[int] = mapped_column()
    last_steeple_seiseki_out: Mapped[int] = mapped_column()
    last_tokubetsu_win: Mapped[int] = mapped_column()
    last_jusho_win: Mapped[int] = mapped_column()
    total_flat_seiseki_1st: Mapped[int] = mapped_column()
    total_flat_seiseki_2nd: Mapped[int] = mapped_column()
    total_flat_seiseki_3rd: Mapped[int] = mapped_column()
    total_flat_seiseki_out: Mapped[int] = mapped_column()
    total_steeple_seiseki_1st: Mapped[int] = mapped_column()
    total_steeple_seiseki_2nd: Mapped[int] = mapped_column()
    total_steeple_seiseki_3rd: Mapped[int] = mapped_column()
    total_steeple_seiseki_out: Mapped[int] = mapped_column()
    data_ymd: Mapped[int] = mapped_column()
