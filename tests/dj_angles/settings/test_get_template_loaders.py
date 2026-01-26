from unittest.mock import patch

from dj_angles.settings import get_template_loaders


def test_get_template_loaders_cached_true():
    loaders = get_template_loaders(cached=True)
    assert len(loaders) == 1
    assert loaders[0][0] == "django.template.loaders.cached.Loader"
    assert isinstance(loaders[0][1], list)


def test_get_template_loaders_cached_false():
    loaders = get_template_loaders(cached=False)
    assert isinstance(loaders, list)
    # Check it's a flat list of strings, not the cached loader tuple
    assert isinstance(loaders[0], str)
    assert "dj_angles.template_loader.Loader" in loaders


def test_get_template_loaders_default_debug_true(settings):
    settings.DEBUG = True
    loaders = get_template_loaders()
    assert isinstance(loaders, list)
    assert isinstance(loaders[0], str)


def test_get_template_loaders_default_debug_false(settings):
    settings.DEBUG = False
    loaders = get_template_loaders()
    assert len(loaders) == 1
    assert loaders[0][0] == "django.template.loaders.cached.Loader"


@patch("dj_angles.settings.is_module_available")
def test_get_template_loaders_with_bird(mock_is_module_available):
    def side_effect(name):
        return name == "django_bird"

    mock_is_module_available.side_effect = side_effect

    loaders = get_template_loaders(cached=False)
    assert "django_bird.loader.BirdLoader" in loaders
    # Ensure it is inserted at the correct position (index 1)
    assert loaders[1] == "django_bird.loader.BirdLoader"


@patch("dj_angles.settings.is_module_available")
def test_get_template_loaders_with_components(mock_is_module_available):
    def side_effect(name):
        return name == "django_components"

    mock_is_module_available.side_effect = side_effect

    loaders = get_template_loaders(cached=False)
    assert "django_components.template_loader.Loader" in loaders
    # Ensure it's at the end
    assert loaders[-1] == "django_components.template_loader.Loader"


@patch("dj_angles.settings.is_module_available")
def test_get_template_loaders_with_viewcomponent(mock_is_module_available):
    def side_effect(name):
        return name == "django_viewcomponent"

    mock_is_module_available.side_effect = side_effect

    loaders = get_template_loaders(cached=False)
    assert "django_viewcomponent.loaders.ComponentLoader" in loaders
    # Ensure it's at the beginning, or at least before others if logic dictates
    # Based on implementation it is inserted at 0
    assert loaders[0] == "django_viewcomponent.loaders.ComponentLoader"
