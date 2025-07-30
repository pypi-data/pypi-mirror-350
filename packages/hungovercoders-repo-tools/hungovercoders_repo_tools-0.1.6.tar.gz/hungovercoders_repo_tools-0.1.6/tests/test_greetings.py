from hungovercoders_repo_tools.greetings import hello

def test_hello(capsys):
    hello()
    out, err = capsys.readouterr()
    assert "Hello from hungovercoders-repo-tools!" in out
