from jinja2 import Template, Environment


def test_no_extension():
    template = Template('foo {{ bar }}')
    result = template.render(bar="foo")
    assert result == "foo foo"


def test_extension1():
    env = Environment(extensions=["jinja2_fnmatch_extension.FnMatchExtension"])
    template = env.from_string("test {{ \"foo-bar\"|fnmatch(\"foo-*\") }}")
    result = template.render()
    assert result == "test True"
