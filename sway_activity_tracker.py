#!/usr/bin/env python3
"""
Sway Window Activity Tracker
Tracks active window titles and their durations throughout the day.
"""

import json
import subprocess
import time
import datetime
import os
import signal
import sys
from pathlib import Path


class SwayActivityTracker:
    def __init__(self, log_dir="~/.local/share/sway-tracker"):
        self.log_dir = Path(log_dir).expanduser()
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.current_window = None
        self.start_time = None
        self.activities = []

        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

    def signal_handler(self, signum, frame):
        """Handle shutdown gracefully"""
        print("\nShutting down tracker...")
        self.save_current_activity()
        self.save_daily_log()
        sys.exit(0)

    def get_active_window(self):
        """Get the currently focused window title and app name"""
        try:
            # Get the tree of windows
            result = subprocess.run(
                ["swaymsg", "-t", "get_tree"], capture_output=True, text=True
            )
            if result.returncode != 0:
                return None

            tree = json.loads(result.stdout)

            def find_focused(node):
                """Recursively find the focused window"""
                if node.get("focused", False):
                    return node
                for child in node.get("nodes", []):
                    focused = find_focused(child)
                    if focused:
                        return focused
                for child in node.get("floating_nodes", []):
                    focused = find_focused(child)
                    if focused:
                        return focused
                return None

            focused_window = find_focused(tree)
            if focused_window:
                title = focused_window.get("name", "Unknown")
                app_id = focused_window.get(
                    "app_id",
                    focused_window.get("window_properties", {}).get("class", "Unknown"),
                )
                return f"{app_id}: {title}"

        except Exception as e:
            print(f"Error getting active window: {e}")

        return None

    def save_current_activity(self):
        """Save the current activity if there is one"""
        if self.current_window and self.start_time:
            duration = time.time() - self.start_time
            if duration > 1:  # Only log activities longer than 1 second
                activity = {
                    "window": self.current_window,
                    "start_time": datetime.datetime.fromtimestamp(
                        self.start_time
                    ).isoformat(),
                    "duration": round(duration, 2),
                    "end_time": datetime.datetime.now().isoformat(),
                }
                self.activities.append(activity)

    def save_daily_log(self):
        """Save activities to daily log file"""
        if not self.activities:
            return

        today = datetime.date.today().isoformat()
        log_file = self.log_dir / f"activity-{today}.json"

        # Load existing data if file exists
        existing_data = []
        if log_file.exists():
            try:
                with open(log_file, "r") as f:
                    existing_data = json.load(f)
            except:
                pass

        # Append new activities
        existing_data.extend(self.activities)

        # Save to file
        with open(log_file, "w") as f:
            json.dump(existing_data, f, indent=2)

        print(f"Saved {len(self.activities)} activities to {log_file}")
        self.activities = []

    def generate_report(self, date=None):
        """Generate a summary report for a specific date"""
        if date is None:
            date = datetime.date.today().isoformat()

        log_file = self.log_dir / f"activity-{date}.json"
        if not log_file.exists():
            print(f"No activity log found for {date}")
            return

        with open(log_file, "r") as f:
            activities = json.load(f)

        # Group activities by window/app
        window_stats = {}
        total_time = 0

        for activity in activities:
            window = activity["window"]
            duration = activity["duration"]

            if window not in window_stats:
                window_stats[window] = {"total_time": 0, "count": 0, "sessions": []}

            window_stats[window]["total_time"] += duration
            window_stats[window]["count"] += 1
            window_stats[window]["sessions"].append(
                {"start": activity["start_time"], "duration": duration}
            )
            total_time += duration

        # Sort by total time spent
        sorted_windows = sorted(
            window_stats.items(), key=lambda x: x[1]["total_time"], reverse=True
        )

        print(f"\n=== Activity Report for {date} ===")
        print(f"Total tracked time: {self.format_duration(total_time)}\n")

        for window, stats in sorted_windows:
            percentage = (
                (stats["total_time"] / total_time * 100) if total_time > 0 else 0
            )
            avg_session = stats["total_time"] / stats["count"]

            print(f"{window}")
            print(
                f"  Total time: {self.format_duration(stats['total_time'])} ({percentage:.1f}%)"
            )
            print(f"  Sessions: {stats['count']}")
            print(f"  Average session: {self.format_duration(avg_session)}")
            print()

    def format_duration(self, seconds):
        """Format duration in human readable format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)

        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def run(self, check_interval=2):
        """Main tracking loop"""
        print("Starting Sway activity tracker...")
        print("Press Ctrl+C to stop and save data")

        try:
            while True:
                current_window = self.get_active_window()
                current_time = time.time()

                if current_window != self.current_window:
                    # Save previous activity
                    self.save_current_activity()

                    # Start tracking new window
                    self.current_window = current_window
                    self.start_time = current_time

                    if current_window:
                        print(f"Switched to: {current_window}")

                # Save data every 5 minutes
                if len(self.activities) > 0 and len(self.activities) % 150 == 0:
                    self.save_daily_log()

                time.sleep(check_interval)

        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Track Sway window activity")
    parser.add_argument(
        "--report",
        "-r",
        metavar="DATE",
        help='Generate report for date (YYYY-MM-DD). Use "today" for today.',
    )
    parser.add_argument(
        "--log-dir",
        default="~/.local/share/sway-tracker",
        help="Directory to store activity logs",
    )
    parser.add_argument(
        "--interval",
        "-i",
        type=int,
        default=2,
        help="Check interval in seconds (default: 2)",
    )

    args = parser.parse_args()

    tracker = SwayActivityTracker(args.log_dir)

    if args.report:
        date = args.report
        if date.lower() == "today":
            date = datetime.date.today().isoformat()
        tracker.generate_report(date)
    else:
        tracker.run(args.interval)


if __name__ == "__main__":
    main()
