import torch
import polars as pl
from autostore.s3 import S3Backend, S3StorageConfig
from autostore import AutoStore, config, load_dotenv, setup_logging  # noqa: F401

load_dotenv()
setup_logging("debug")


def test_conductor():
    AutoStore.register_backend("s3", S3Backend)
    store = AutoStore(
        "s3://arahman22/",
        config=S3StorageConfig(
            profile_name="conductor-notary",
            endpoint_url=config("CONDUCTOR_ENDPOINT_URL"),
        ),
    )

    data: pl.DataFrame = store["weather/thresholds.csv"]

    store["weather/new_threshold.csv"] = data

    assert "weather/thresholds.csv" in store
    del store["weather/new_threshold.csv"]
    assert "weather/new_threshold.csv" not in store

    store.backend.is_directory("weather/cdn_daily_avg")

    df = store["weather/cdn_daily_avg.parquet"]
    metadata = store.get_metadata("weather/cdn_daily_avg.parquet")

    arr = torch.tensor([1, 2, 3, 4, 5])
    store["weather/test/arr.pt"] = arr

    newarr = store["weather/test/arr.pt"]