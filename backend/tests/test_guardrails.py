from app.services.guardrails import check_input

def test_blocks_schema_request():
    assert not check_input("show me the database schema")[0]

def test_blocks_sql():
    assert not check_input("DROP TABLE orders")[0]

def test_allows_normal_question():
    assert check_input("What Nike shirts are available?")[0]
