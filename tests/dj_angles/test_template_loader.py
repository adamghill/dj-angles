from types import SimpleNamespace

from django.template import Engine

from dj_angles.template_loader import Loader


def test_get_contents_returns_original_when_no_angles(tmp_path):
    html = "<div>hello</div>\n"
    template_path = tmp_path / "plain.html"
    template_path.write_text(html, encoding="utf-8")

    engine = Engine()
    loader = Loader(engine=engine)
    origin = SimpleNamespace(name=str(template_path))

    actual = loader.get_contents(origin)

    assert actual == html


def test_get_contents_converts_when_angles_present(tmp_path):
    expected = "{% debug %}"

    template_path = tmp_path / "has_angles.html"
    html = "<dj-debug />"
    template_path.write_text(html, encoding="utf-8")

    engine = Engine()
    loader = Loader(engine=engine)
    origin = SimpleNamespace(name=str(template_path))

    actual = loader.get_contents(origin)

    assert expected == actual
