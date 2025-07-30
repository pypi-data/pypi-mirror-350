# TODO: Tests for playback functionality will be added here.

# filepath: /home/radu/repos/beets-quicktag/tests/test_playback.py
import pytest
from unittest.mock import MagicMock, patch, PropertyMock

from beetsplug.quicktag.widgets.playback import PlaybackEnded, PlaybackWidget


class TestPlaybackWidget:
    """Test the PlaybackWidget with just-playback."""

    @pytest.fixture
    def mock_playback(self):
        """Mock the just_playback.Playback class."""
        mock_player = MagicMock()
        mock_player.duration = None
        mock_player.curr_pos = None
        mock_player.active = False
        mock_player.playing = False
        mock_player.paused = False
        return mock_player

    @pytest.fixture
    def playback_widget(self, mock_playback):
        """Create a PlaybackWidget with mocked just_playback."""
        with patch('beetsplug.quicktag.widgets.playback.Playback', return_value=mock_playback):
            widget = PlaybackWidget()
            # Mock the post_message method for testing
            widget.post_message = MagicMock()
            return widget

    def test_initialization_success(self, playback_widget, mock_playback):
        """Test successful initialization of PlaybackWidget."""
        assert playback_widget.player == mock_playback
        assert playback_widget._current_path is None
        assert playback_widget._playback_progress is not None

    def test_initialization_failure(self):
        """Test PlaybackWidget initialization when just_playback fails."""
        with patch('beetsplug.quicktag.widgets.playback.Playback', side_effect=Exception("Mock error")):
            widget = PlaybackWidget()
            assert widget.player is None

    @pytest.mark.asyncio
    async def test_mount_starts_eof_timer(self, playback_widget):
        """Test that mounting starts the EOF check timer."""
        # Mock the set_interval method
        playback_widget.set_interval = MagicMock()
        
        await playback_widget.on_mount()
        
        # Should set up the EOF check timer
        playback_widget.set_interval.assert_called_once_with(0.5, playback_widget._check_eof)

    @pytest.mark.asyncio 
    async def test_unmount_cleanup(self, playback_widget, mock_playback):
        """Test that unmounting properly cleans up resources."""
        # Set up timer mock
        timer_mock = MagicMock()
        playback_widget._eof_check_timer = timer_mock
        
        await playback_widget.on_unmount()
        
        # Should stop timer and player
        timer_mock.stop.assert_called_once()
        mock_playback.stop.assert_called_once()
        assert playback_widget.player is None
        assert playback_widget._current_path is None

    def test_load_track_success(self, playback_widget, mock_playback):
        """Test successful track loading."""
        test_path = "/path/to/test.mp3"
        
        playback_widget.load_track(test_path)
        
        mock_playback.load_file.assert_called_once_with(test_path)
        assert playback_widget._current_path == test_path

    def test_load_track_same_path(self, playback_widget, mock_playback):
        """Test loading the same track twice."""
        test_path = "/path/to/test.mp3"
        playback_widget._current_path = test_path
        
        playback_widget.load_track(test_path)
        
        # Should not call load_file again
        mock_playback.load_file.assert_not_called()

    def test_load_track_empty_path(self, playback_widget, mock_playback):
        """Test loading with empty or None path."""
        playback_widget.load_track(None)
        
        # Should call stop and clear path
        mock_playback.stop.assert_called_once()
        assert playback_widget._current_path is None

    def test_load_track_error(self, playback_widget, mock_playback):
        """Test error handling during track loading."""
        mock_playback.load_file.side_effect = Exception("Load error")
        test_path = "/path/to/test.mp3"
        
        playback_widget.load_track(test_path)
        
        # Should handle error gracefully
        assert playback_widget._current_path is None

    def test_play_no_player(self, mock_playback):
        """Test play when no player is available."""
        with patch('beetsplug.quicktag.widgets.playback.Playback', side_effect=Exception("No player")):
            widget = PlaybackWidget()
            widget.play()  # Should not crash

    def test_play_no_track_loaded(self, playback_widget, mock_playback):
        """Test play when no track is loaded."""
        playback_widget._current_path = None
        
        playback_widget.play()
        
        # Should not attempt to play
        mock_playback.play.assert_not_called()
        mock_playback.resume.assert_not_called()

    def test_play_paused_track(self, playback_widget, mock_playback):
        """Test resuming a paused track."""
        playback_widget._current_path = "/path/to/test.mp3"
        mock_playback.paused = True
        
        playback_widget.play()
        
        mock_playback.resume.assert_called_once()

    def test_play_stopped_track(self, playback_widget, mock_playback):
        """Test playing a stopped track."""
        playback_widget._current_path = "/path/to/test.mp3"
        mock_playback.paused = False
        mock_playback.playing = False
        
        playback_widget.play()
        
        mock_playback.play.assert_called_once()

    def test_pause_success(self, playback_widget, mock_playback):
        """Test successful pause."""
        playback_widget._current_path = "/path/to/test.mp3"
        mock_playback.active = True
        mock_playback.paused = False
        playback_widget.is_player_active = MagicMock(return_value=True)
        
        playback_widget.pause()
        
        mock_playback.pause.assert_called_once()

    def test_pause_no_track(self, playback_widget, mock_playback):
        """Test pause when no track is active."""
        playback_widget.is_player_active = MagicMock(return_value=False)
        
        playback_widget.pause()
        
        mock_playback.pause.assert_not_called()

    def test_play_pause_toggle_to_play(self, playback_widget, mock_playback):
        """Test play_pause toggles from pause to play."""
        playback_widget._current_path = "/path/to/test.mp3"
        playback_widget.is_playing = MagicMock(return_value=False)
        mock_playback.paused = True
        
        playback_widget.play_pause()
        
        mock_playback.resume.assert_called_once()

    def test_play_pause_toggle_to_pause(self, playback_widget, mock_playback):
        """Test play_pause toggles from play to pause."""
        playback_widget._current_path = "/path/to/test.mp3"
        playback_widget.is_playing = MagicMock(return_value=True)
        playback_widget.is_player_active = MagicMock(return_value=True)
        mock_playback.paused = False
        
        playback_widget.play_pause()
        
        mock_playback.pause.assert_called_once()

    def test_stop(self, playback_widget, mock_playback):
        """Test stopping playback."""
        playback_widget._current_path = "/path/to/test.mp3"
        
        playback_widget.stop()
        
        mock_playback.stop.assert_called_once()
        assert playback_widget._current_path is None

    def test_seek_relative_with_position(self, playback_widget, mock_playback):
        """Test relative seeking when position is available."""
        mock_playback.duration = 180.0
        mock_playback.curr_pos = 60.0
        
        playback_widget.seek_relative(10)
        
        mock_playback.seek.assert_called_once_with(70.0)

    def test_seek_relative_clamp_to_bounds(self, playback_widget, mock_playback):
        """Test that seeking clamps to valid bounds."""
        mock_playback.duration = 180.0
        mock_playback.curr_pos = 175.0
        
        # Seek past end
        playback_widget.seek_relative(10)
        mock_playback.seek.assert_called_with(180.0)
        
        mock_playback.reset_mock()
        mock_playback.curr_pos = 5.0
        
        # Seek before start
        playback_widget.seek_relative(-10)
        mock_playback.seek.assert_called_with(0.0)

    def test_seek_relative_no_duration(self, playback_widget, mock_playback):
        """Test seeking when no duration is available."""
        mock_playback.duration = None
        
        playback_widget.seek_relative(10)
        
        mock_playback.seek.assert_not_called()

    def test_is_playing_true(self, playback_widget, mock_playback):
        """Test is_playing returns True when playing."""
        mock_playback.playing = True
        
        assert playback_widget.is_playing() is True

    def test_is_playing_false(self, playback_widget, mock_playback):
        """Test is_playing returns False when not playing."""
        mock_playback.playing = False
        
        assert playback_widget.is_playing() is False

    def test_is_playing_no_player(self, mock_playback):
        """Test is_playing when no player is available."""
        with patch('beetsplug.quicktag.widgets.playback.Playback', side_effect=Exception("No player")):
            widget = PlaybackWidget()
            assert widget.is_playing() is False

    def test_is_player_active_true(self, playback_widget, mock_playback):
        """Test is_player_active returns True when active."""
        mock_playback.active = True
        
        assert playback_widget.is_player_active() is True

    def test_is_player_active_false(self, playback_widget, mock_playback):
        """Test is_player_active returns False when not active."""
        mock_playback.active = False
        
        assert playback_widget.is_player_active() is False

    def test_check_eof_triggers_message(self, playback_widget, mock_playback):
        """Test that EOF check triggers PlaybackEnded message."""
        playback_widget._current_path = "/path/to/test.mp3"
        mock_playback.duration = 180.0
        mock_playback.curr_pos = 179.8  # Near end
        mock_playback.active = False  # Not playing anymore
        
        playback_widget._check_eof()
        
        # Should post PlaybackEnded message
        playback_widget.post_message.assert_called_once()
        message = playback_widget.post_message.call_args[0][0]
        assert isinstance(message, PlaybackEnded)

    def test_check_eof_not_at_end(self, playback_widget, mock_playback):
        """Test that EOF check doesn't trigger when not at end."""
        playback_widget._current_path = "/path/to/test.mp3"
        mock_playback.duration = 180.0
        mock_playback.curr_pos = 60.0  # Middle of track
        mock_playback.active = False
        
        playback_widget._check_eof()
        
        # Should not post message
        playback_widget.post_message.assert_not_called()

    def test_check_eof_still_active(self, playback_widget, mock_playback):
        """Test that EOF check doesn't trigger when still playing."""
        playback_widget._current_path = "/path/to/test.mp3"
        mock_playback.duration = 180.0
        mock_playback.curr_pos = 179.8
        mock_playback.active = True  # Still playing
        
        playback_widget._check_eof()
        
        # Should not post message
        playback_widget.post_message.assert_not_called()

    def test_check_eof_no_current_path(self, playback_widget, mock_playback):
        """Test EOF check when no track is loaded."""
        playback_widget._current_path = None
        
        playback_widget._check_eof()
        
        # Should not post message
        playback_widget.post_message.assert_not_called()
