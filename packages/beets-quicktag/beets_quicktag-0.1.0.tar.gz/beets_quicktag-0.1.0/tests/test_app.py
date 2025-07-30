import pytest
from unittest.mock import MagicMock, patch
from textual.widgets import SelectionList, Static

from beetsplug.quicktag.app import QuickTagApp, NavigateDirection, HeaderWidget
from beetsplug.quicktag.widgets.custom_selection_list import CustomSelectionList
from beetsplug.quicktag.widgets.input_with_label import InputWithLabel


class TestNavigateDirection:
    """Test the NavigateDirection enum."""
    
    def test_enum_values(self):
        """Test that enum values are correct."""
        assert NavigateDirection.FORWARD.value == 1
        assert NavigateDirection.BACKWARD.value == -1


class TestHeaderWidget:
    """Test the HeaderWidget component."""
    
    def test_initialization(self):
        """Test HeaderWidget initialization."""
        from beetsplug.quicktag.widgets.playback import PlaybackWidget
        
        playback_widget = PlaybackWidget()
        header = HeaderWidget(playback_widget=playback_widget)
        
        assert header.playback_widget == playback_widget
        assert header.item is None

    def test_initialization_with_item(self, beets_items):
        """Test HeaderWidget initialization with an item."""
        from beetsplug.quicktag.widgets.playback import PlaybackWidget
        
        playback_widget = PlaybackWidget()
        header = HeaderWidget(playback_widget=playback_widget, item=beets_items[0])
        
        assert header.item == beets_items[0]

    @pytest.mark.asyncio
    async def test_header_update(self, beets_items):
        """Test header text updates."""
        from textual.app import App
        from beetsplug.quicktag.widgets.playback import PlaybackWidget
        
        class TestApp(App):
            def compose(self):
                playback_widget = PlaybackWidget()
                yield HeaderWidget(playback_widget=playback_widget, id="test-header")
        
        app = TestApp()
        async with app.run_test() as pilot:
            header = app.query_one("#test-header", HeaderWidget)
            
            # Test default header
            header.update_header()
            text_widget = header.query_one("#header_text_content", Static)
            assert str(text_widget.renderable) == "QuickTag"
            
            # Test with item
            header.update_header(beets_items[0])
            assert "Test Artist 1" in str(text_widget.renderable)
            assert "Test Track 1" in str(text_widget.renderable)


