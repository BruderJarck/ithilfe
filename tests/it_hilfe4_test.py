from it_hilfe import it_hilfe4
from pytest import fixture, raises, mark


@fixture(scope="function")
def create_single_register():
    new = it_hilfe4.WindowsLapTop(1, "maurice")
    new.OS = "Win7"
    it_hilfe4.registered_devices[new.name] = new


def test_device():
    dev1 = it_hilfe4.Device("1", "Maurice")
    assert dev1.name == "1"
    assert dev1.user == "Maurice"
    assert dev1.OS == None


def test_windowsLapTop():
    dev1 = it_hilfe4.WindowsLapTop("1", "Maurice")
    assert dev1.name == "1"
    assert dev1.user == "Maurice"


def test_macbook():
    dev1 = it_hilfe4.Macbook("2", "Maurice")
    assert dev1.name == "2"
    assert dev1.user == "Maurice"


def test_WinWorkStation():
    dev1 = it_hilfe4.WindowsWorkStation("3", "Maurice")
    assert dev1.name == "3"
    assert dev1.user == "Maurice"


def test_getAvialable(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: 1)
    assert it_hilfe4.get_available([1, 2, 3]) == 1

    with raises(IndexError):
        monkeypatch.setattr("builtins.input", lambda _: 4)
        it_hilfe4.get_available([1, 2, 3])


@mark.parametrize("test_input,expected",
                  [([1, 1, "maurice", 1], '0, 1, maurice, Win10'),
                   ([2, 2, "Peter", 1], "1, 2, Peter, Win10"),
                   ([3, 3, "Heinz"], "2, 3, Heinz, MacOS"),
                   ([1, 1, "maurice", 1], '\x1b[91malready taken dev name\n\x1b[0m')])
def test_register(monkeypatch, test_input, expected):
    inputlist = test_input
    monkeypatch.setattr("builtins.input", lambda _x: inputlist.pop(0))
    assert it_hilfe4.register() == expected


def test_view(create_single_register):
    assert it_hilfe4.view() == ('device name: 1, username: maurice, OS: Win7, largerBattery: True, ' 'upgradedCPU: False, devtype: WindowsLapTop,\n')

    it_hilfe4.registered_devices.clear()

    assert it_hilfe4.view() == "no device registered yet\n"


@mark.parametrize("test_input,expected", [
    ([1, 1, "peter"], ('device name: 1, username: peter, OS: Win7, largerBattery: True, upgradedCPU: ' 'False, devtype: WindowsLapTop,')),
    ([1, 2, 2],('device name: 1, username: maurice, OS: Win7, largerBattery: True, ' 'upgradedCPU: False, devtype: WindowsLapTop,')),
    ([1, 3, False], ('device name: 1, username: maurice, OS: Win7, largerBattery: True, ' 'upgradedCPU: False, devtype: WindowsLapTop,')),
    ([1, 4, True], ('device name: 1, username: maurice, OS: Win7, largerBattery: True, ' 'upgradedCPU: False, devtype: WindowsLapTop,'))])
def test_change(test_input, expected, create_single_register, monkeypatch):

    monkeypatch.setattr("builtins.input", lambda _x: test_input[2])
    assert str(it_hilfe4.change_param(test_input[0], test_input[1])) == expected


def test_search(create_single_register):
    assert it_hilfe4.search("maurice") == ['match found: device name: 1, username: maurice, OS: Win7, largerBattery: ' 'True, upgradedCPU: False, devtype: WindowsLapTop,\n']

    assert it_hilfe4.search("Heinz") == ['\nno match found\n']

    it_hilfe4.registered_devices.clear()

    assert it_hilfe4.search("maurice") == ["\nno devices registered yet\n"]
