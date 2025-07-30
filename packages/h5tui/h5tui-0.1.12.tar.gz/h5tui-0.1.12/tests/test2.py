import pytest
from unittest.mock import MagicMock
from textual.app import App
from textual.widgets import Static
from textual.screen import ModalScreen
from h5tui.h5tui import H5TUIApp, AttributeScreen, check_file_validity, h5tui

EXAMPLE_H5FILE = "example.h5"

# Mock HDF5 file and other components
@pytest.fixture
def mock_h5file():
    # Mock an HDF5 file
    mock_file = MagicMock()
    mock_file.name = EXAMPLE_H5FILE
    return mock_file

@pytest.fixture
def app(mock_h5file):
    # Initialize the H5TUIApp with a mocked HDF5 file
    return H5TUIApp(EXAMPLE_H5FILE)

# Test Initialization of H5TUIApp
def test_app_initialization(app):
    assert isinstance(app, H5TUIApp)
    assert app._fname == EXAMPLE_H5FILE
    assert app._file is not None  # Ensures the file is initialized

# Test the quit action in AttributeScreen
def test_action_quit_attrs(app, mocker):
    # Mock the app's pop_screen method
    mock_pop_screen = mocker.patch.object(app, 'pop_screen')
    
    # Create AttributeScreen and trigger quit action
    screen = AttributeScreen(app._file, '/Group2', 'RecArray')
    screen.action_quit_attrs()

    # Check if pop_screen was called once
    mock_pop_screen.assert_called_once()

# Test moving cursor down in AttributeScreen
def test_action_cursor_down(app):
    screen = AttributeScreen(app._file, '/Group2', 'RecArray')
    initial_attr = screen._cur_attr
    screen.action_cursor_down()
    
    # Verify the attribute has changed
    assert screen._cur_attr != initial_attr

# Test the toggle_plot action in H5TUIApp
def test_action_toggle_plot(app):
    # Mock the toggle_class method
    mock_toggle_class = MagicMock()
    app.toggle_class = mock_toggle_class
    
    # Perform the action
    app.action_toggle_plot()

    # Ensure toggle_class was called
    mock_toggle_class.assert_called_once_with("view-plot")

# Test check_file_validity function
def test_check_file_validity():
    # Test valid file
    assert check_file_validity(EXAMPLE_H5FILE) is True
    # Test invalid file
    assert check_file_validity('invalid_file.txt') is False

# Test h5tui function (entry point)
def test_h5tui(mocker):
    # Mock the command-line arguments
    mocker.patch('sys.argv', ['h5tui.py', EXAMPLE_H5FILE])
    
    # Mock the check_file_validity function
    mocker.patch('your_module.check_file_validity', return_value=True)
    
    # Mock the run method of H5TUIApp
    mock_run = mocker.patch.object(H5TUIApp, 'run')
    
    # Call the h5tui function
    h5tui()

    # Ensure the run method was called once
    mock_run.assert_called_once()


