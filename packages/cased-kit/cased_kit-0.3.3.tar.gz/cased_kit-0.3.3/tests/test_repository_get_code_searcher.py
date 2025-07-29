import tempfile
from pathlib import Path

from kit import CodeSearcher, Repository


def test_get_code_searcher_returns_bound_instance():
    """Ensure that Repository.get_code_searcher() returns the internal CodeSearcher and it works."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_root = Path(tmpdir)
        # Create a simple file so the searcher has something to find
        (repo_root / "hello.py").write_text("print('hello world')\n")

        repo = Repository(str(repo_root))
        searcher = repo.get_code_searcher()

        # The returned object should be a CodeSearcher instance
        assert isinstance(searcher, CodeSearcher)

        # It should point at the same repository path
        assert Path(searcher.repo_path) == repo_root

        # And basic search should work
        matches = searcher.search_text("hello world")
        assert any("hello world" in m["line"] for m in matches) 