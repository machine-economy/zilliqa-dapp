from unittest import mock

def test_mock():
  m = mock.Mock()
  m.return_value = 42
  assert m() == 42
