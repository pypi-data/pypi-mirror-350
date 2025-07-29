import builtins
from collection import load_from_file, main
from pytest_mock import MockerFixture

def test_result_file(mocker: MockerFixture):
    mock_args = mocker.MagicMock()
    mock_args.file = 'test.txt'
    mock_args.string = None
    mocker_parse = mocker.patch('argparse.ArgumentParser.parse_args', return_value = mock_args)
    mocker_open = mocker.patch.object(builtins, 'open', mocker.mock_open(read_data='Mock data'))
    main()
    mocker_parse.assert_called()
    mocker_open.assert_called()

def test_result_string(mocker: MockerFixture):
    mock_args = mocker.MagicMock()
    mock_args.file = None
    mock_args.string = 'aaagjk'
    mocker_parse = mocker.patch('argparse.ArgumentParser.parse_args', return_value = mock_args)
    main()
    mocker_parse.assert_called()