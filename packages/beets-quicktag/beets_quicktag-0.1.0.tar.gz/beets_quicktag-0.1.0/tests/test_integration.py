import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from beets import ui
from beets.library import Item as BeetsItem

from beetsplug.quicktag import QuickTagPlugin


class TestQuickTagPluginIntegration:
    """Integration tests for the complete QuickTag plugin workflow."""
    
    @pytest.fixture
    def plugin_with_config(self):
        """Create a plugin with test configuration."""
        plugin = QuickTagPlugin()
        plugin.config.set({
            "categories": {
                "genre": ["rock", "pop", "jazz", "electronic"],
                "mood": ["happy", "sad", "energetic", "calm"],
                "rating": ["1", "2", "3", "4", "5"]
            },
            "autoplay_on_track_change": False,
            "autoplay_at_launch": False,
            "autonext_at_track_end": False,
            "autosave_on_quit": False,
            "keep_playing_on_track_change_if_playing": True,
        })
        return plugin

    def test_plugin_with_no_categories_config(self, plugin_with_config, mock_library, beets_items, capsys):
        """Test plugin behavior when no categories are configured."""
        # Clear categories config
        plugin_with_config.config.set({"categories": {}})
        
        # Mock ui.decargs to return empty query
        with patch('beetsplug.quicktag.ui.decargs', return_value=[]):
            with patch.object(mock_library, 'items', return_value=beets_items):
                # This should print error message and return early
                plugin_with_config.run_quicktag(mock_library, None, [])
        
        captured = capsys.readouterr()
        assert "No categories defined" in captured.out
        assert "Example configuration:" in captured.out

    def test_plugin_with_no_items_found(self, plugin_with_config, mock_library, capsys):
        """Test plugin behavior when no items match the query."""
        # Mock ui.decargs to return empty query
        with patch('beetsplug.quicktag.ui.decargs', return_value=[]):
            with patch.object(mock_library, 'items', return_value=[]):
                plugin_with_config.run_quicktag(mock_library, None, [])
        
        captured = capsys.readouterr()
        assert "No tracks found to tag" in captured.out

    @pytest.mark.asyncio
    async def test_complete_tagging_workflow(self, plugin_with_config, mock_library, beets_items):
        """Test a complete tagging workflow using the plugin."""
        
        # Mock the app.run() method to avoid actually starting the TUI
        with patch('beetsplug.quicktag.app.QuickTagApp.run') as mock_run:
            with patch('beetsplug.quicktag.ui.decargs', return_value=[]):
                with patch.object(mock_library, 'items', return_value=beets_items):
                    
                    plugin_with_config.run_quicktag(mock_library, None, [])
                    
                    # Should have created and attempted to run the app
                    mock_run.assert_called_once()

    def test_plugin_extracts_config_correctly(self, plugin_with_config, mock_library, beets_items):
        """Test that plugin correctly extracts all configuration values."""
        
        with patch('beetsplug.quicktag.app.QuickTagApp') as MockApp:
            with patch('beetsplug.quicktag.ui.decargs', return_value=[]):
                with patch.object(mock_library, 'items', return_value=beets_items):
                    
                    plugin_with_config.run_quicktag(mock_library, None, [])
                    
                    # Check that app was created with correct parameters
                    MockApp.assert_called_once()
                    call_args = MockApp.call_args
                    
                    assert call_args[0][0] == mock_library  # lib
                    assert call_args[0][1] == beets_items   # items
                    
                    # Check categories
                    categories = call_args[0][2]
                    expected_categories = [
                        ("genre", ["rock", "pop", "jazz", "electronic"]),
                        ("mood", ["happy", "sad", "energetic", "calm"]),
                        ("rating", ["1", "2", "3", "4", "5"])
                    ]
                    assert categories == expected_categories
                    
                    # Check boolean flags
                    assert call_args[0][3] is False  # autoplay_on_track_change_enabled
                    assert call_args[0][4] is False  # autoplay_at_launch_enabled
                    assert call_args[0][5] is False  # autonext_at_track_end_enabled
                    assert call_args[0][6] is False  # autosave_on_quit_enabled
                    assert call_args[0][7] is True   # keep_playing_on_track_change_if_playing_enabled

    def test_plugin_command_query_processing(self, plugin_with_config, mock_library):
        """Test that plugin correctly processes command line arguments."""
        
        test_args = ["artist:Beatles", "album:Abbey Road"]
        
        with patch('beetsplug.quicktag.app.QuickTagApp') as MockApp:
            with patch('beetsplug.quicktag.ui.decargs', return_value=test_args) as mock_decargs:
                with patch.object(mock_library, 'items', return_value=[]) as mock_items:
                    
                    plugin_with_config.run_quicktag(mock_library, None, ["artist:Beatles", "album:Abbey Road"])
                    
                    # Should decode arguments
                    mock_decargs.assert_called_once_with(["artist:Beatles", "album:Abbey Road"])
                    
                    # Should query library with decoded args
                    mock_items.assert_called_once_with(test_args)

    def test_plugin_with_different_config_values(self, mock_library, beets_items):
        """Test plugin with various configuration combinations."""
        plugin = QuickTagPlugin()
        plugin.config.set({
            "categories": {"test_cat": ["val1", "val2"]},
            "autoplay_on_track_change": True,
            "autoplay_at_launch": True,
            "autonext_at_track_end": True,
            "autosave_on_quit": True,
            "keep_playing_on_track_change_if_playing": False,
        })
        
        with patch('beetsplug.quicktag.app.QuickTagApp') as MockApp:
            with patch('beetsplug.quicktag.ui.decargs', return_value=[]):
                with patch.object(mock_library, 'items', return_value=beets_items):
                    
                    plugin.run_quicktag(mock_library, None, [])
                    
                    call_args = MockApp.call_args
                    
                    # Check all boolean flags are True except the last one
                    assert call_args[0][3] is True   # autoplay_on_track_change_enabled
                    assert call_args[0][4] is True   # autoplay_at_launch_enabled
                    assert call_args[0][5] is True   # autonext_at_track_end_enabled
                    assert call_args[0][6] is True   # autosave_on_quit_enabled
                    assert call_args[0][7] is False  # keep_playing_on_track_change_if_playing_enabled


