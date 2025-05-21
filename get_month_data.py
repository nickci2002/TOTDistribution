import date_conversion as mydate
import file_abbr as myfile
import format_folders as folder
import format_reqs as nando
import obtain_token as token
import json
import sys

# Beginning of the script
if __name__ == "__main__":
	try:
		mydate.set_current_month()
		int_month = int(input("Which month (0 is current, 1 is last month, etc.)"))
	except mydate.InvalidMonthError:
		print("The following month does not have any TOTDs. Closing program.")
		sys.exit()

	print("Obtaining monthly TOTD tracklists...")
	
	# Gets the month
	month, year = mydate.convert_relative_month(int_month)
	month_folder = folder.dir_month(month, year)
	# Request variables
	tl_req_url = nando.get_tl_url(int_month)
	req_header = { 
		"User-Agent": "Obtaining TOTD data from " + month_folder
	}
	tl_req = token.make_request(tl_req_url, req_header)
	tl = tl_req.json()
	print("\tObtained track list for " + month_folder + " successfully!")
	
	# Adds file to subdirectory
	folder.mkdir_month(month_folder)
	with myfile.write_file(folder.tl_dir(month, year)) as tl_file:
		json.dump(tl, tl_file, indent=2)

	print("Finish collecting data monthly tracks!")
	#print(tl)

	tl = tl['monthList'][0]
	# Get individual track data
	days_in_month = tl['lastDay']
	for d in range(days_in_month):
		# The actual numerical date
		day = d + 1
		
		# Gets initial data for the current track
		curr_track = tl['days'][d]
		
		day_folder = folder.dir_day(day, month, year)
		print("Accessing track data for [" + day_folder + "]...")

		# Check if the track exists
		if curr_track['mapUid'] == "" and curr_track['seasonUid'] == "":
			print("\tThis track does not exist.")
			print("\tTry again tomorrow after 7PM CEST.")
			break

		# Dictionary we are storing the leaderboard data to
		lb_json = {
			"name": "",  # name of the track
			"medals": [    # medal times for each track
				0,	# author time
				0,	# gold time
				0,	# silver time	
				0	# bronze time
			],
			"count": 0,    # number of leaderboard entries
			"tops": []     # data of leaderboard entries
		}

		# Gets medal data
		print("Obtaining track data...")
		map_req_url = nando.get_map_url(curr_track['mapUid'])
		map_req_response = token.make_request(map_req_url, req_header)

		if map_req_response.status_code == 200:
			folder.mkdir_day(month_folder, day_folder)
			
			map_data = map_req_response.json()
			lb_json['name'] = map_data['name']
			lb_json['medals'] = [
				map_data['authorTime'],
				map_data['goldTime'],
				map_data['silverTime'],
				map_data['bronzeTime']
			]
			
			print("Finished obtaining track data!")

		else:
			print("Error getting permissions for " + day_folder + "!")
			continue

		# Gets rankings
		offset = 0
		print("Obtaining leaderboard...")
		while True:
			lb_req_url = nando.get_lb_url(curr_track['seasonUid'], \
									   curr_track['mapUid'],    \
									   offset)
			lb_req_response = token.make_request(lb_req_url, req_header)

			if lb_req_response.status_code == 200:
				records = lb_req_response.json()["tops"][0]["top"]
				if len(records) == 0 or offset >= 10000:
					break
				else:
					lb_json["tops"].extend(records)
					records.clear()
					offset += 100
					print("\tObtained " + str(offset) + " records!")

		# Creates a folder/file for the leaderboard data
		lb_json['count'] = lb_json['tops'][-1]['position']
		with myfile.write_file(folder.lb_dir(day, month, year)) as lb_file:
			json.dump(lb_json, lb_file, indent=2)

		# Console output upon completion
		print("Done searching!")
		print(f"Found a total of {lb_json['count']} items for the current map!")
		print()
		
	print("Finished obtaining leaderboard data for the current month!")