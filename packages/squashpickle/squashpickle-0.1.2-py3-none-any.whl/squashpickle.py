"""Module providing a pickle-like interface with compression."""

import gzip
import pickle


def dumps(
    obj,
    protocol=None,
    *,
    fix_imports=True,
    buffer_callback=None,
):
    """Serialise the object and return the result."""
    return gzip.compress(
        pickle.dumps(
            obj,
            protocol=protocol,
            fix_imports=fix_imports,
            buffer_callback=buffer_callback,
        )
    )


def dump(
    obj,
    file,
    protocol=None,
    *,
    fix_imports=True,
    buffer_callback=None,
):
    """Serialise the object to a file."""
    file.write(
        dumps(
            obj,
            protocol=protocol,
            fix_imports=fix_imports,
            buffer_callback=buffer_callback,
        )
    )


def loads(
    data,
    /,
    *,
    fix_imports=True,
    encoding="ASCII",
    errors="strict",
    buffers=(),
):
    """Deserialize the object and return the result."""
    return pickle.loads(
        gzip.decompress(data),
        fix_imports=fix_imports,
        encoding=encoding,
        errors=errors,
        buffers=buffers,
    )


def load(
    file,
    *,
    fix_imports=True,
    encoding="ASCII",
    errors="strict",
    buffers=(),
):
    """Deserialize the object from file and return the result."""
    return loads(
        file.read(),
        fix_imports=fix_imports,
        encoding=encoding,
        errors=errors,
        buffers=buffers,
    )
