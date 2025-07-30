import polars as pl
from autostore.s3 import S3Backend, S3StorageConfig
from autostore import AutoStore, config, load_dotenv  # noqa: F401

load_dotenv()


def test_conductor():
    AutoStore.register_backend("s3", S3Backend)
    store = AutoStore(
        "s3://arahman22/",
        storage_config=S3StorageConfig(
            profile_name="conductor-notary",
            endpoint_url=config("CONDUCTOR_ENDPOINT_URL"),
        ),
    )
    data: pl.DataFrame = store["weather/thresholds.csv"]

    data["weather/new_threshold.csv"] = data
