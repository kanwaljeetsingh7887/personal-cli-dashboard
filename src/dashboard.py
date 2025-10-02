import os
import time
from dotenv import load_dotenv

from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.align import Align
from rich import box

from src.metrics import get_system_stats
from src.weather import get_weather
from src.logger import log_stats
from src.gcal import get_creds, get_next_event

#contributor kanwaljeet
load_dotenv()

OPENWEATHER_KEY = os.getenv('OPENWEATHER_API_KEY')
CITY = os.getenv('CITY', 'Mumbai,IN')
CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS', 'credentials.json')
TOKEN_PATH = os.getenv('TOKEN_PATH', 'token.json')
CSV_PATH = os.getenv('LOG_CSV', 'stats_log.csv')
REFRESH = int(os.getenv('REFRESH', '60'))  # seconds

def make_system_panel(stats):
    t = Table.grid()
    t.add_row(f"[b]CPU:[/b] {stats['cpu']}%")
    t.add_row(f"[b]Memory:[/b] {stats['memory']}%")
    t.add_row(f"[b]Disk:[/b] {stats['disk']}%")
    if stats.get('battery') is not None:
        charging_status = "⚡ Charging" if stats['charging'] else "🔋 Discharging"
        t.add_row(f"[b]Battery:[/b] {stats['battery']}% {charging_status}")
    return Panel(t, title="System Stats")

def make_weather_panel(weather):
    t = Table.grid(expand=True)
    t.add_column()
    if not weather:
        t.add_row("Weather: N/A")
    else:
        t.add_row(f"[b]{weather['desc']}[/b]")
        t.add_row(f"Temp: {weather['temp']}°C (Feels {weather['feels_like']}°C)")
        t.add_row(f"Humidity: {weather['humidity']}%  Wind: {weather['wind']} m/s")
    return Panel(t, title="Weather", box=box.ROUNDED)

def make_calendar_panel(event):
    t = Table.grid(expand=True)
    t.add_column()
    if not event:
        t.add_row("No upcoming events")
    else:
        t.add_row(f"[b]{event['summary']}[/b]")
        t.add_row(f"Starts: {event['start']}")
        if event.get('link'):
            t.add_row(f"[link={event['link']}]Open in Calendar[/link]")
    return Panel(t, title="Next Calendar Event", box=box.ROUNDED)

def build_layout(stats, weather, event):
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=1)
    )
    layout["body"].split_row(
        Layout(name="left", ratio=1),
        Layout(name="right", ratio=1)
    )
    layout["header"].update(Align.center("[b]Personal CLI Dashboard[/b]", vertical="middle"))
    layout["left"].update(make_system_panel(stats))
    right = Layout()
    right.split_column(Layout(name="weather", ratio=1), Layout(name="calendar", ratio=1))
    right["weather"].update(make_weather_panel(weather))
    right["calendar"].update(make_calendar_panel(event))
    layout["right"].update(right)
    layout["footer"].update(Align.center("Press Ctrl+C to quit"))
    return layout

def main():
    creds = None
    try:
        creds = get_creds(CREDENTIALS_PATH, TOKEN_PATH)
    except Exception:
        print("Google Calendar: credentials or token missing / auth canceled. Calendar will be disabled.")
    with Live(refresh_per_second=4, screen=True) as live:
        while True:
            stats = get_system_stats()
            try:
                weather = get_weather(OPENWEATHER_KEY, CITY)
            except Exception:
                weather = None
            event = None
            if creds:
                try:
                    event = get_next_event(creds)
                except Exception:
                    event = None
            log_stats(CSV_PATH, stats)
            layout = build_layout(stats, weather, event)
            live.update(layout)
            time.sleep(REFRESH)

if __name__ == "__main__":
    main()
