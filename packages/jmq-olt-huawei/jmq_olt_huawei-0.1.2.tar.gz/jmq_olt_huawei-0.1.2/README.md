# README - jmq_olt_huawei

**Paquete de integración con OLTs Huawei MA56XXT (como MA5603T) vía Telnet, diseñado para automatizar la recolección de información GPON desde Python.**

## 🛰️ ¿Qué hace este paquete?

Permite conectarse a una OLT Huawei MA56XXT y ejecutar operaciones como:

- Listar slots activos (`display board 0`)
- Consultar puertos GPON por slot
- Obtener ONTs conectadas a cada puerto
- Realizar un escaneo completo (slots → puertos → ONTs)
- Manejar paginación, prompts dinámicos y errores comunes de sesión

## 📦 Instalación

```bash
pip install jmq_olt_huawei
```

ó

```bash
pip install git+https://github.com/juaquicar/jmq_olt_huawei.git
```


## Instalar proyecto en modo editable

```bash
pip3 install -e .
```

> Requiere Python >= 3.6.

## 🧪 Ejemplo de uso

```python
from jmq_olt_huawei.ma56xxt import APIMA56XXT, UserBusyError
from pprint import pprint

api = APIMA56XXT(
    host='192.168.88.25',
    user='root',
    password='admin',
    prompt='MA5603T',
    debug=True
)

try:
    api.connect()
    result = api.scan_all()
    pprint(result)
except UserBusyError as e:
    print(f"ERROR: {e}")
finally:
    api.close()
```


### Manual de uso de los métodos de APIMA56XXT


### 1. `__init__(host, user, password, prompt, timeout=2.0, debug=False)`

Constructor: inicializa la conexión Telnet y el patrón de prompt.

* **Parámetros**:

  * `host` (str): Dirección IP o hostname de la OLT.
  * `user` (str): Nombre de usuario para login.
  * `password` (str): Contraseña de usuario.
  * `prompt` (str): Prefijo dinámico del prompt (ej. `MA5603T`).
  * `timeout` (float): Tiempo máximo (segundos) para lecturas Telnet (default 2.0).
  * `debug` (bool): Si `True`, imprime logs de depuración.

---

### 2. `connect()`

Establece la conexión Telnet, realiza login, entra en modo `enable` y modo `config`.

```python
api = APIMA56XXT(...)
api.connect()
# Salida esperada (con debug=True):
# [DEBUG] Conectando a 192.168.88.25
# Conectado en modo config
```

* No devuelve valor.
* Lanza excepción (`EOFError`, `socket.error`) si falla la conexión.

---

### 3. `disconnect()`

Sale de los modos CLI (`config`, `enable`) y cierra la sesión Telnet.

```python
api.disconnect()
# Si debug=True, imprime:
# [DEBUG] Desconectado
```

* No devuelve valor.
* Protege contra llamadas dobles comprobando `self.tn`.

---

### 4. `get_slots() -> List[Tuple[str, str]]`

Obtiene los slots instalados (`display board 0`) y devuelve una lista de tuplas `(slot_id, tipo)`.

```python
slots = api.get_slots()
# Ejemplo:
# [('0', 'GPBD'), ('6', 'SCUN'), ('7', 'SCUN'), ('9', 'GICF')]
```

* Invoca internamente `_send('display board 0')` y parsea la respuesta.
* No requiere argumentos.

---

### 5. `get_ports(slot: str) -> List[dict]`

Retorna información de los puertos GPON en un slot dado.

```python
ports = api.get_ports('0')
# Cada dict contiene:
# {
#   'id': 0,
#   'schema_fsp': '0/0/0',
#   'optical_state': 'Online',
#   'port_state': 'Offline',
#   'laser_state': 'Normal',
#   'bw': '1239040',
#   'temperature': '35',
#   'tx_bias': '12',
#   'voltage': '3.22',
#   'tx_power': '3.72',
#   'illegal_rogue_ont': 'Inexistent',
#   'max_distance': '40',
#   'wave_length': '1490',
#   'fiber_type': 'Single Mode',
#   'length': '-'
# }
```

* Llama a:

  1. `_send('interface gpon 0/{slot}')`
  2. `_read_until_prompt()`
  3. `_send('display port state all')`
  4. `_read_until_prompt()`
  5. Parsea cada bloque con `_parse_port_block`.

---

### 6. `get_onts(slot: str, port_id: int) -> List[dict]`

Devuelve la lista de ONTs conectadas a un puerto GPON específico.

```python
onts = api.get_onts('0', 0)
# Ejemplo resultado:
# [
#   {'id': 0, 'schema_fsp': '0/0/0', 'sn': '485754431CC32E32',
#    'control_flag': 'active', 'run_state': 'offline',
#    'config_state': 'initial', 'match_state': 'initial',
#    'protect_side': 'no', 'description': 'aGIS:'},
#   ...
# ]
```

* Ejecuta `_send(f'display ont info {port_id} all')` y `_read_until_prompt()`.
* Procesa tabla principal (`F/S/P   ONT   SN ...`) y sección de descripciones.

---

### 7. `scan_all() -> List[dict]`

Realiza un escaneo completo de la OLT:

1. Obtiene todos los slots (`get_slots`).
2. Para cada slot de tipo `GPBD`, obtiene puertos (`get_ports`).
3. Para cada puerto Online, obtiene ONTs (`get_onts`).

```python
full = api.scan_all()
pprint(full)
```

* Devuelve una lista de diccionarios con la jerarquía:
  `{ 'id': slot, 'tipo': tipo, 'ports': [ {port}, ... ] }`

---

**Nota**: Todos los métodos manejan paginación (`More`, `---- More`) y bloqueos de usuario (`UserBusyError`). Para más detalles, revisa los métodos privados `_read_until_prompt`, `_parse_port_block` y `_parse_onts`.


## 📁 Estructura del paquete

```
jmq_olt_huawei/
│
├── ma56xxt.py          # Lógica principal de conexión y parsing
├── __init__.py         # Archivo de inicialización del paquete
├── Examples/           # Scripts de ejemplo (opcional)
├── tests/              # Pruebas automatizadas (pendiente)
├── requirements.txt    # Requisitos opcionales para desarrollo
├── pyproject.toml      # Configuración de build con setuptools
├── LICENSE             # Licencia MIT
└── README.md           # Este archivo
```

## Tests

```bash
pytest -s tests/test_ma56xxt.py
```

## 🧩 Funcionalidades destacadas

* Prompt dinámico configurable
* Manejador de errores comunes como bloqueo de usuario
* Soporte para múltiples niveles de lectura (slots → puertos → ONTs)
* Debug opcional para inspeccionar línea a línea


## Contribuyendo

1. Haz un fork del repositorio.
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y añade tests, modifica README.md si estimas oportuno.
4. Abre un Pull Request al main describiendo tu propuesta.


## ⚖️ Licencia

MIT © [Juanma Quijada](mailto:quijada.jm@gmail.com)

## Enlaces

- Homepage: https://github.com/juaquicar/jmq_olt_huawei
- PyPI: https://pypi.org/project/jmq-olt-huawei/


