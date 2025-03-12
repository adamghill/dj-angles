from datetime import datetime, time, timedelta
from uuid import UUID

from django.template.base import Token, TokenType
from django.template.context import RenderContext

from dj_angles.templatetags.call import do_call


def test_no_args():
    token = Token(TokenType.BLOCK, contents="call set_name as name")
    node = do_call(None, token)

    context = RenderContext({"set_name": lambda: "Alice"})
    node.render(context)

    assert context["name"] == "Alice"


def test_str_arg():
    token = Token(TokenType.BLOCK, contents="call set_name 'Bob' as name")
    node = do_call(None, token)

    context = RenderContext({"set_name": lambda s: s.upper()})
    node.render(context)

    assert context["name"] == "BOB"


def test_multiple_args():
    token = Token(TokenType.BLOCK, contents="call set_name_duplicate 'Jill' 3 as name")
    node = do_call(None, token)

    context = RenderContext({"set_name_duplicate": lambda s, n: s * n})
    node.render(context)

    assert context["name"] == "JillJillJill"


def test_parens():
    token = Token(TokenType.BLOCK, contents="call set_name('Hello', 4) as name")
    node = do_call(None, token)

    context = RenderContext({"set_name": lambda s, n: s * n})
    node.render(context)

    assert context["name"] == "HelloHelloHelloHello"


def test_dictionary():
    token = Token(TokenType.BLOCK, contents="call set_name(dictionary) as name")
    node = do_call(None, token)

    context = RenderContext({"dictionary": {"name": "Hello"}, "set_name": lambda obj: obj["name"]})
    node.render(context)

    assert context["name"] == "Hello"


def test_true():
    token = Token(TokenType.BLOCK, contents="call set_name(True) as name")
    node = do_call(None, token)

    context = RenderContext({"set_name": lambda t: "Hello" if t else "Goodbye"})
    node.render(context)

    assert context["name"] == "Hello"


def test_false():
    token = Token(TokenType.BLOCK, contents="call set_name(False) as name")
    node = do_call(None, token)

    context = RenderContext({"set_name": lambda t: "Hello" if t else "Goodbye"})
    node.render(context)

    assert context["name"] == "Goodbye"


def test_none():
    token = Token(TokenType.BLOCK, contents="call set_name(None) as name")
    node = do_call(None, token)

    context = RenderContext({"set_name": lambda t: "Hello" if t is not None else "Goodbye"})
    node.render(context)

    assert context["name"] == "Goodbye"


def test_date():
    token = Token(TokenType.BLOCK, contents="call add_day('2025-03-11') as d")
    node = do_call(None, token)

    context = RenderContext({"add_day": lambda d: d + timedelta(days=1)})
    node.render(context)

    assert context["d"] == datetime(2025, 3, 12)


def test_datetime():
    token = Token(TokenType.BLOCK, contents="call add_day('2025-03-11T01:02:03') as dt")
    node = do_call(None, token)

    context = RenderContext({"add_day": lambda dt: dt + timedelta(days=1)})
    node.render(context)

    assert context["dt"] == datetime(2025, 3, 12, 1, 2, 3)


def test_time():
    token = Token(TokenType.BLOCK, contents="call set_time('01:02:03') as t")
    node = do_call(None, token)

    context = RenderContext({"set_time": lambda t: t.replace(hour=2)})
    node.render(context)

    assert context["t"] == time(2, 2, 3)


def test_uuid():
    token = Token(TokenType.BLOCK, contents="call set_uuid('ed997280-1ec8-4509-be83-f35426e1deff') as uuid")
    node = do_call(None, token)

    context = RenderContext({"set_uuid": lambda uuid: uuid})
    node.render(context)

    assert context["uuid"] == UUID("ed997280-1ec8-4509-be83-f35426e1deff")


def test_object():
    class TestObject:
        def __init__(self, name):
            self.name = name

    token = Token(TokenType.BLOCK, contents="call set_name(obj) as name")
    node = do_call(None, token)

    context = RenderContext({"obj": TestObject("Billy"), "set_name": lambda obj: obj.name})
    node.render(context)

    assert context["name"] == "Billy"


def test_object_function():
    class TestObject:
        def set_name(self, value):
            self.name = value

    token = Token(TokenType.BLOCK, contents="call obj.set_name('Sally')")
    node = do_call(None, token)

    context = RenderContext({"obj": TestObject()})
    node.render(context)

    assert context["obj"].name == "Sally"


def test_object_function_kwarg():
    class TestObject:
        def set(self, name: str = ""):
            self.name = name

    token = Token(TokenType.BLOCK, contents="call obj.set(name='Joe')")
    node = do_call(None, token)

    context = RenderContext({"obj": TestObject()})
    node.render(context)

    assert context["obj"].name == "Joe"


