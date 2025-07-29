def test_author_dunder_attr(package) -> None:
    """Verifies that the package has a __author__ attribute."""

    assert hasattr(package, '__author__')


def test_doc_dunder_attr(package) -> None:
    """Verifies that the package has a __doc__ attribute."""

    assert hasattr(package, '__doc__')


def test_version_dunder_attr(package) -> None:
    """Verifies that the package has a __version__ attribute."""

    assert hasattr(package, '__version__')
