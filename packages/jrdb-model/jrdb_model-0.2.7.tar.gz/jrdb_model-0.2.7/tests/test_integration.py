"""DBと接続する統合テスト."""


def test_kaisai():
    """開催データのジョインロードのテスト."""
    import os
    from typing import List

    from sqlalchemy.orm import joinedload

    from jrdb_model import KaisaiData, create_app

    os.environ["DB"] = (
        "mariadb+pymysql://astroripple:S#tonoprime0407@sazanami-db/astroripple"
    )
    app = create_app()
    kaisais: List[KaisaiData]
    with app.app_context():
        kaisais = (
            KaisaiData.query.filter(
                KaisaiData.ymd >= 20220101, KaisaiData.ymd <= 20220130
            )
            .options(joinedload("*"))
            .all()
        )
    assert len(kaisais) == 26
    assert kaisais[0].races[0].racehorses[0].result.order_of_arrival == 4
