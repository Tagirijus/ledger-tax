# coding=utf-8

# tax equation, found on:
# https://www.bmf-steuerrechner.de
# (visited on 19. August 2016)
def calculate_taxes(income):
	# outputs tupple like this: (taxes to pay, real income)
	tax_A = 8652.0
	tax_B = 13669.0
	tax_C = 53665.0
	tax_D = 254446.0
	if income <= tax_A:
		TAXES = 0.0
	elif income > tax_A and income <= tax_B:
		TAXES = (993.62 * (income - tax_A) / 10000.0 + 1400.0) * (income - tax_A) / 10000.0
	elif income > tax_B and income <= tax_C:
		TAXES = (225.4 * (income - tax_B) / 10000.0 + 2397.0) * (income - tax_B) / 10000.0 + 952.48
	elif income > tax_C and income <= tax_D:
		TAXES = 0.42 * income - 8394.14
	elif income > tax_D:
		TAXES = 0.45 * income - 16027.52

	# output the tuple
	return (round(TAXES, 2), round(income - TAXES, 2))



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