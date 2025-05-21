import date_conversion as mydate
import file_abbr as myfile
import format_folders as folder
import json
import sys


if __name__ == '__main__':
	# Outputs number of people who got a certain medal and the percentage of all players
	def output_medal_data(medal: int):
		global medal_count, player_dist
		return str(medal_count[medal]) + " ({:.0%})".format(player_dist[medal])

	# Get months to convert
	try:
		mydate.set_current_month()
		int_month = int(input("Which month (0 is current, 1 is last month, etc.)"))
		month, year = mydate.convert_relative_month(int_month)
	except mydate.InvalidMonthError:
		print("The following month does not have any TOTDs. Closing program.")
		sys.exit()

	# Get number of folders in the current month directory
	print("Counting tracks in the folder")
	month_folder = folder.dir_month(month, year)

	print(month_folder)
	dir_count = folder.get_track_dir_count(month_folder)

	print(dir_count)

	if dir_count == 0:
		print("There is no individual track data for " + month_folder + "!")
		print("Try running 'get_track_leaderboards.py'")
		sys.exit()

	# Doesn't get data for current day 
	for d in range(dir_count-1):
		# The actual numerical date
		day = d + 1
		
		day_folder = folder.dir_day(day, month, year)
		print("Calculating medal distribution for [" + day_folder + "]...")

		# Reads JSON file of tracks into the program
		try:
			lb_file = myfile.read_file(folder.lb_dir(day, month, year))
			print(lb_file)
			lb_data = json.load(lb_file)
		except OSError:
			print("File does not exist! Closing program!")
			sys.exit()

		# Loop through all players and determine the count for each medal
		author_time, gold_time, silver_time, bronze_time = lb_data['medals']
		medal_count =  [0, 0, 0, 0, 0]  # [A, G, S, B, No medal]
		player_dist = [0, 0, 0, 0, 0]  # [A, G, S, B, No medal]
		player_count = lb_data['count']
		leaderboard = lb_data['tops']

		for i in range(player_count):
			curr_player_time = leaderboard[i]['score']
			if curr_player_time <= author_time:
				medal_count[0] += 1
			elif curr_player_time <= gold_time:
				medal_count[1] += 1
			elif curr_player_time <= silver_time:
				medal_count[2] += 1
			elif curr_player_time <= bronze_time:
				medal_count[3] += 1
			else: # NO MEDAL
				medal_count[4] += 1

		# Calculate percentage
		for i in range(len(player_dist)):
			player_dist[i] = float(medal_count[i]/player_count)
		
		print("\tDone calculating medal distribution!")

		# Output to file
		md_data = "Medal Distribution for " + lb_data['name'] + "\n" + \
				  "\tNumber of Author Medals: " + output_medal_data(0) + "\n" + \
				  "\tNumber of Gold Medals: " + output_medal_data(1) + "\n" + \
				  "\tNumber of Silver Medals: " + output_medal_data(2) + "\n" + \
				  "\tNumber of Bronze Medals: " + output_medal_data(3) + "\n" + \
				  "\tPeople with No Medal: " + output_medal_data(4)

		md_file = myfile.write_file(folder.md_dir(day, month, year))
		md_file.write(md_data)
		md_file.close()