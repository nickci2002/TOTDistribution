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

	# Obtains json data from request
	try:
		while True:
			# Gets the month
			month, year = mydate.convert_relative_month(int_month)
			month_folder = folder.dir_month(month, year)

			# Request variables
			tl_url = nando.get_tl_url(int_month)
			tl_header = { "User-Agent": "Obtaining TOTD data from " + month_folder }
			tl_req = token.make_request(tl_url, tl_header)
			tl = tl_req.json()
			print("\tObtained track list for " + month_folder + " successfully!")
			
			# Adds file to subdirectory
			folder.dir_new(folder.TRACK_DIR, month_folder)
			with myfile.write_file(folder.tl_dir(month, year)) as tl_file:
				json.dump(tl, tl_file, indent=2)

			# Increments month counter
			int_month += 1

	except mydate.InvalidMonthError:
		print("Finished collecting data from all months")