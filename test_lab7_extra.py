import pytest
import library
from user import User


@pytest.fixture
def biblioteca():
    return library.Library()


def test_fixture_biblioteca_vacia(biblioteca):
    assert biblioteca.books == []
    assert biblioteca.users == []


@pytest.mark.parametrize("user_id", ["0001", "ID0001", "9999"])
def test_parametrize_usuario_no_registrado(biblioteca, user_id):
    with pytest.raises(ValueError, match="^User not found$"):
        biblioteca._find_user(user_id)


def test_capsys_prestamos_desactivados(biblioteca, monkeypatch, capsys):
    monkeypatch.setitem(library.settings, "loans_enabled", False)

    resultado = biblioteca.borrow_book("0001", "ISBN001")
    salida = capsys.readouterr()

    assert salida.out == "Loans are disabled\n"
    assert resultado is None
    assert biblioteca.books == []
    assert biblioteca.users == []


def test_setattr_configuracion_prestamos(biblioteca, monkeypatch):
    monkeypatch.setattr(library, "settings", {"loans_enabled": True})

    with pytest.raises(ValueError, match="^User not found$"):
        biblioteca.borrow_book("0001", "ISBN001")


def test_delattr_historial_usuario(monkeypatch):
    usuario = User("Paulo", "0001")
    monkeypatch.delattr(usuario, "history")

    with pytest.raises(AttributeError, match="history"):
        usuario.get_history()
