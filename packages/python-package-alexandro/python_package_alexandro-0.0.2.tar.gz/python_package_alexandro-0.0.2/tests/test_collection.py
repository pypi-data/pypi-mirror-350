from collection import occur_once, load_from_file

import pytest
import builtins

@pytest.mark.parametrize('text, result', [('aaaabccccdfg', 4), ('gggpjjazxc', 5)])
def test_result_true(text, result):
    assert occur_once(text) == result

@pytest.mark.parametrize('text, result', [('abcdfg', 4), ('gpjazxc', 5)])
def test_result_false(text, result):
    assert occur_once(text) != result

@pytest.mark.parametrize('text', [1, [1, 2, 3], True, None])
def test_result_type(text):
    with pytest.raises(TypeError):
        occur_once(text)

def test_open_file(mocker):
        mock_open = mocker.patch.object(builtins, 'open', mocker.mock_open(read_data='Mock data'))
        data = load_from_file('test.txt')

        assert data == 'Mock data'
        mock_open.assert_called_once_with('test.txt', 'r')

