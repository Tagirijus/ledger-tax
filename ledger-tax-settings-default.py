# coding=utf-8

# configurarion


# some default values

expenses_account		= 'Expenses'
income_account			= 'Income'
threshold_amount		= 487.9 # german threshold. above this the expense can only reduce tax for X years (according to the afa table). the value is meant to be 410 taxfree and 487,9 with 19% taxes

# color variables - and boolean for switching between color modes

colorize = True

WHITE = '\033[97m'
PURPLE = '\033[95m'
BLUE = '\033[94m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
BOLD = '\033[1m'
DIM = '\033[2m'
GREY = '\033[90m'
UNDERLINE = '\033[4m'

# customize the colors here !!!

# normal text
CL_TXT = PURPLE if colorize else ''
# info, error and warning text
CL_INF = BOLD + RED if colorize else ''
# account
CL_ACC = BLUE if colorize else ''
# dimmed output
CL_DIM = GREY if colorize else ''
# value
CL_VAL = GREEN if colorize else ''
# invoice code
CL_INV = YELLOW if colorize else ''

# don't change this- it's the ending string for the coloring strings
CL_E = '\033[0m' if colorize else ''