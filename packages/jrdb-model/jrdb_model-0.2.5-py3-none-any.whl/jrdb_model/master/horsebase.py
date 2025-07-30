"""馬基本データ."""

from sqlalchemy.orm import Mapped, mapped_column

from ..sessioncontroll import db


class HorsebaseData(db.Model):
    """馬基本データ.

    Args:
        db (_type_): _description_

    """

    __tablename__ = "horsebase"
    blood: Mapped[int] = mapped_column(primary_key=True)
    horse: Mapped[str] = mapped_column()
    sex: Mapped[int] = mapped_column()
    hair: Mapped[int] = mapped_column()
    umakigo: Mapped[int] = mapped_column()
    father: Mapped[str] = mapped_column()
    mother: Mapped[str] = mapped_column()
    mother_father: Mapped[str] = mapped_column()
    birthday: Mapped[int] = mapped_column()
    father_birthyear: Mapped[int] = mapped_column()
    mother_birthyear: Mapped[int] = mapped_column()
    mother_father_birthyear: Mapped[int] = mapped_column()
    owner: Mapped[str] = mapped_column()
    owner_kai_code: Mapped[int] = mapped_column()
    producer: Mapped[str] = mapped_column()
    locality: Mapped[str] = mapped_column()
    delete_flg: Mapped[int] = mapped_column()
    data_ymd: Mapped[int] = mapped_column()
    father_phylogeny: Mapped[int] = mapped_column()
    mother_phylogeny: Mapped[int] = mapped_column()
