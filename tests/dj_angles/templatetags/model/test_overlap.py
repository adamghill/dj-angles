from unittest.mock import patch

import pytest

from dj_angles.templatetags.model import get_models


# Mock setup for apps and models
class MockModel:
    def __init__(self, name):
        self.__name__ = name

    def __repr__(self):
        return f"<Model: {self.__name__}>"


class MockAppConfig:
    def __init__(self, label, models):
        self.label = label
        self._models = models

    def get_models(self):
        return self._models


@pytest.fixture
def mock_apps():
    with patch("dj_angles.templatetags.model.apps") as mock_apps:
        yield mock_apps


def test_get_models_structure(mock_apps):
    # Setup: 2 apps, "shop" and "inventory"
    # "shop" has "Product"
    # "inventory" has "Product" (overlap) and "Item"

    product1 = MockModel("Product")
    product2 = MockModel("Product")  # Different object, same name
    item = MockModel("Item")

    app1 = MockAppConfig("shop", [product1])
    app2 = MockAppConfig("inventory", [product2, item])

    mock_apps.get_app_configs.return_value = [app1, app2]

    models = get_models()

    # Check nesting
    assert models["shop"]["Product"] is product1
    assert models["inventory"]["Product"] is product2
    assert models["inventory"]["Item"] is item

    # Check short names
    assert models["Item"] is item
    # Last wins for overlapping short names
    assert models["Product"] is product2


def test_model_app_collision_warning(mock_apps, caplog):
    # Setup: App named "User" and Model named "User" (in another app)
    user_model = MockModel("User")
    app_user = MockAppConfig("User", [])  # App named User
    app_auth = MockAppConfig("auth", [user_model])  # Model named User

    mock_apps.get_app_configs.return_value = [app_user, app_auth]

    with caplog.at_level("WARNING"):
        models = get_models()

    # App dict exists first
    assert isinstance(models["User"], MockModel)  # Overwritten by model
    assert models["User"] is user_model

    # Verify warning
    assert "Model name collision with app label: User" in caplog.text


def test_model_model_collision_warning(mock_apps, caplog):
    product1 = MockModel("Product")
    product2 = MockModel("Product")

    app1 = MockAppConfig("shop", [product1])
    app2 = MockAppConfig("inventory", [product2])

    mock_apps.get_app_configs.return_value = [app1, app2]

    with caplog.at_level("WARNING"):
        models = get_models()

    assert "Model name collision: Product" in caplog.text
    assert "Using inventory" in caplog.text  # Should mention the new app label