def test_nested_object_function():
    class TestObject:
        class NestedObject:
            def __init__(self, name):
                self.name = name

            def set_name(self, value):
                self.name = value

        def __init__(self, name):
            self.nested = self.NestedObject(name)

    token = Token(TokenType.BLOCK, contents="call obj.nested.set_name('Object2')")
    node = do_call(None, token)

    context = RenderContext({"obj": TestObject("Object1")})
    node.render(context)

    assert context["obj"].nested.name == "Object2"


def test_object_function_with_return():
    class TestObject:
        def __init__(self, name):
            self.name = name

        def get_name(self):
            return self.name + "!"

    token = Token(TokenType.BLOCK, contents="call obj.get_name as name")
    node = do_call(None, token)

    context = RenderContext({"obj": TestObject("bob")})
    node.render(context)

    assert context["name"] == "bob!"


def test_object_function_with_parens_with_return():
    class TestObject:
        def __init__(self, name):
            self.name = name

        def get_name(self):
            return self.name + "!"

    token = Token(TokenType.BLOCK, contents="call obj.get_name() as name")
    node = do_call(None, token)

    context = RenderContext({"obj": TestObject("bob")})
    node.render(context)

    assert context["name"] == "bob!"


def test_args_return_tuple():
    def set_names(*names):
        return names

    token = Token(TokenType.BLOCK, contents="call set_names(*names) as names")
    node = do_call(None, token)

    context = RenderContext({"set_names": set_names, "names": ["bob", "jane"]})
    node.render(context)

    # Splatted args are a tuple
    assert context["names"] == ("bob", "jane")


def test_args():
    def set_names(*names):
        return names[0] + " - " + names[1]

    token = Token(TokenType.BLOCK, contents="call set_names(*names) as result")
    node = do_call(None, token)

    context = RenderContext({"set_names": set_names, "names": ["bob", "jane"]})
    node.render(context)

    assert context["result"] == "bob - jane"


def test_args_2():
    def set_names(name1, name2):
        return name1 + " + " + name2

    token = Token(TokenType.BLOCK, contents="call set_names(*names) as result")
    node = do_call(None, token)

    context = RenderContext({"set_names": set_names, "names": ["bob", "jane"]})
    node.render(context)

    assert context["result"] == "bob + jane"


def test_args_ints():
    def multiply(*args):
        product = 1

        for a in args:
            product *= a

        return product

    token = Token(TokenType.BLOCK, contents="call multiply(*products) as result")
    node = do_call(None, token)

    context = RenderContext({"multiply": multiply, "products": [2, 3]})
    node.render(context)

    assert context["result"] == 6


def test_args_ints_2():
    def multiply(*args):
        product = 1

        for a in args:
            product *= a

        return product

    token = Token(TokenType.BLOCK, contents="call multiply(*[2, 4]) as result")
    node = do_call(None, token)

    context = RenderContext({"multiply": multiply})
    node.render(context)

    assert context["result"] == 8


def test_kwargs():
    def set_names(**kwargs):
        return kwargs["first_name"] + " " + kwargs["last_name"]

    token = Token(TokenType.BLOCK, contents="call set_names(**names) as result")
    node = do_call(None, token)

    context = RenderContext({"set_names": set_names, "names": {"first_name": "sue", "last_name": "smith"}})
    node.render(context)

    assert context["result"] == "sue smith"


def test_kwargs_2():
    def set_names(**kwargs):
        return kwargs["first_name"] + " " + kwargs["last_name"]

    token = Token(
        TokenType.BLOCK, contents="call set_names(**{'first_name': 'rachel', 'last_name': 'jones'}) as result"
    )
    node = do_call(None, token)

    context = RenderContext({"set_names": set_names})
    node.render(context)

    assert context["result"] == "rachel jones"


def test_chained_functions():
    class TestObject:
        def __init__(self, first_value):
            self.first_value = first_value

        def second(self, second_value):
            return f"{self.first_value} | {second_value}!"

    def first(first_value):
        return TestObject(first_value)

    token = Token(TokenType.BLOCK, contents="call first('rachel').second('jones') as result")
    node = do_call(None, token)

    context = RenderContext({"first": first})
    node.render(context)

    assert context["result"] == "rachel | jones!"


# def test_model():
#     token = Token(TokenType.BLOCK, contents="call Model.objects.filter(id=1).first() as result")
#     node = do_call(None, token)

#     context = RenderContext({"Model": Model})
#     node.render(context)

#     assert context["result"] == "rachel | jones!"
