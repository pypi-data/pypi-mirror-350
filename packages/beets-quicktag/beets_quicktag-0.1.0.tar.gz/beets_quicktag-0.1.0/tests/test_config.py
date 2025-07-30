import pytest
from beetsplug.quicktag import QuickTagPlugin


def test_plugin_initialization():
    """Test that the plugin initializes correctly."""
    plugin = QuickTagPlugin()
    
    # Test that it has the expected plugin interface
    assert hasattr(plugin, 'config')
    assert hasattr(plugin, 'commands')
    assert callable(plugin.commands)
    assert callable(plugin.run_quicktag)


def test_plugin_commands():
    """Test that the plugin correctly registers its commands."""
    plugin = QuickTagPlugin()
    commands = plugin.commands()
    
    assert len(commands) == 1
    
    cmd = commands[0]
    assert cmd.name == "quicktag"
    assert "qt" in cmd.aliases
    assert "Quickly tag tracks with predefined options." in cmd.help
    assert cmd.func == plugin.run_quicktag


def test_config_with_categories():
    """Test plugin behavior with categories configured."""
    plugin = QuickTagPlugin()
    
    # Simulate config with categories
    plugin.config.set({"categories": {
        "genre": ["rock", "pop", "jazz"],
        "mood": ["happy", "sad", "energetic"]
    }})
    
    categories_config = plugin.config["categories"].get(dict)
    assert "genre" in categories_config
    assert "mood" in categories_config
    assert categories_config["genre"] == ["rock", "pop", "jazz"]
    assert categories_config["mood"] == ["happy", "sad", "energetic"]


def test_boolean_config_values():
    """Test that boolean configuration values work correctly."""
    plugin = QuickTagPlugin()
    
    # Test setting True values
    plugin.config.set({
        "autoplay_on_track_change": True,
        "autoplay_at_launch": True,
        "autonext_at_track_end": True,
        "autosave_on_quit": True,
        "keep_playing_on_track_change_if_playing": False,
    })
    
    assert plugin.config["autoplay_on_track_change"].get(bool) is True
    assert plugin.config["autoplay_at_launch"].get(bool) is True
    assert plugin.config["autonext_at_track_end"].get(bool) is True
    assert plugin.config["autosave_on_quit"].get(bool) is True
    assert plugin.config["keep_playing_on_track_change_if_playing"].get(bool) is False


def test_empty_categories_config():
    """Test behavior when categories config is explicitly empty."""
    plugin = QuickTagPlugin()
    plugin.config.set({"categories": {}})
    
    categories_config = plugin.config["categories"].get(dict)
    assert categories_config == {}


def test_config_defaults_are_set():
    """Test that the plugin sets up default configuration values."""
    plugin = QuickTagPlugin()
    
    # These should be available even if not explicitly configured
    assert plugin.config["autoplay_on_track_change"].exists()
    assert plugin.config["autoplay_at_launch"].exists()
    assert plugin.config["autonext_at_track_end"].exists()
    assert plugin.config["autosave_on_quit"].exists()
    assert plugin.config["keep_playing_on_track_change_if_playing"].exists()
    assert plugin.config["categories"].exists()


def test_config_type_conversion():
    """Test that configuration values are properly converted to expected types."""
    plugin = QuickTagPlugin()
    
    # Test that boolean values work correctly
    plugin.config.set({"autoplay_on_track_change": True})
    assert plugin.config["autoplay_on_track_change"].get(bool) is True
    
    plugin.config.set({"autoplay_on_track_change": False})
    assert plugin.config["autoplay_on_track_change"].get(bool) is False
    
    # Test that dict values work correctly
    plugin.config.set({"categories": {"test": ["a", "b"]}})
    categories = plugin.config["categories"].get(dict)
    assert isinstance(categories, dict)
    assert categories["test"] == ["a", "b"]


# TODO: More tests will be added here.
