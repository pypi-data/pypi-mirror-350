import pytest

from jmq_olt_huawei.ma56xxt import APIMA56XXT, UserBusyError


class DummyTelnet:
    """
    Dummy Telnet-like object to attach to APIMA56XXT.tn for testing.
    """
    def __init__(self):
        self.buffer = b''

    def read_until(self, expected, timeout=None):
        # Return empty bytes by default
        return b''

    def write(self, data):
        # No-op for testing writes
        pass

    def close(self):
        # No-op for closing
        pass


def make_api(debug=False):
    """
    Helper to create an APIMA56XXT instance with a DummyTelnet attached.
    """
    api = APIMA56XXT(
        host='dummy', user='user', password='pass', prompt='PROMPT', debug=debug
    )
    api.tn = DummyTelnet()
    return api


def test_parse_port_block_basic():
    api = make_api()
    slot = '1'
    block = (
        "  0/1/2  EXTRA_TEXT\n"
        "    Optical Module status : Online\n"
        "    Port state           : Up\n"
        "    Laser state          : On\n"
        "    Available bandwidth  : 2.5G\n"
        "    Temperature          : 40C\n"
        "    TX Bias              : 4mA\n"
        "    Supply Voltage       : 3.3V\n"
        "    TX power             : -1.5dBm\n"
        "    Illegal rogue ONT    : None\n"
        "    Max Distance         : 15km\n"
        "    Wave length          : 1310nm\n"
        "    Fiber type           : SM\n"
        "    Length               : 1km\n"
    )
    result = api._parse_port_block(slot, block)

    # Verify parsed values
    assert result is not None
    assert result['id'] == 2
    assert result['optical_state'] == 'Online'
    assert result['port_state'] == 'Up'
    assert result['laser_state'] == 'On'
    assert result['bw'] == '2.5G'
    assert result['temperature'] == '40C'
    assert result['tx_bias'] == '4mA'
    assert result['voltage'] == '3.3V'
    assert result['tx_power'] == '-1.5dBm'
    assert result['illegal_rogue_ont'] == 'None'
    assert result['max_distance'] == '15km'
    assert result['wave_length'] == '1310nm'
    assert result['fiber_type'] == 'SM'
    assert result['length'] == '1km'

    print("test_parse_port_block_basic passed")


def test_scan_all(monkeypatch):
    api = make_api()
    # Mock get_slots to return two slots
    monkeypatch.setattr(api, 'get_slots', lambda: [('1', 'GPBD'), ('2', 'OTHER')])

    # Prepare ports: one online, one offline
    port_online = {'id': 10, 'optical_state': 'Online'}
    port_offline = {'id': 11, 'optical_state': 'Offline'}
    monkeypatch.setattr(api, 'get_ports', lambda slot: [port_online.copy(), port_offline.copy()])

    # Mock get_onts to return a list per port
    monkeypatch.setattr(api, 'get_onts', lambda slot, pid: [{'id': pid, 'sn': f'SN{pid}'}])

    result = api.scan_all()

    # Validate first slot (GPBD)
    slot1 = result[0]
    assert slot1['id'] == '1'
    assert slot1['tipo'] == 'GPBD'
    assert len(slot1['ports']) == 2

    # Online port should have 'onts'
    online_port = next(p for p in slot1['ports'] if p['id'] == 10)
    assert 'onts' in online_port
    assert online_port['onts'] == [{'id': 10, 'sn': 'SN10'}]

    # Offline port should not have 'onts'
    offline_port = next(p for p in slot1['ports'] if p['id'] == 11)
    assert 'onts' not in offline_port

    # Validate second slot (OTHER)
    slot2 = result[1]
    assert slot2['id'] == '2'
    assert slot2['tipo'] == 'OTHER'
    assert slot2['ports'] == []

    print("test_scan_all passed")


def test_read_until_prompt_raises_userbusy():
    api = make_api()
    # Simulate busy message on first read
    api._read_line = lambda: 'Reenter times have reached the upper limit'
    # Prevent real disconnect side-effects
    api.disconnect = lambda: None

    with pytest.raises(UserBusyError):
        api._read_until_prompt()
    print("test_read_until_prompt_raises_userbusy passed")


def test_get_slots_simulation():
    api = make_api()
    # Simulated output of `display board 0`
    board_output = (
        "  -------------------------------------------------------------------------\n"
        "  SlotID  BoardName  Status          SubType0 SubType1    Online/Offline\n"
        "  -------------------------------------------------------------------------\n"
        "  0       H806GPBD   Normal                           \n"
        "  6       H802SCUN   Active_normal                    \n"
        "  7       H802SCUN   Standby_failed                   Online   \n"
        "  9       H801GICF   Normal                           \n"
        "  -------------------------------------------------------------------------"
    )
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(api, '_send', lambda cmd: None)
    monkeypatch.setattr(api, '_read_until_prompt', lambda: board_output)

    slots = api.get_slots()
    assert slots == [
        ('0', 'GPBD'),
        ('6', 'SCUN'),
        ('7', 'SCUN'),
        ('9', 'GICF')
    ]
    print("test_get_slots_simulation passed")
    monkeypatch.undo()


def test_get_ports_simulation():
    api = make_api()
    # Simulated port state output for slot '0'
    port_output = (
        "  ----------------------------------------------------------------------------\n"
        "  F/S/P                        0/0/0\n"
        "  Optical Module status        Online\n"
        "  Port state                   Offline\n"
        "  ----------------------------------------------------------------------------"
    )
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(api, '_send', lambda cmd: None)
    # First call to _read_until_prompt() after 'interface' returns empty header, second call returns port_output
    responses = iter(["", port_output, ""])
    monkeypatch.setattr(api, '_read_until_prompt', lambda: next(responses))

    ports = api.get_ports('0')
    assert len(ports) == 1
    p = ports[0]
    assert p['id'] == 0
    assert p['optical_state'] == 'Online'
    assert p['port_state'] == 'Offline'
    print("test_get_ports_simulation passed")
    monkeypatch.undo()


def test_get_onts_simulation():
    api = make_api()
    # Simulated ONT info output for port 0
    ont_output = (
        "  -----------------------------------------------------------------------------\n"
        "  F/S/P   ONT         SN         Control     Run      Config   Match    Protect\n"
        "          ID                     flag        state    state    state    side \n"
        "  -----------------------------------------------------------------------------\n"
        "  0/ 0/0    0  485754431CC32E32  active      offline  initial  initial  no \n"
        "  0/ 0/0    1  485754438D23273E  active      offline  initial  initial  no \n"
        "  -----------------------------------------------------------------------------\n"
        "  F/S/P   ONT-ID   Description\n"
        "  -----------------------------------------------------------------------------\n"
        "  0/ 0/0       0   aGIS: \n"
        "  0/ 0/0       1   aGIS: \n"
    )
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(api, '_send', lambda cmd: None)
    monkeypatch.setattr(api, '_read_until_prompt', lambda: ont_output)

    onts = api.get_onts('0', 0)
    assert len(onts) == 2
    assert onts[0]['id'] == 0 and onts[0]['sn'] == '485754431CC32E32'
    # Strip trailing whitespace from description for comparison
    assert onts[0]['description'].strip() == 'aGIS:'
    assert onts[1]['description'].strip() == 'aGIS:'
    print("test_get_onts_simulation passed")
    monkeypatch.undo()
