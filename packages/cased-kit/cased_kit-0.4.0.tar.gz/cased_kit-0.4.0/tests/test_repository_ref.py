"""Tests for Repository ref parameter functionality."""

import pytest
import tempfile
import subprocess
import shutil
from pathlib import Path
from kit import Repository


class TestRepositoryRef:
    """Test ref parameter functionality."""

    def test_repository_stores_ref(self):
        """Test that Repository stores the ref parameter."""
        repo = Repository(".", ref="main")
        assert repo.ref == "main"

    def test_repository_no_ref(self):
        """Test that Repository works without ref parameter."""
        repo = Repository(".")
        assert repo.ref is None

    def test_git_metadata_properties(self):
        """Test that git metadata properties work."""
        repo = Repository(".")
        
        # These should all be strings or None
        assert isinstance(repo.current_sha, str) or repo.current_sha is None
        assert isinstance(repo.current_sha_short, str) or repo.current_sha_short is None
        assert isinstance(repo.current_branch, str) or repo.current_branch is None
        assert isinstance(repo.remote_url, str) or repo.remote_url is None
        
        # In this repo, we should have some git metadata
        assert repo.current_sha is not None
        assert len(repo.current_sha) == 40  # Full SHA
        assert repo.current_sha_short is not None
        assert len(repo.current_sha_short) == 7  # Short SHA
        
    def test_git_metadata_consistency(self):
        """Test that git metadata is consistent."""
        repo = Repository(".")
        
        if repo.current_sha and repo.current_sha_short:
            assert repo.current_sha.startswith(repo.current_sha_short)

    def test_invalid_ref_error(self):
        """Test that invalid refs raise appropriate errors."""
        with pytest.raises(ValueError, match="Failed to checkout ref"):
            Repository(".", ref="nonexistent-ref-12345")

    def test_checkout_ref_with_local_repo(self):
        """Test checking out a specific ref in a local repository."""
        # This test runs on the current repo, so we can test checking out main
        repo = Repository(".", ref="main")
        assert repo.ref == "main"
        # Should be able to get git metadata
        assert repo.current_sha is not None
        
    def test_git_metadata_with_non_git_repo(self):
        """Test git metadata properties with non-git repository."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a non-git directory
            test_file = Path(temp_dir) / "test.py"
            test_file.write_text("def hello(): pass")
            
            repo = Repository(temp_dir)
            
            # All git metadata should be None for non-git repos
            assert repo.current_sha is None
            assert repo.current_sha_short is None
            assert repo.current_branch is None
            assert repo.remote_url is None

    def test_ref_with_non_git_repo_error(self):
        """Test that using ref with non-git repo raises error."""
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test.py"
            test_file.write_text("def hello(): pass")
            
            with pytest.raises(ValueError, match="not a git repository"):
                Repository(temp_dir, ref="main")

    def test_github_token_parameter(self):
        """Test that github_token parameter is properly stored and passed."""
        # We can't test actual GitHub cloning without credentials,
        # but we can test that the parameter is accepted
        repo = Repository(".", github_token="fake-token")
        assert repo.ref is None  # No ref specified
        
    def test_multiple_repository_instances(self):
        """Test that multiple Repository instances work independently."""
        repo1 = Repository(".", ref="main")
        repo2 = Repository(".")
        
        assert repo1.ref == "main"
        assert repo2.ref is None
        
        # Both should be able to access git metadata
        assert repo1.current_sha is not None
        assert repo2.current_sha is not None
        # Should be the same SHA since both point to same repo
        assert repo1.current_sha == repo2.current_sha 