class TestEndToEndWorkflow:
    """End-to-end workflow tests that test real scenarios with minimal mocking."""
    
    def test_real_beets_item_creation_and_tagging(self, temp_audio_files):
        """Test creating real beets items and simulating tagging operations."""
        
        # Create real beets items
        items = []
        for i, path in enumerate(temp_audio_files):
            item = BeetsItem()
            item.path = path.encode('utf-8')
            item.artist = f"Test Artist {i+1}"
            item.title = f"Test Track {i+1}"
            item.album = f"Test Album {i+1}"
            
            # Add store method to track calls
            item.store = MagicMock()
            items.append(item)
        
        # Test tagging operations
        item = items[0]
        
        # Simulate tagging
        item.genre = "rock"
        item.mood = "energetic"
        item.comments = "Great track!"
        
        # Verify tags are set
        assert item.genre == "rock"
        assert item.mood == "energetic"
        assert item.comments == "Great track!"
        
        # Simulate storing
        item.store()
        item.store.assert_called_once()

    def test_audio_file_path_handling(self, temp_audio_files):
        """Test that audio file paths are handled correctly."""
        
        for path in temp_audio_files:
            # Verify files exist
            assert Path(path).exists()
            
            # Test path encoding/decoding
            item = BeetsItem()
            item.path = path.encode('utf-8')
            
            # Decode path as the app would
            try:
                decoded_path = item.path.decode("utf-8", "surrogateescape")
            except AttributeError:
                decoded_path = item.path
            
            assert decoded_path == path

    @pytest.mark.asyncio
    async def test_app_with_real_items_minimal_mocking(self, temp_audio_files, test_categories):
        """Test the app with real beets items and minimal mocking."""
        from beetsplug.quicktag.app import QuickTagApp
        
        # Create real items
        items = []
        for i, path in enumerate(temp_audio_files):
            item = BeetsItem()
            item.path = path.encode('utf-8')
            item.artist = f"Real Artist {i+1}"
            item.title = f"Real Track {i+1}"
            item.album = f"Real Album {i+1}"
            item.get = lambda key, default=None, self=item: getattr(self, key, default)
            item.store = MagicMock()
            items.append(item)
        
        # Create app with real items
        mock_lib = MagicMock()
        app = QuickTagApp(
            lib=mock_lib,
            items=items,
            categories=test_categories,
            autoplay_on_track_change_enabled=False,
            autoplay_at_launch_enabled=False,
            autonext_at_track_end_enabled=False,
            autosave_on_quit_enabled=False,
            keep_playing_on_track_change_if_playing=True,
        )
        
        # Test basic app functionality
        assert app.items == items
        assert app.current_item_index == 0
        assert app.item == items[0]
        
        # Test navigation
        await app._navigate(app.NavigateDirection.FORWARD)
        assert app.current_item_index == 1
        assert app.item == items[1]
        
        await app._navigate(app.NavigateDirection.BACKWARD)
        assert app.current_item_index == 0
        assert app.item == items[0]

    def test_category_validation(self):
        """Test category configuration validation."""
        plugin = QuickTagPlugin()
        
        # Test valid categories
        valid_config = {
            "categories": {
                "genre": ["rock", "pop"],
                "mood": ["happy", "sad"]
            }
        }
        plugin.config.set(valid_config)
        categories_config = plugin.config["categories"].get(dict)
        
        assert "genre" in categories_config
        assert "mood" in categories_config
        assert categories_config["genre"] == ["rock", "pop"]
        assert categories_config["mood"] == ["happy", "sad"]
        
        # Convert to format used by app
        categories = list(categories_config.items())
        expected = [
            ("genre", ["rock", "pop"]),
            ("mood", ["happy", "sad"])
        ]
        assert categories == expected

    def test_file_path_edge_cases(self):
        """Test handling of various file path edge cases."""
        
        test_paths = [
            "/normal/path/file.mp3",
            "/path with spaces/file.mp3",
            "/path/with/unicode/файл.mp3",
            "/path/with/symbols/file-name_123.mp3",
        ]
        
        for path_str in test_paths:
            item = BeetsItem()
            item.path = path_str.encode('utf-8')
            
            # Test the decoding logic from the app
            try:
                decoded = item.path.decode("utf-8", "surrogateescape")
            except AttributeError:
                decoded = item.path
            
            assert decoded == path_str 