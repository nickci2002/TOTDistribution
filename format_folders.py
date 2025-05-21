import os

# Constants for various directories/files
TRACK_DIR = "Tracks"
LB_DIR = "leaderboard.json" #json file
MD_DIR = "medal_data.txt"   #text document
TL_DIR = "track_list.json"  #json file


# Formats the month and year as a string ["Month_YYYY"]
#   month --> The month (string)
#   year ---> The year  (integer)
def dir_month(month, year):
	return "{}_{:04d}".format(month, year)


# Creates necessary month directories/subdirectories
#   month --> The month (string)
#   year ---> The year  (integer)
def mkdir_month(month, year):
	dir_new(TRACK_DIR, dir_month(month, year))
#	f_month --> Formatted month folder
def mkdir_month(f_month):
	dir_new(TRACK_DIR, f_month)


# Formats the date as a string [DD_MM_YYYY]
#   day ----> The day   (integer)
#   month --> The month (string)
#   year ---> The year  (integer)
def dir_day(day, month, year):
	return "{:02d}_{}_{:04d}".format(day, month, year)


# Creates necessary day directories/subdirectories
#   day ----> The day   (integer)
#   month --> The month (string)
#   year ---> The year  (integer)
def mkdir_day(day, month, year):
	dir_new(mk_dir_month(month, year) + dir_day(day, month, year))
#	f_month --> Formatted month folder
#	f_day ----> Formatted day folder
def mkdir_day(f_month, f_day):
	dir_new(TRACK_DIR, f_month, f_day)

								
# Subdirectory containing all LEADERBOARD entries
#   day ------> The day   (integer)
#   month ----> The month (string)
#   year -----> The year  (integer)
#	is_file --> Is it the file or the folder?
def lb_dir(day, month, year):
	m_folder = dir_month(month, year)
	d_folder = dir_day(day, month, year)
	return append(TRACK_DIR, m_folder, d_folder, LB_DIR)


# Subdirectory containing MEDAL DISTRIBUTION among leaderboard entries
#   day ----> The day
#   month --> The month
#   year ---> The year
def md_dir(day, month, year):
	m_folder = dir_month(month, year)
	d_folder = dir_day(day, month, year)
	return append(TRACK_DIR, m_folder, d_folder, MD_DIR)


# Subdirectory containing the TOTD list for the month
#   month --> The month
#   year ---> The year
def tl_dir(month, year):
	m_folder = dir_month(month, year)
	return append(TRACK_DIR, m_folder, TL_DIR)


# Custom function used to create directories easily
#   args --> The directories we wish to add
def dir_new(*args):
	dir_temp = ""
	for arg in args:
		dir_temp = append(dir_temp, arg)
		if not os.path.isdir(append(os.getcwd(), dir_temp)):
			os.mkdir(dir_temp)


# Chains directores using the folder 'Tracks'
#   args --> The directories we wish to add together
def append(*args):
	return os.path.join(*args)


# Counts number of folders in the current folder
#	f_name --> The name of the folder we're checking
def get_track_dir_count(f_name: str):
	f_path = append(TRACK_DIR, f_name)
	return len(next(os.walk(f_path))[1])