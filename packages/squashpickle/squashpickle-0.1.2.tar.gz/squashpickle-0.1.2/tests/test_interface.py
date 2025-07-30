"""Tests against the user-facing functionality."""

import pickle
from inspect import signature
from pathlib import Path

from squashpickle import dump, dumps, load, loads


def test_dumps_dict_compression():
    """Trivial test to ensure the compression is occurring."""
    test_data = _generate_dictionary_object(1000)
    # Compare result against a dump with pickle directly.
    compressed, uncompressed = _compression_rate(test_data)
    # Check for byte compression
    assert compressed / uncompressed < 0.6


def test_loads_compressed_string():
    """Trivial test to ensure the compressed binary can be loaded."""
    compressed_string = (
        b"\x1f\x8b\x08\x00W+\xeef\x02\xffk`\x99\xca\xc1\x00\x01=,%"
        b"\xa9\xc5%S\xf4\x00,i\xe2\xb3\x13\x00\x00\x00"
    )
    assert loads(compressed_string) == "test"


def test_dump_to_file_and_load_back(tmp_path: Path):
    """Check the round-trip with file-io."""
    test_data = _generate_dictionary_object(100)
    pickle_path = tmp_path.joinpath("test.pkl")
    with pickle_path.open("wb") as f:
        dump(test_data, f)
    # Check the file was created.
    assert pickle_path.exists() and pickle_path.is_file()
    with pickle_path.open("rb") as f:
        loaded_data = load(f)
    # Check the loaded data matches what we put
    assert loaded_data == test_data


def test_dumps_signature_match():
    """Confirm our dumps interface matches pickle."""
    assert signature(pickle.dumps) == signature(dumps)


def test_loads_signature_match():
    """Confirm our loads interface matches pickle."""
    assert signature(pickle.loads) == signature(loads)


def test_dump_signature_match():
    """Confirm our dump interface matches pickle."""
    assert signature(pickle.dump) == signature(dump)


def test_load_signature_match():
    """Confirm our load interface matches pickle."""
    assert signature(pickle.load) == signature(load)


def _generate_dictionary_object(length: int) -> dict[int, str]:
    return {i: str(i) for i in range(length)}


def _compression_rate(test_data) -> tuple[int, int]:
    compressed_bytes = dumps(test_data)
    uncompressed_bytes = pickle.dumps(test_data)
    # Check the compression rate seems normal ~51%
    return len(compressed_bytes), len(uncompressed_bytes)
