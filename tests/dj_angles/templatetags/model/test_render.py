from unittest.mock import patch

import pytest
from django.template.base import Token, TokenType
from django.template.context import RenderContext
from example.book.models import Book

from dj_angles.templatetags.model import do_model


@pytest.mark.django_db
def test_model():
    Book.objects.create(id=1, title="Tom Sawyer")

    token = Token(TokenType.BLOCK, contents="model Book.objects.filter(id=1).first() as book")
    node = do_model(None, token)

    context = RenderContext({"Book": Book})
    node.render(context)

    assert "book" in context
    assert isinstance(context["book"], Book)
    assert context["book"].title == "Tom Sawyer"


@pytest.mark.django_db
@patch("dj_angles.templatetags.model.get_models")
def test_model_verify_models_are_cached(get_models):
    Book.objects.create(id=1, title="Tom Sawyer")

    token = Token(TokenType.BLOCK, contents="model Book.objects.filter(id=1).first() as book")
    node = do_model(None, token)

    context = RenderContext({"Book": Book})

    assert get_models.call_count == 0

    node.render(context)

    get_models.assert_called_once()

    node.render(context)
    get_models.assert_called_once()
