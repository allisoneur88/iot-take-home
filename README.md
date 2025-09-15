## 📦 Requirements

- Python 3.9 or newer
- Docker + Docker Compose

Python dependencies are listed in `requirements.txt`

## ▶️ Running Instructions
### 1. Clone the Repo

```bash
git clone https://github.com/allisoneur88/iot-take-home.git
cd iot-take-home 

```

### 2. Start MQTT
```bash
docker compose up
```

### 3. Setup Python environment

### macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bit/activate
```

### Windows(Powershell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Intall Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
### 4. Run the app
```bash
python main.py
```

## Testing Pub
Requires mosquitto installed locally
```bash
mosquitto_pub -h localhost -p 1883 -t "m/MES/UnitsProduced" -m '{"units": 42}'
```
