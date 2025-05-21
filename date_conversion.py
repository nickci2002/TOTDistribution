import datetime

# Constants of the first month of TOTDs
FIRST_MONTH = 7
FIRST_YEAR = 2020
# Global variables for the current month/year
curr_month = 0
curr_year = 0


# InvalidMonthError - A custom exception class, used when any month is
#					  invalid.
class InvalidMonthError(Exception):
	"Raised if the current integer is not a valid month."
	pass


# Converts integer into corresponding month
#   month --> An integer representation of the current month
#   THROWS InvalidMonthError: The month is not a number 1-12
def convert_month(month: int):
	if month == 1:
		return "January"
	elif month == 2:
		return "February"
	elif month == 3:
		return "March"
	elif month == 4:
		return "April"
	elif month == 5:
		return "May"
	elif month == 6:
		return "June"
	elif month == 7:
		return "July"
	elif month == 8:
		return "August"
	elif month == 9:
		return "September"
	elif month == 10:
		return "October"
	elif month == 11:
		return "November"
	elif month == 12:
		return "December"
	else:
		raise InvalidMonthError("Month out of range (1-12)")


# Calculates the current month and pastes their values to curr_month
#   and curr_year
def set_current_month():
	global curr_month, curr_year
	curr_date = datetime.datetime.now()
	curr_month = curr_date.month
	curr_year = curr_date.year


# Obtains an earlier month, relative to the current month (Ex: (5,2022))
#   relative --> The number of months prior to 'curr_int'
#   THROWS InvalidMonthError if the desired month doesn't have TOTDs
def convert_relative_month(relative: int):
	if relative < 0:
		raise InvalidMonthError("Please enter a positive integer")
	
	relative -= curr_month
	if relative < 0: 
		return convert_month(-relative), curr_year

	#logic to get desired month and year
	year = curr_year - (relative//12) - 1
	month = 12 - (relative%12)

	if (year < FIRST_YEAR) or ((year == FIRST_YEAR) and (month < FIRST_MONTH)):
		raise InvalidMonthError("The month is too high")
	else:
		return convert_month(month), year