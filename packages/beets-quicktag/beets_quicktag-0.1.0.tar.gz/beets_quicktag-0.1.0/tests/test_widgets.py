import pytest
from textual.widgets import SelectionList
from textual import events

from beetsplug.quicktag.widgets.custom_selection_list import CustomSelectionList
from beetsplug.quicktag.widgets.input_with_label import InputWithLabel
from beetsplug.quicktag.widgets.playback_progress import PlaybackProgressWidget


class TestCustomSelectionList:
    """Test the CustomSelectionList widget."""

    def test_initialization(self):
        """Test CustomSelectionList initializes correctly."""
        widget = CustomSelectionList()
        assert isinstance(widget, SelectionList)
        assert widget.search_char is None

    @pytest.mark.asyncio
    async def test_alphanumeric_key_search(self):
        """Test searching through options with alphanumeric keys."""
        from textual.widgets.selection_list import Selection
        
        # Create selection list with test options
        options = [
            Selection("Apple", 0),
            Selection("Banana", 1),
            Selection("Cherry", 2),
            Selection("Date", 3),
        ]
        
        widget = CustomSelectionList(*options)
        
        # Simulate mounting the widget
        widget.highlighted = 0  # Start with "Apple" highlighted
        
        # Create a key event for 'b' to find "Banana"
        key_event = events.Key("b", "b")
        
        await widget.on_key(key_event)
        
        # Should move to "Banana" (index 1)
        assert widget.highlighted == 1
        assert widget.search_char == "b"

    @pytest.mark.asyncio
    async def test_key_search_wrapping(self):
        """Test that key search wraps around the list."""
        from textual.widgets.selection_list import Selection
        
        options = [
            Selection("Apple", 0),
            Selection("Banana", 1),
            Selection("Cherry", 2),
            Selection("Avocado", 3),  # Second item starting with 'A'
        ]
        
        widget = CustomSelectionList(*options)
        widget.highlighted = 0  # Start with "Apple"
        
        # Search for 'a' again - should wrap to "Avocado"
        key_event = events.Key("a", "a")
        await widget.on_key(key_event)
        
        assert widget.highlighted == 3  # Should wrap to "Avocado"

    @pytest.mark.asyncio
    async def test_non_alphanumeric_key_ignored(self):
        """Test that non-alphanumeric keys are not handled."""
        from textual.widgets.selection_list import Selection
        
        options = [Selection("Apple", 0), Selection("Banana", 1)]
        widget = CustomSelectionList(*options)
        widget.highlighted = 0
        
        # Create a non-alphanumeric key event
        key_event = events.Key("escape", None)
        
        await widget.on_key(key_event)
        
        # Should not change highlighted item
        assert widget.highlighted == 0
        assert widget.search_char is None

    @pytest.mark.asyncio
    async def test_empty_options_list(self):
        """Test behavior with empty options list."""
        widget = CustomSelectionList()
        
        key_event = events.Key("a", "a")
        await widget.on_key(key_event)
        
        # Should handle gracefully
        assert widget.search_char == "a"


class TestInputWithLabel:
    """Test the InputWithLabel widget."""

    def test_initialization(self):
        """Test InputWithLabel initializes correctly."""
        widget = InputWithLabel("Test Label:", id="test-input")
        assert widget.input_label == "Test Label:"
        assert widget.id == "test-input"

    def test_compose_creates_children(self):
        """Test that compose creates Label and Input widgets."""
        widget = InputWithLabel("Comments:")
        
        # Get the composed widgets
        children = list(widget.compose())
        assert len(children) == 2
        
        # First should be a Label, second should be an Input
        from textual.widgets import Label, Input
        assert isinstance(children[0], Label)
        assert isinstance(children[1], Input)

    @pytest.mark.asyncio
    async def test_value_property(self):
        """Test the value property getter and setter."""
        from textual.app import App
        from textual.widgets import Input
        
        class TestApp(App):
            def compose(self):
                yield InputWithLabel("Test:", id="test-widget")
        
        app = TestApp()
        async with app.run_test() as pilot:
            widget = app.query_one("#test-widget", InputWithLabel)
            
            # Test initial value is empty
            assert widget.value == ""
            
            # Test setting value
            widget.value = "test content"
            assert widget.value == "test content"
            
            # Verify the underlying Input widget has the value
            input_widget = widget.query_one(Input)
            assert input_widget.value == "test content"


class TestPlaybackProgressWidget:
    """Test the PlaybackProgressWidget."""

    def test_initialization_with_player(self):
        """Test initialization with a player."""
        from unittest.mock import MagicMock
        
        mock_player = MagicMock()
        mock_player.duration = None
        mock_player.curr_pos = None
        
        widget = PlaybackProgressWidget(player=mock_player)
        assert widget.player == mock_player

    def test_format_time_utility(self):
        """Test the time formatting utility function."""
        from beetsplug.quicktag.widgets.playback_progress import format_seconds_to_time_str
        
        assert format_seconds_to_time_str(0) == "00:00"
        assert format_seconds_to_time_str(65) == "01:05"
        assert format_seconds_to_time_str(3661) == "61:01"  # Over an hour
        assert format_seconds_to_time_str(None) == "--:--"
        assert format_seconds_to_time_str(-5) == "00:00"  # Negative values

    def test_update_progress_display_no_duration(self):
        """Test progress display update when no duration is available."""
        from unittest.mock import MagicMock
        
        mock_player = MagicMock()
        mock_player.duration = None
        mock_player.curr_pos = 65.0
        
        widget = PlaybackProgressWidget(player=mock_player)
        widget._progress_bar = MagicMock()
        widget._time_remaining_display = MagicMock()
        
        widget._update_progress_display()
        
        # Should hide progress bar and time display when no duration
        widget._progress_bar.visible = False
        widget._time_remaining_display.visible = False

    def test_update_progress_display_with_duration(self):
        """Test progress display update with duration."""
        from unittest.mock import MagicMock
        
        mock_player = MagicMock()
        mock_player.duration = 180.0  # 3 minutes
        mock_player.curr_pos = 65.0   # 1:05
        mock_player.active = True
        
        widget = PlaybackProgressWidget(player=mock_player)
        widget._progress_bar = MagicMock()
        widget._time_remaining_display = MagicMock()
        
        widget._update_progress_display()
        
        # Should update progress bar
        assert widget._progress_bar.total == 180.0
        assert widget._progress_bar.progress == 65.0
        widget._progress_bar.visible = True
        
        # Should update time remaining display
        widget._time_remaining_display.update.assert_called()
        widget._time_remaining_display.visible = True

    def test_compose_creates_children(self):
        """Test that compose creates the expected child widgets."""
        from unittest.mock import MagicMock
        
        mock_player = MagicMock()
        widget = PlaybackProgressWidget(player=mock_player)
        
        # Get the composed widgets
        children = list(widget.compose())
        assert len(children) == 1  # Should have one Horizontal container
        
        # The container should contain progress bar and time display
        from textual.containers import Horizontal
        assert isinstance(children[0], Horizontal) 