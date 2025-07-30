import re
from dateutil import parser
from datetime import datetime, date

class DateUtils:
	def is_date(self, string):
		try:
			parser.parse(string)
			return True
		except ValueError:
			return False

	def calculate_age(self, born):
		today = date.today()
		return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
	
	def validate_date_format(date_string):
		return re.match(r'^\d{4}-\d{2}-\d{2}$', date_string) is not None
	
	def calculate_hour_difference_from_iso_dates(self, start_date_iso, end_date_iso):
		if start_date_iso is None or end_date_iso is None:
				return 0
		
		time_difference = abs(end_date_iso - start_date_iso)
		duration_in_seconds = time_difference.total_seconds()
		duration_in_minutes = duration_in_seconds / 60
		
		return duration_in_minutes
	
	def convert_minute_in_hours(self, minutes):
		hours = minutes // 60
		minutes_remaining = minutes % 60
		
		return f"{int(hours):02d}:{int(minutes_remaining):02d}"
		
		
	def calculate_hour_difference(self, hour_start_str, hour_end_str):
		if hour_start_str is None or hour_end_str is None:
			return 0
		
		hour_start = datetime.strptime(hour_start_str, "%H:%M")
		hour_end = datetime.strptime(hour_end_str, "%H:%M")
		hour_diff = hour_end - hour_start
		hours_in_minutes = (hour_diff.seconds // 60) % 60

		return hours_in_minutes