import open_publishing


def test_init():
    """Test that library loads correctly."""
    var = open_publishing.assets
    assert var is not None

