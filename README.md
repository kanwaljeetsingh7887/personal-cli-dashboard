# Personal CLI Dashboard

## Description
A terminal-based dashboard that shows live system stats (CPU, Memory, Disk, Battery), weather updates, and optionally Google Calendar events.  
It also logs system stats automatically for monitoring purposes. 

---

## Tools / Technologies Used
- Python 3  
- psutil  
- requests  
- rich  
- python-dotenv  
- Google Calendar API  
- OpenWeatherMap API  
- Ubuntu/Linux  

---

## Features
- 📊 Live CPU, Memory, Disk stats  
- 🔋 Battery % and charging status  
- 🌦️ Weather updates for your city  
- 📝 Automatic logging of system stats (`stats_log.csv`)  
- 📅 Optional Google Calendar integration  

---

## How to Run

```bash
# Clone the repo
git clone https://github.com/kanwaljeetsingh7887/personal-cli-dashboard
cd personal-cli-dashboard

# Create virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Create .env file and add API keys
cp .env.example .env
nano .env  # Add OPENWEATHER_API_KEY, CITY, GOOGLE_CREDENTIALS etc.

# Run the dashboard
python -m src.dashboard
