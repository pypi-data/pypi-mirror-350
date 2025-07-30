# ma56xxt.py

import telnetlib
import re
from pprint import pprint


class UserBusyError(Exception):
    """Raised when the OLT indicates the user login attempts are blocked."""
    pass


class APIMA56XXT:
    """
    Clase para conectarse a una OLT vía Telnet y obtener:
      - Slots (tarjetas PON)
      - Puertos GPON de un slot
      - ONTs de un puerto
      - Flujo completo de escaneo
    Maneja prompts dinámicos, paginación y confirmaciones.
    """

    def __init__(
        self,
        host: str,
        user: str,
        password: str,
        prompt: str,
        timeout: float = 2.0,
        debug: bool = False,
    ):
        self.host = host
        self.user = user
        self.password = password
        self.timeout = timeout
        self.debug = debug
        self.tn = None
        # Regex para detectar prompt dinámico: MA5603T>, MA5603T(config)#, etc.
        pattern = rf"^{re.escape(prompt)}(?:\([^)]+\))?[>#]"
        self.prompt_re = re.compile(pattern)

    def _log(self, *args):
        if self.debug:
            print("[DEBUG]", *args)

    def _read_line(self) -> str:
        raw = self.tn.read_until(b"\n", timeout=self.timeout)
        text = raw.decode("utf-8", errors="ignore")
        return re.sub(r"\x1b\[[0-9;]*[a-zA-Z]", "", text).rstrip()

    def _read_until_prompt(self) -> str:
        """
        Lee líneas hasta detectar el prompt dinámico,
        manejando paginación, errores o bloqueo de usuario.
        """
        lines = []
        while True:
            line = self._read_line()
            if not line:
                continue
            if "Reenter times have reached the upper limit" in line:
                self._log("Usuario bloqueado: demasiados intentos de reingreso")
                self.close()
                raise UserBusyError("Usuario ocupado: demasiados intentos de login")
            lines.append(line)
            if self.debug:
                print("[DEBUG] →", line)
            if line.startswith('%'):
                break
            if 'More' in line or "Press 'Q'" in line or '---- More' in line:
                self._log("Paginación detectada, ENTER")
                self.tn.write(b"\n")
                continue
            if self.prompt_re.search(line):
                break
        return "\n".join(lines)

    def connect(self):
        """Conecta, hace login, enable y config."""
        self._log("Conectando a", self.host)
        self.tn = telnetlib.Telnet(self.host)
        # Login
        self.tn.read_until(b"User name:", timeout=self.timeout)
        self.tn.write(self.user.encode() + b"\n")
        self.tn.read_until(b"User password:", timeout=self.timeout)
        self.tn.write(self.password.encode() + b"\n")
        # Prompt usuario
        self._read_until_prompt()
        # Enable
        self._send('enable')
        self._read_until_prompt()
        # Config
        self._send('config')
        self._read_until_prompt()
        print("Conectado en modo config")

    def close(self):
        self.tn.close()
        self.tn = None
        self._log("Desconectado")

    def disconnect(self):
        """Sale de config y cierra la conexión Telnet con confirmación."""
        if not self.tn:
            return
        # Quit interfaces
        self._send('quit')
        self._read_until_prompt()
        # Exit config
        self._send('quit')
        self._read_until_prompt()
        # Exit enable (pide confirm)
        self._send('quit')
        try:
            confirm = self.tn.read_until(b"(y/n)", timeout=self.timeout).decode('utf-8', errors='ignore')
            self._log(f"Confirm prompt: {confirm.strip()}")
            self.tn.write(b"y\n")
        except Exception:
            pass
        # Cerrar
        self.tn.close()
        self.tn = None
        self._log("Desconectado")

    def _send(self, cmd: str):
        """Envía un comando sin esperar prompt previo."""
        self._log(f"Enviando comando: {cmd}")
        self.tn.write(cmd.encode() + b"\n")

    def get_slots(self) -> list[tuple[str, str]]:
        """Obtiene lista de (slot, tipo) con 'display board 0'."""
        self._send('display board 0')
        raw = self._read_until_prompt()
        slots = []
        for line in raw.splitlines():
            m = re.match(r"\s*(\d+)\s+H\d+([A-Z]+)", line)
            if m:
                slots.append((m.group(1), m.group(2)))
        return slots

    def get_ports(self, slot: str) -> list[dict]:
        """Obtiene datos de puertos GPON de un slot."""
        self._send(f'interface gpon 0/{slot}')
        self._read_until_prompt()
        self._send('display port state all')
        raw = self._read_until_prompt()
        ports = []
        for bloque in raw.split('F/S/P')[1:]:
            info = self._parse_port_block(slot, bloque)
            if info:
                ports.append(info)
        self._send('quit')
        self._read_until_prompt()
        return ports

    def get_onts(self, slot: str, port_id: int) -> list[dict]:
        self._send(f'interface gpon 0/{slot}')
        self._read_until_prompt()
        """Obtiene lista de ONTs de un puerto GPON."""
        self._send(f'display ont info {port_id} all')
        raw = self._read_until_prompt()
        self._send('quit')
        self._read_until_prompt()
        return self._parse_onts(raw, slot, port_id)

    def scan_all(self) -> list[dict]:
        """Escaneo completo: slots → puertos → ONTs."""
        result = []
        for slot, tipo in self.get_slots():
            entry = {'id': slot, 'tipo': tipo, 'ports': []}
            if tipo == 'GPBD':
                for port in self.get_ports(slot):
                    if port.get('optical_state') == 'Online':

                        port['onts'] = self.get_onts(slot, port['id'])
                    entry['ports'].append(port)
            result.append(entry)
        return result

    def _parse_port_block(self, slot: str, bloque: str) -> dict | None:
        lines = bloque.strip().splitlines()
        m = re.match(rf"\s*0/{re.escape(slot)}/(\d+)", lines[0])
        if not m:
            return None
        pid = int(m.group(1))
        data = {
            'id': pid,
            'schema_fsp': f"0/{slot}/{pid}",
            'optical_state': None,
            'port_state': None,
            'laser_state': None,
            'bw': None,
            'temperature': None,
            'tx_bias': None,
            'voltage': None,
            'tx_power': None,
            'illegal_rogue_ont': None,
            'max_distance': None,
            'wave_length': None,
            'fiber_type': None,
            'length': None,
        }
        for l in lines:
            if 'Optical Module status' in l:
                data['optical_state'] = l.split()[-1]
            elif 'Port state' in l:
                data['port_state'] = l.split()[-1]
            elif 'Laser state' in l:
                data['laser_state'] = l.split()[-1]
            elif 'Available bandwidth' in l:
                data['bw'] = l.split()[-1]
            elif 'Temperature' in l:
                data['temperature'] = l.split()[-1]
            elif 'TX Bias' in l:
                data['tx_bias'] = l.split()[-1]
            elif 'Supply Voltage' in l:
                data['voltage'] = l.split()[-1]
            elif 'TX power' in l:
                data['tx_power'] = l.split()[-1]
            elif 'Illegal rogue ONT' in l:
                data['illegal_rogue_ont'] = l.split()[-1]
            elif 'Max Distance' in l:
                data['max_distance'] = l.split()[-1]
            elif 'Wave length' in l:
                data['wave_length'] = l.split()[-1]
            elif 'Fiber type' in l:
                data['fiber_type'] = l.split()[-1]
            elif 'Length' in l:
                data['length'] = l.split()[-1]
        return data

    def _parse_onts(self, raw: str, slot: str, port_id: int) -> list[dict]:
        """Parseo de info ONTs bajo puerto GPON 0/S/P."""
        onts = []
        lines = raw.splitlines()
        in_main = False
        in_desc = False
        base_fsp = f"0/{slot}/{port_id}"
        for ln in lines:
            # Inicia sección de tabla principal de ONTs
            if ln.startswith('  F/S/P') and 'ONT' in ln and 'SN' in ln:
                in_main = True
                continue
            # Procesar filas de ONTs
            if in_main and ln.strip():
                parts = ln.split()
                # Formato esperado: ['0/', '0/0', 'ONT_ID', 'SN', 'CTRL', 'RUN', 'CFG', 'MATCH', 'PROTECT']
                if len(parts) >= 9 and parts[1].startswith(f"{slot}/"):
                    try:
                        oid = int(parts[2])
                    except ValueError:
                        continue
                    entry = {
                        'id': oid,
                        'schema_fsp': base_fsp,
                        'sn': parts[3],
                        'control_flag': parts[4],
                        'run_state': parts[5],
                        'config_state': parts[6],
                        'match_state': parts[7],
                        'protect_side': parts[8],
                        'description': None
                    }
                    onts.append(entry)
                    continue
            # Cambio a sección de descripciones
            if ln.startswith('  F/S/P') and 'Description' in ln:
                in_desc = True
                in_main = False
                continue
            # Procesar descripciones
            if in_desc and ln.strip():
                parts = ln.split(maxsplit=3)
                if len(parts) == 4 and parts[0].startswith('0/'):
                    try:
                        oid = int(parts[2])
                    except ValueError:
                        continue
                    desc = parts[3]
                    for o in onts:
                        if o['id'] == oid:
                            o['description'] = desc
                            break
        return onts


if __name__ == '__main__':
    api = APIMA56XXT(host='192.168.88.25', user='root', password='admin', prompt='MA5603T', debug=True)
    try:
        api.connect()
        full = api.scan_all()
        pprint(full)
    except UserBusyError as e:
        print(f"ERROR: {e}")
    finally:
#        api.disconnect()
        api.close()
