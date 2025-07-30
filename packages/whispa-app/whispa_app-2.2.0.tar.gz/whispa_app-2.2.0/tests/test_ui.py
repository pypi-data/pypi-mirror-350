"""Tests for UI components."""

import pytest
from unittest.mock import Mock, patch, MagicMock

from whispa_app.ui.panels import build_panels

@pytest.fixture
def root():
    """Create a mock root window for testing."""
    root = MagicMock()
    root.winfo_children.return_value = []
    return root

@pytest.fixture
def mock_callbacks():
    """Create mock callbacks for UI testing."""
    return {
        "on_transcribe": Mock(),
        "on_translate": Mock(),
        "on_export": Mock(),
        "on_model_change": Mock(),
        "on_language_change": Mock()
    }

@patch('whispa_app.ui.panels.ctk')
def test_build_panels(mock_ctk, mock_callbacks):
    """Test panel construction."""
    # Create mock frame and button classes
    mock_frame = MagicMock()
    mock_button = MagicMock()
    mock_combobox = MagicMock()
    
    mock_ctk.CTkFrame.return_value = mock_frame
    mock_ctk.CTkButton.return_value = mock_button
    mock_ctk.CTkComboBox.return_value = mock_combobox
    mock_ctk.StringVar.return_value = MagicMock()
    
    # Create a mock root
    root = MagicMock()
    
    panels = build_panels(
        root,
        on_transcribe=mock_callbacks["on_transcribe"],
        on_translate=mock_callbacks["on_translate"],
        on_export=mock_callbacks["on_export"],
        on_model_change=mock_callbacks["on_model_change"],
        on_language_change=mock_callbacks["on_language_change"]
    )
    
    assert isinstance(panels, dict)
    assert "input" in panels
    assert "output" in panels
    assert "controls" in panels
    
    # Verify components were created
    assert mock_ctk.CTkFrame.call_count >= 3  # At least 3 frames
    assert mock_ctk.CTkButton.call_count >= 3  # At least 3 buttons
    assert mock_ctk.CTkComboBox.call_count >= 2  # At least 2 dropdowns

@patch('whispa_app.ui.panels.ctk')
def test_button_callbacks(mock_ctk, mock_callbacks):
    """Test button callback connections."""
    # Set up mocks
    mock_ctk.CTkFrame.return_value = MagicMock()
    mock_ctk.CTkTextbox.return_value = MagicMock()
    mock_ctk.StringVar.return_value = MagicMock()
    mock_ctk.CTkComboBox.return_value = MagicMock()
    
    # Create mock buttons that store their command
    def create_button_with_command(self, *args, **kwargs):
        btn = MagicMock()
        btn.command = kwargs.get('command')
        return btn
    
    mock_ctk.CTkButton = Mock(side_effect=create_button_with_command)
    
    # Create a mock root
    root = MagicMock()
    
    panels = build_panels(
        root,
        on_transcribe=mock_callbacks["on_transcribe"],
        on_translate=mock_callbacks["on_translate"],
        on_export=mock_callbacks["on_export"],
        on_model_change=mock_callbacks["on_model_change"],
        on_language_change=mock_callbacks["on_language_change"]
    )
    
    # Test transcribe button by calling its stored command
    panels["transcribe_btn"].command()
    mock_callbacks["on_transcribe"].assert_called_once()
    
    # Test translate button
    panels["translate_btn"].command()
    mock_callbacks["on_translate"].assert_called_once()
    
    # Test export button
    panels["export_btn"].command()
    mock_callbacks["on_export"].assert_called_once()

@patch('whispa_app.ui.panels.ctk')
def test_model_selection(mock_ctk, mock_callbacks):
    """Test model selection dropdown."""
    # Set up mocks
    mock_ctk.CTkFrame.return_value = MagicMock()
    mock_ctk.CTkTextbox.return_value = MagicMock()
    mock_ctk.StringVar.return_value = MagicMock()
    
    # Create mock combobox that stores its command
    def create_combobox_with_command(self, *args, **kwargs):
        box = MagicMock()
        box.command = kwargs.get('command')
        return box
    
    mock_ctk.CTkComboBox = Mock(side_effect=create_combobox_with_command)
    
    # Create a mock root
    root = MagicMock()
    
    panels = build_panels(
        root,
        on_transcribe=mock_callbacks["on_transcribe"],
        on_translate=mock_callbacks["on_translate"],
        on_export=mock_callbacks["on_export"],
        on_model_change=mock_callbacks["on_model_change"],
        on_language_change=mock_callbacks["on_language_change"]
    )
    
    # Test model selection by calling its command directly
    panels["model_dropdown"].command("base")
    mock_callbacks["on_model_change"].assert_called_with("base")

@patch('whispa_app.ui.panels.ctk')
def test_language_selection(mock_ctk, mock_callbacks):
    """Test language selection dropdown."""
    # Set up mocks
    mock_ctk.CTkFrame.return_value = MagicMock()
    mock_ctk.CTkTextbox.return_value = MagicMock()
    mock_ctk.StringVar.return_value = MagicMock()
    
    # Create mock combobox that stores its command
    def create_combobox_with_command(self, *args, **kwargs):
        box = MagicMock()
        box.command = kwargs.get('command')
        return box
    
    mock_ctk.CTkComboBox = Mock(side_effect=create_combobox_with_command)
    
    # Create a mock root
    root = MagicMock()
    
    panels = build_panels(
        root,
        on_transcribe=mock_callbacks["on_transcribe"],
        on_translate=mock_callbacks["on_translate"],
        on_export=mock_callbacks["on_export"],
        on_model_change=mock_callbacks["on_model_change"],
        on_language_change=mock_callbacks["on_language_change"]
    )
    
    # Test language selection by calling its command directly
    panels["lang_dropdown"].command("Spanish")
    mock_callbacks["on_language_change"].assert_called_with("Spanish") 