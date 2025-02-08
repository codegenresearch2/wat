def test_inspect_primitive_var():
    output = inspect_format(None)
    assert strip_ansi_colors(output) == "value: None\ntype: NoneType"

    output = inspect_format([5])
    assert strip_ansi_colors(output) == "value: [\n    5,\n]\ntype: list\nlen: 1\n\nPublic attributes:..."

    output = inspect_format([5], dunder=True)
    assert "def __eq__(value, /) # Return self==value." in strip_ansi_colors(output)

    output = inspect_format('poo', short=True)
    assert_multiline_match(output, r'''value: 'poo'\ntype: str\nlen: 3''')

# Additional test cases for other functions and classes would follow similarly.