class TestQuickTagApp:
    """Test the main QuickTagApp."""

    @pytest.fixture
    def quicktag_app(self, mock_library, beets_items, test_categories, app_config):
        """Create a QuickTagApp instance for testing."""
        return QuickTagApp(
            lib=mock_library,
            items=beets_items,
            categories=test_categories,
            **app_config
        )

    def test_app_initialization(self, quicktag_app, beets_items, test_categories):
        """Test app initializes with correct state."""
        assert quicktag_app.items == beets_items
        assert quicktag_app.categories == test_categories
        assert quicktag_app.current_item_index == 0
        assert quicktag_app.item == beets_items[0]
        assert quicktag_app.playback_widget is not None
        assert quicktag_app.header_widget is not None

    def test_app_initialization_empty_items(self, mock_library, test_categories, app_config):
        """Test app initialization with empty items list."""
        app = QuickTagApp(
            lib=mock_library,
            items=[],
            categories=test_categories,
            **app_config
        )
        assert app.item is None

    @pytest.mark.asyncio
    async def test_app_compose_with_items(self, quicktag_app):
        """Test app composition with items."""
        async with quicktag_app.run_test() as pilot:
            # Should have header
            assert quicktag_app.query_one(HeaderWidget)
            
            # Should have selection lists for each category
            selection_lists = quicktag_app.query(CustomSelectionList)
            assert len(selection_lists) == 3  # genre, mood, rating
            
            # Should have comments input
            assert quicktag_app.query_one(InputWithLabel)

    @pytest.mark.asyncio
    async def test_app_compose_no_items(self, mock_library, test_categories, app_config):
        """Test app composition with no items."""
        app = QuickTagApp(
            lib=mock_library,
            items=[],
            categories=test_categories,
            **app_config
        )
        
        async with app.run_test() as pilot:
            # Should show "No items to tag" message
            static_widgets = app.query(Static)
            static_texts = [str(w.renderable) for w in static_widgets]
            assert any("No items to tag" in text for text in static_texts)

    @pytest.mark.asyncio
    async def test_navigation_forward(self, quicktag_app):
        """Test forward navigation between items."""
        async with quicktag_app.run_test() as pilot:
            # Start with first item
            assert quicktag_app.current_item_index == 0
            assert quicktag_app.item.title == "Test Track 1"
            
            # Navigate forward
            await quicktag_app.action_next_item()
            assert quicktag_app.current_item_index == 1
            assert quicktag_app.item.title == "Test Track 2"
            
            # Navigate forward again
            await quicktag_app.action_next_item()
            assert quicktag_app.current_item_index == 2
            assert quicktag_app.item.title == "Test Track 3"

    @pytest.mark.asyncio
    async def test_navigation_backward(self, quicktag_app):
        """Test backward navigation between items."""
        async with quicktag_app.run_test() as pilot:
            # Start at second item
            quicktag_app.current_item_index = 1
            await quicktag_app._set_item(quicktag_app.items[1], save_current_item_tags=False)
            
            # Navigate backward
            await quicktag_app.action_previous_item()
            assert quicktag_app.current_item_index == 0
            assert quicktag_app.item.title == "Test Track 1"

    @pytest.mark.asyncio
    async def test_navigation_at_boundaries(self, quicktag_app):
        """Test navigation at list boundaries."""
        async with quicktag_app.run_test() as pilot:
            # Test backward at start (should not change)
            assert quicktag_app.current_item_index == 0
            await quicktag_app.action_previous_item()
            assert quicktag_app.current_item_index == 0
            
            # Navigate to end
            quicktag_app.current_item_index = 2
            await quicktag_app._set_item(quicktag_app.items[2], save_current_item_tags=False)
            
            # Test forward past end (should show completion message)
            await quicktag_app.action_next_item()
            header_text = quicktag_app.header_widget._header_text_display.renderable
            assert "All items processed" in str(header_text)

    @pytest.mark.asyncio
    async def test_playback_actions(self, quicktag_app):
        """Test playback control actions."""
        async with quicktag_app.run_test() as pilot:
            # Mock playback widget methods
            quicktag_app.playback_widget.play_pause = MagicMock()
            quicktag_app.playback_widget.seek_relative = MagicMock()
            
            # Test play/pause
            await quicktag_app.action_play_pause_current_item()
            quicktag_app.playback_widget.play_pause.assert_called_once()
            
            # Test seeking
            await quicktag_app.action_seek_forward(5)
            quicktag_app.playback_widget.seek_relative.assert_called_with(5)
            
            await quicktag_app.action_seek_backward(5)
            quicktag_app.playback_widget.seek_relative.assert_called_with(-5)

    @pytest.mark.asyncio
    async def test_save_tags_simple_case(self, quicktag_app):
        """Test saving tags for a single category."""
        async with quicktag_app.run_test() as pilot:
            # Find the genre selection list
            genre_list = quicktag_app.query_one("#selection-genre", CustomSelectionList)
            
            # Select "rock" (index 0)
            genre_list.select(0)
            
            # Save tags
            await quicktag_app._save_current_item_tags()
            
            # Check that the item was tagged
            assert quicktag_app.item.get("genre") == "rock"
            quicktag_app.item.store.assert_called()

    @pytest.mark.asyncio
    async def test_save_tags_multiple_selections(self, quicktag_app):
        """Test saving tags with multiple selections in one category."""
        async with quicktag_app.run_test() as pilot:
            # Find the mood selection list
            mood_list = quicktag_app.query_one("#selection-mood", CustomSelectionList)
            
            # Select multiple moods
            mood_list.select(0)  # happy
            mood_list.select(2)  # energetic
            
            # Save tags
            await quicktag_app._save_current_item_tags()
            
            # Check that multiple values are saved
            mood_value = quicktag_app.item.get("mood")
            assert "happy" in mood_value
            assert "energetic" in mood_value
            assert "," in mood_value  # Should be comma-separated

    @pytest.mark.asyncio
    async def test_save_comments(self, quicktag_app):
        """Test saving comments."""
        async with quicktag_app.run_test() as pilot:
            # Find comments input
            comments_input = quicktag_app.query_one("#comments-input", InputWithLabel)
            comments_input.value = "Great track!"
            
            # Save tags
            await quicktag_app._save_current_item_tags()
            
            # Check comments were saved
            assert quicktag_app.item.get("comments") == "Great track!"

    @pytest.mark.asyncio
    async def test_load_existing_tags(self, quicktag_app):
        """Test loading existing tags into the UI."""
        async with quicktag_app.run_test() as pilot:
            # Set some existing tags on the item
            quicktag_app.item.genre = "rock, pop"
            quicktag_app.item.mood = "happy"
            quicktag_app.item.comments = "Existing comment"
            
            # Mock the get method to return these values
            def mock_get(key, default=None):
                return getattr(quicktag_app.item, key, default)
            quicktag_app.item.get = mock_get
            
            # Load tags
            await quicktag_app._load_tags_for_current_item()
            
            # Check that UI reflects the existing tags
            genre_list = quicktag_app.query_one("#selection-genre", CustomSelectionList)
            mood_list = quicktag_app.query_one("#selection-mood", CustomSelectionList)
            comments_input = quicktag_app.query_one("#comments-input", InputWithLabel)
            
            # rock (0) and pop (1) should be selected
            assert 0 in genre_list.selected
            assert 1 in genre_list.selected
            
            # happy (0) should be selected
            assert 0 in mood_list.selected
            
            # Comments should be loaded
            assert comments_input.value == "Existing comment"

    @pytest.mark.asyncio
    async def test_autosave_on_quit(self, mock_library, beets_items, test_categories):
        """Test autosave functionality on quit."""
        app = QuickTagApp(
            lib=mock_library,
            items=beets_items,
            categories=test_categories,
            autoplay_on_track_change_enabled=False,
            autoplay_at_launch_enabled=False,
            autonext_at_track_end_enabled=False,
            autosave_on_quit_enabled=True,  # Enable autosave
            keep_playing_on_track_change_if_playing_enabled=True,
        )
        
        async with app.run_test() as pilot:
            # Mock save method
            app._save_current_item_tags = MagicMock()
            
            # Quit the app
            await app.action_quit()
            
            # Should have called save
            app._save_current_item_tags.assert_called_once()

    @pytest.mark.asyncio
    async def test_no_autosave_on_quit(self, quicktag_app):
        """Test that autosave doesn't happen when disabled."""
        async with quicktag_app.run_test() as pilot:
            # Mock save method
            quicktag_app._save_current_item_tags = MagicMock()
            
            # Quit the app
            await quicktag_app.action_quit()
            
            # Should not have called save (autosave disabled in fixture)
            quicktag_app._save_current_item_tags.assert_not_called()

    @pytest.mark.asyncio
    async def test_track_ended_with_autonext(self, mock_library, beets_items, test_categories):
        """Test track ended behavior with autonext enabled."""
        from beetsplug.quicktag.widgets.playback import PlaybackEnded
        
        app = QuickTagApp(
            lib=mock_library,
            items=beets_items,
            categories=test_categories,
            autoplay_on_track_change_enabled=False,
            autoplay_at_launch_enabled=False,
            autonext_at_track_end_enabled=True,  # Enable autonext
            autosave_on_quit_enabled=False,
            keep_playing_on_track_change_if_playing_enabled=True,
        )
        
        async with app.run_test() as pilot:
            # Start at first track
            assert app.current_item_index == 0
            
            # Simulate track ended
            message = PlaybackEnded()
            await app.on_playback_widget_track_ended(message)
            
            # Should advance to next track
            assert app.current_item_index == 1

    @pytest.mark.asyncio
    async def test_track_ended_without_autonext(self, quicktag_app):
        """Test track ended behavior with autonext disabled."""
        from beetsplug.quicktag.widgets.playback import PlaybackEnded
        
        async with quicktag_app.run_test() as pilot:
            # Mock playback methods
            quicktag_app.playback_widget.pause = MagicMock()
            quicktag_app.playback_widget.seek = MagicMock()
            
            # Simulate track ended
            message = PlaybackEnded()
            await quicktag_app.on_playback_widget_track_ended(message)
            
            # Should pause and seek to beginning
            quicktag_app.playback_widget.pause.assert_called_once()
            quicktag_app.playback_widget.seek.assert_called_with(0)

    @pytest.mark.asyncio
    async def test_item_without_path(self, quicktag_app):
        """Test handling items without valid paths."""
        async with quicktag_app.run_test() as pilot:
            # Create item without path
            quicktag_app.item.path = None
            
            # Try to play - should handle gracefully
            await quicktag_app.action_play_pause_current_item()
            # Should not crash

    @pytest.mark.asyncio
    async def test_app_key_bindings(self, quicktag_app):
        """Test that key bindings are properly defined."""
        # Check that bindings exist
        binding_keys = [binding.key for binding in quicktag_app.BINDINGS]
        
        assert "escape" in binding_keys
        assert "left" in binding_keys
        assert "right" in binding_keys
        assert "/" in binding_keys
        assert "<" in binding_keys
        assert ">" in binding_keys

    def test_app_css_defined(self, quicktag_app):
        """Test that CSS is properly defined."""
        assert quicktag_app.DEFAULT_CSS is not None
        assert "Screen" in quicktag_app.DEFAULT_CSS
        assert "SelectionList" in quicktag_app.DEFAULT_CSS

# TODO: Tests for the application will be added here.
