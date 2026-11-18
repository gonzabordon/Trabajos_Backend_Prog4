from unittest.mock import patch
import database
from tests.conftest import engine

def test_get_session():
    with patch.object(database, "engine", engine):
        generador = database.get_session()
        sesion = next(generador)
        assert sesion is not None
        try:
            next(generador)
        except StopIteration:
            pass