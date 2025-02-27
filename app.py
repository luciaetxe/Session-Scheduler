from flask import Flask, request, render_template
from datetime import datetime
import json

app = Flask(__name__)

sessions = []
try:
	with open("sessions.json", "r") as file:
		sessions = json.load(file)
	print("Loaded sessions from file:", sessions)
except FileNotFoundError:
	sessions = []
	print("No file found, starting with empty sessions")

@app.route("/", methods=["GET", "POST"])
def schedule():
	error = None
	print("Request method:", request.method)
	print("Sessions at start:", sessions)
	if request.method == "POST":
		name = request.form["name"].strip()
		date = request.form["date"]
		time = request.form["time"]
		service = request.form["service"]
		print("Form data:", {"name": name, "date": date, "time": time, "service": service})
		if not name or not date or not time or not service:
			error = "Name, date, time and service are required."
			print("Error set for empty fields:", error)
		else:
			try:
				date_obj = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
				print("Parsed datetime:", date_obj)
				if date_obj < datetime.now():
					error = "Date and time cannot be in the past."
					print("Error set for past date/time:", error)
				else:
					sessions.append({"name": name, "date": date, "time": time, "service": service})
					print("After append:", sessions)
					with open("sessions.json", "w") as file:
						json.dump(sessions, file)
						print("Save to file:", sessions)
			except ValueError:
				error = "Invalid format (use YYYY-MM-DD and HH:MM)."
				print("Error set for format:", error)
	sorted_sessions = sorted(sessions, key=lambda x: (x["date"], x.get("time", "00:00")))
	print("Rendering with sorted sessions:", sorted_sessions, "Error:", error)
	return render_template("agenda.html", sessions=sorted_sessions, error=error), 200, {'Cache-Control': 'no-cache'}

if __name__ == "__main__":
	app.run(debug=True)