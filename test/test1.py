from dependency_fetcher.core import fetch_dependencies

def test_fetch_dependencies():
    fetch_dependencies(".", False, False)
    assert "requirements.txt" in os.listdir(".")
