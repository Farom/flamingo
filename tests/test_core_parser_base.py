def test_base_parser_import():
    from flamingo.core.parser import ContentParser  # NOQA


def test_basic_meta_data_parsing(flamingo_dummy_context):
    from flamingo.core.parser import ContentParser
    from flamingo.core.data_model import Content

    raw_content = """
    a: content of a
    b: content of b
    c:
        a, b, c


    content
    """

    parser = ContentParser(flamingo_dummy_context)
    content = Content()

    parser.parse(raw_content, content)

    assert sorted(list(content.data.keys())) == ['a', 'b', 'c', 'content_body',
                                                 'content_offset']

    assert content['a'] == 'content of a'
    assert content['b'] == 'content of b'
    assert content['c'].strip() == 'a, b, c'

    assert content['content_body'] == 'content'

    # test with whitespaces
    raw_content = """
    a: content of a
    b: content of b
    c:
        a, b, c
        

    content
    """  # NOQA

    parser = ContentParser(flamingo_dummy_context)
    content = Content()

    parser.parse(raw_content, content)

    assert sorted(list(content.data.keys())) == ['a', 'b', 'c', 'content_body',
                                                 'content_offset']

    assert content['a'] == 'content of a'
    assert content['b'] == 'content of b'
    assert content['c'].strip() == 'a, b, c'

    assert content['content_body'] == 'content'


def test_meta_data_blocks(flamingo_dummy_context):
    from flamingo.core.parser import ContentParser
    from flamingo.core.data_model import Content

    # default block
    raw_content = """
    a: content of a
    b: content of b

    c: content of c


    content
    """

    parser = ContentParser(flamingo_dummy_context)
    content = Content()

    parser.parse(raw_content, content)

    assert sorted(list(content.data.keys())) == ['a', 'b', 'c', 'content_body',
                                                 'content_offset']

    assert content['a'] == 'content of a'
    assert content['b'] == 'content of b'
    assert content['c'] == 'content of c'
    assert content['content_body'] == 'content'

    # simple block
    raw_content = """
    a: content of a
    b: content of b
    c: content of c

    content
    """

    parser = ContentParser(flamingo_dummy_context)
    content = Content()

    parser.parse(raw_content, content)

    assert sorted(list(content.data.keys())) == ['a', 'b', 'c', 'content_body',
                                                 'content_offset']

    assert content['a'] == 'content of a'
    assert content['b'] == 'content of b'
    assert content['c'] == 'content of c'
    assert content['content_body'] == 'content'

    raw_content = """
    a: content of a
    b: content of b

    c: content of c

    real content
    """

    parser = ContentParser(flamingo_dummy_context)
    content = Content()

    parser.parse(raw_content, content)

    assert sorted(list(content.data.keys())) == ['a', 'b', 'content_body',
                                                 'content_offset']

    assert content['a'] == 'content of a'
    assert content['b'] == 'content of b'
    assert content['content_body'].startswith('c: content of c\n')
    assert content['content_body'].endswith('real content')

    # no meta data
    raw_content = """
    real content1
    real content2
    """

    parser = ContentParser(flamingo_dummy_context)
    content = Content()

    parser.parse(raw_content, content)

    assert sorted(list(content.data.keys())) == ['content_body',
                                                 'content_offset']

    assert content['content_body'].startswith('real content1')
    assert content['content_body'].endswith('real content2')

    raw_content = """
    real content1

    real content2
    """

    parser = ContentParser(flamingo_dummy_context)
    content = Content()

    parser.parse(raw_content, content)

    assert sorted(list(content.data.keys())) == ['content_body',
                                                 'content_offset']

    assert content['content_body'].startswith('real content1')
    assert content['content_body'].endswith('real content2')

    raw_content = """
    real content1


    real content2
    """

    parser = ContentParser(flamingo_dummy_context)
    content = Content()

    parser.parse(raw_content, content)

    assert sorted(list(content.data.keys())) == ['content_body',
                                                 'content_offset']

    assert content['content_body'].startswith('real content1')
    assert content['content_body'].endswith('real content2')


def test_content_offsets(flamingo_env):
    flamingo_env.write('/content/a.rst', """
    a: 1
    b: 2

    foo
    ===
    """)

    flamingo_env.write('/content/b.rst', """
    a: 1
    b: 2


    foo
    ===
    """)

    flamingo_env.write('/content/c.rst', """
    foo
    ===
    """)

    flamingo_env.write('/content/d.rst', """
    foo


    foo
    ===
    """)

    flamingo_env.build()
    contents = flamingo_env.context.contents

    assert contents.get(path='a.rst')['content_offset'] == 4
    assert contents.get(path='b.rst')['content_offset'] == 5
    assert contents.get(path='c.rst')['content_offset'] == 0
    assert contents.get(path='d.rst')['content_offset'] == 0
