from autostore import AutoStore


def test_json():
    data = {"company": "Test Company", "employees": 100}
    store = AutoStore("./tmp")
    store["test/company"] = data
    assert store["test/company"] == data
    assert "test/company" in store


def test_parquet():
    import polars as pl
    df = pl.DataFrame({
        "name": ["Alice", "Bob", "Charlie"],
        "age": [25, 30, 35],
        "city": ["New York", "Los Angeles", "Chicago"]
    })
    store = AutoStore("./tmp")
    store["test/people"] = df
    assert "test/people" in store