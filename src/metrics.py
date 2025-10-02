import psutil
from datetime import datetime

def get_system_stats():
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    # Battery info
    battery = psutil.sensors_battery()
    if battery:
        batt_percent = battery.percent
        charging = battery.power_plugged
    else:
        batt_percent = "N/A"
        charging = "N/A"

    return {
        'cpu': round(cpu, 1),
        'memory': round(mem, 1),
        'disk': round(disk, 1),
        'battery': batt_percent,
        'charging': charging,
        'timestamp': datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")  # 12-hour format with AM/PM
    }
