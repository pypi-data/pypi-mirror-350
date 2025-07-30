import os
import sqlite3
import subprocess
import threading
import pandas as pd
from datetime import datetime
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Button, DataTable, Log, Input, Select, Static
from textual.containers import VerticalScroll
from apscheduler.schedulers.background import BackgroundScheduler

# Configuration
SCRIPT_DIRECTORY = "C:\\Projects\\finceptTerminal\\fincept_terminal\\FinceptAuthModule\\"
DB_FILE = "scheduled_jobs.db"
LOG_FILE = "script_logs.txt"

# Initialize Scheduler
scheduler = BackgroundScheduler()
scheduler.start()

# Store running scripts & start times
running_scripts = {}

# Initialize Database
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS jobs 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, script_path TEXT, hour INTEGER, 
                  minute INTEGER, second INTEGER, frequency TEXT, active INTEGER)''')
    conn.commit()
    conn.close()


init_db()


# Utility Functions
def log_message(message):
    """Logs messages to a file for UI updates."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now()} - {message}\n")


def run_script(script_path):
    """Runs a script asynchronously and updates UI with execution time."""
    def execute():
        start_time = datetime.now()
        running_scripts[script_path] = start_time  # Store start time
        log_message(f"⚡ Running: {script_path} at {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        try:
            subprocess.run(["python", script_path], capture_output=True, text=True)
            log_message(f"✅ Finished: {script_path}")
        except Exception as e:
            log_message(f"❌ Error: {script_path}: {str(e)}")

        del running_scripts[script_path]  # Remove script after completion

    threading.Thread(target=execute, daemon=True).start()


def add_job(script_path, hour, minute, second, frequency):
    """Schedules a script based on frequency."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO jobs (script_path, hour, minute, second, frequency, active) VALUES (?, ?, ?, ?, ?, ?)",
              (script_path, hour, minute, second, frequency, 1))
    conn.commit()
    conn.close()

    log_message(f"📌 Scheduled: {script_path} at {hour}:{minute}:{second} ({frequency})")

    job_id = f"{script_path}_{hour}_{minute}_{second}"
    if frequency == "daily":
        scheduler.add_job(run_script, 'cron', hour=hour, minute=minute, second=second, id=job_id, args=[script_path])
    elif frequency == "weekly":
        scheduler.add_job(run_script, 'interval', weeks=1, id=job_id, args=[script_path])
    elif frequency == "monthly":
        scheduler.add_job(run_script, 'interval', weeks=4, id=job_id, args=[script_path])
    elif frequency.startswith("custom_"):  # e.g., custom_3d
        days = int(frequency.split("_")[1].replace("d", ""))
        scheduler.add_job(run_script, 'interval', days=days, id=job_id, args=[script_path])
    else:
        scheduler.add_job(run_script, 'date', run_date=datetime.now().replace(hour=hour, minute=minute, second=second),
                          id=job_id, args=[script_path])


def get_jobs():
    """Fetches all scheduled jobs."""
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT * FROM jobs", conn)
    conn.close()
    return df


class ScriptSchedulerApp(App):
    """Textual-based script scheduler."""

    CSS = """
    Screen {
        background: #121212;
        color: white;
    }

    Header {
        background: #1e1e1e;
        text-align: center;
        padding: 1;
    }

    Footer {
        background: #1e1e1e;
        padding: 1;
    }

    DataTable {
        border: solid white;
        padding: 1;
    }

    Log {
        height: 20;
        border: solid green;
    }

    Button {
        margin: 1;
        padding: 1;
        background: #007acc;
        border: none;
    }

    Input {
        width: 50;
        margin: 1;
        border: solid white;
    }

    Select {
        width: 50;
        margin: 1;
        border: solid white;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield VerticalScroll(
            Input(id="script_input", placeholder="Enter script filename"),
            Input(id="hour_input", placeholder="Hour (0-23)"),
            Input(id="minute_input", placeholder="Minute (0-59)"),
            Input(id="second_input", placeholder="Second (0-59)"),
            Select(
                [
                    ("Once", "once"),
                    ("Daily", "daily"),
                    ("Weekly", "weekly"),
                    ("Monthly", "monthly"),
                    ("Custom", "custom")
                ],
                id="frequency_input"
            ),
            Button("➕ Schedule Script", id="schedule_button"),
            Button("▶ Run Selected Script", id="run_button"),
            Button("🗑 Remove Job ", id="remove_button"),
            DataTable(id="job_table"),
            Static("⏳ Running Scripts", id="running_title"),
            DataTable(id="running_table"),
            Button("🧹 Clear Logs", id="clear_logs"),
            Log(id="log_view", auto_scroll=True),
        )
        yield Footer()

    def on_mount(self):
        """Load scheduled jobs & logs on startup."""
        self.refresh_jobs()
        self.load_logs()
        self.set_interval(1, self.update_running_scripts)  # Update running scripts every second

    def refresh_jobs(self):
        """Refresh job table in place (Clear & Add Rows)."""
        jobs = get_jobs()
        table = self.query_one("#job_table", DataTable)
        table.clear(columns=True)  # Clears old table but keeps column headers
        table.add_columns("ID", "Script", "Hour", "Min", "Sec", "Frequency", "Status")

        for _, row in jobs.iterrows():
            table.add_row(str(row["id"]), row["script_path"], str(row["hour"]), str(row["minute"]), str(row["second"]),
                          row["frequency"], "✅ Active" if row["active"] else "⏸ Paused")

    def update_running_scripts(self):
        """Update the running scripts table dynamically."""
        running_table = self.query_one("#running_table", DataTable)
        running_table.clear(columns=True)  # Clears previous data while keeping headers
        running_table.add_columns("Script", "Start Time", "Elapsed Time")

        for script, start_time in running_scripts.items():
            elapsed_time = datetime.now() - start_time
            running_table.add_row(script, start_time.strftime('%Y-%m-%d %H:%M:%S'), str(elapsed_time).split(".")[0])

    def load_logs(self):
        """Load log content dynamically."""
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = f.readlines()
            log_widget = self.query_one("#log_view", Log)
            log_widget.clear()
            log_widget.write("".join(logs))

    def on_button_pressed(self, event):
        """Handle button clicks."""
        button_id = event.button.id
        if button_id == "schedule_button":
            script = self.query_one("#script_input", Input).value
            add_job(os.path.join(SCRIPT_DIRECTORY, script), 0, 0, 0, "once")
            self.refresh_jobs()

        elif button_id == "run_button":
            script = self.query_one("#script_input", Input).value
            run_script(os.path.join(SCRIPT_DIRECTORY, script))

        elif button_id == "clear_logs":
            self.query_one("#log_view", Log).clear()  # Clears logs in UI only


if __name__ == "__main__":
    ScriptSchedulerApp().run()
