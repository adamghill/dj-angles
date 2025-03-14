from django.template.base import Token, TokenType

from dj_angles.templatetags.model import do_model


def test_model():
    token = Token(TokenType.BLOCK, contents="model Book.objects.filter(id=1).first() as books")
    actual = do_model(None, token)

    assert actual.parsed_function.portions[0].name == "__dj_angles_models"
    assert actual.parsed_function.portions[1].name == "Book"
    assert actual.parsed_function.portions[2].name == "objects"
    assert actual.parsed_function.portions[3].name == "filter"
    assert actual.parsed_function.portions[3].args == []
    assert actual.parsed_function.portions[3].kwargs == {"id": 1}
    assert actual.parsed_function.portions[4].name == "first"
    assert actual.context_variable_name == "books"
