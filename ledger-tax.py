# coding=utf-8

#
# A little programm, which gets all business expenses and calculates
# according to german law, what can be sed to reduce the tax.
#

import sys, datetime, os, imp, re, ledger



### ### ###
### ### ### load configurarion file for variables
### ### ###

# !!!!! SET YOUR INDIVIDUAL SETTINGS FILE HERE
# !!!!! IT MUST BE SET UP LIKE THE 'ledger-tax-settings-default.py' FILE
####
###
#

SETTINGS_FILE = 'ledger-tax-settings.py'

#
###
####
# !!!!!
# !!!!!

# get the actual path to the python script
path_to_project = os.path.dirname(os.path.realpath(__file__))


# check if user set an individual settings file, or load default otherwise

if os.path.isfile(path_to_project + '/' + SETTINGS_FILE):
	print 'Loading configuration PERSONAL'
	configuration = imp.load_source('ledger-tax-settings', path_to_project + '/' + SETTINGS_FILE)
	configuration_def = imp.load_source('ledger-tax-settings-default', path_to_project + '/ledger-tax-settings-default.py')
else:
	if os.path.isfile(path_to_project + '/ledger-tax-settings-default.py'):
		configuration = imp.load_source('ledger-tax-settings-default', path_to_project + '/ledger-tax-settings-default.py')
	else:
		print 'No settings file found.'
		exit()



# configuartion function

def config(att):
	if hasattr(configuration, att):
		return getattr(configuration, att)
	else:
		print 'Please update your personal settings file.'
		return getattr(configuration_def, att)



# getting the variables from the settings file - don't change the values here!

expenses_account = config('expenses_account')
income_account = config('income_account')
threshold_amount = config('threshold_amount')

colorize = config('colorize')

CL_TXT = config('CL_TXT')
CL_INF = config('CL_INF')
CL_ACC = config('CL_ACC')
CL_DIM = config('CL_DIM')
CL_VAL = config('CL_VAL')
CL_INV = config('CL_INV')
CL_E = config('CL_E')

### ### ###
### ### ### load configurarion file for variables - END
### ### ###



# get year from 1st parameter or set last year as default
try:
	year = int(sys.argv[1])
except Exception, e:
	year = int(datetime.date.today().year-1)

# get my ledger file, stored in the ENVIRONMENT_VARIABLE "LEDGER_FILE"
ledger_file = os.environ.get('LEDGER_FILE')
if not ledger_file:
	print 'LEDGER_FILE not set.'
	exit()

# make python ledger object from file
LED = ledger.read_journal(ledger_file)

# get the (german) afa table
if os.path.isfile(path_to_project + '/afa.txt'):

	# load the afa.txt file
	f = open(path_to_project + '/afa.txt')
	afa_file = f.read().splitlines()
	f.close()

	# get the variables from the file
	afa_table = {}
	for line in afa_file:
		if not '#' in line and line != '':
			try:
				tmp_key = line.split('=')[0].strip()
				tmp_val = line.split('=')[1].strip()
				afa_table[tmp_key] = int(tmp_val)
			except Exception:
				pass
else:
	print 'No afa.txt file found.'
	exit()

# get max value (years) from afa_table
max_year_into_past = year - max(afa_table.values())



# Classes and Functions

def get_last_tag_of_posting(posting):
	out = ''
	for x in afa_table.keys():
		if posting.has_tag(x):
			out = x
	return out



class All_Expenses_Class(object):
	def __init__(self, actual_year):
		self.Actual_Year = actual_year
		self.Expenses = []
		self.Accounts_With_Total = {} # var[account] = 0.0
		self.Total_Amount = 0.0

	def add(self, date, payee, account, amount, invoice, tag, note):
		# add an expense
		self.Expenses.append( Expense(date, payee, account, amount, invoice, tag, note) )

		# recalculate Accounts_With_Total
		if not account in self.Accounts_With_Total.keys():
			self.Accounts_With_Total[account] = self.Expenses[ len(self.Expenses)-1 ].get_actual_year_amount(self.Actual_Year)
		else:
			self.Accounts_With_Total[account] += self.Expenses[ len(self.Expenses)-1 ].get_actual_year_amount(self.Actual_Year)

		# recalculate overall Total_Amount
		self.Total_Amount += self.Expenses[ len(self.Expenses)-1 ].get_actual_year_amount(self.Actual_Year)


	def show_tax_reduction(self):
		# print acounts with its totals
		for acc in sorted(self.Accounts_With_Total.iteritems()):
			if acc[1] > 0.0:
				print
				print CL_ACC + acc[0] + ' -> ' + CL_VAL + str(acc[1]) + CL_E

			# list its expenses
			for ex in self.Expenses:
				if ex.Account == acc[0] and ex.get_actual_year_amount(self.Actual_Year) > 0.0:
					# get note
					tmp_note = ' (' + ex.Note + ') ' if ex.Note != 'None' else ' '
					# get invoice code
					tmp_code = '(' + ex.Invoice + ') ' if ex.Invoice != 'None' else ''
					# get this year and lasting years for tax reduction
					tmp_years = ' (' + str(ex.get_this_year_and_all_years(self.Actual_Year)[0]) + '/' + str(ex.get_this_year_and_all_years(self.Actual_Year)[1]) + ')' if ex.get_this_year_and_all_years(self.Actual_Year)[1] > 0 else ''
					# print expense
					print '     ' + CL_TXT + ex.Payee + CL_DIM + tmp_note + CL_INV + tmp_code + CL_TXT + '-> ' + CL_VAL + str(ex.get_actual_year_amount(self.Actual_Year)) + CL_DIM + tmp_years + CL_E

		# list past years expenses, which are reducing this years tax as well - summerized
		past_years_expenses = {}
		for ex in self.Expenses:
			if ex.Date.year != self.Actual_Year and ex.get_actual_year_amount(self.Actual_Year) != 0.0:
				# get note
				tmp_note = ' (' + ex.Note + ') ' if ex.Note != 'None' else ' '
				# get invoice code
				tmp_code = '(' + ex.Invoice + ') ' if ex.Invoice != 'None' else ''
				# get this year and lasting years for tax reduction
				tmp_years = ' (' + str(ex.get_this_year_and_all_years(self.Actual_Year)[0]) + '/' + str(ex.get_this_year_and_all_years(self.Actual_Year)[1]) + ')' if ex.get_this_year_and_all_years(self.Actual_Year)[1] > 0 else ''
				# append to past_years_expenses
				if not ex.Date.year in past_years_expenses.keys():
					past_years_expenses[ ex.Date.year ] = []
					past_years_expenses[ ex.Date.year ].append( CL_TXT + ex.Payee + CL_DIM + tmp_note + CL_INV + tmp_code + CL_TXT + '-> ' + CL_VAL + str(ex.get_actual_year_amount(self.Actual_Year)) + CL_DIM + tmp_years + CL_E )
				else:
					past_years_expenses[ ex.Date.year ].append( CL_TXT + ex.Payee + CL_DIM + tmp_note + CL_INV + tmp_code + CL_TXT + '-> ' + CL_VAL + str(ex.get_actual_year_amount(self.Actual_Year)) + CL_DIM + tmp_years + CL_E )
		# print out, if there are any past years expenses
		if len(past_years_expenses) != 0:
			print
			print CL_ACC + 'Past year expenses:' + CL_E
			for past_years in past_years_expenses.iteritems():
				print CL_ACC + '     ' + str(past_years[0])
				for past_expenses in past_years[1]:
					print CL_TXT + '       ' + past_expenses

		# show me the total
		print
		print CL_DIM + '--- --- --- --- --- --- --- --- ---' + CL_E
		print
		print CL_ACC + 'Total tax reduction amount: ' + CL_VAL + str(self.Total_Amount) + CL_E



class Expense(object):
	def __init__(self, date, payee, account, amount, invoice, tag, note):
		self.Date = date
		self.Payee = payee
		self.Account = account
		self.Amount = amount
		self.Invoice = invoice
		self.Tag = tag
		self.Note = note
		self.Afa = afa_table

	def get_this_year_and_all_years(self, actual_year):
		tmp_this_year = 0
		tmp_all_years = 0

		# get this year
		tmp_this_year = actual_year - self.Date.year + 1

		# get all years
		if self.Tag in self.Afa.keys() and self.Amount > threshold_amount:
			# it has a tag and the amount is above the threshold_amount
			if self.Afa[self.Tag] == 0:
				# it is a ZERO afa-value ... so the amount has to be zero
				tmp_all_years = 0
			else:
				# it is a afa-value above ZERO
				tmp_all_years = self.Afa[self.Tag]
		elif not self.Tag in self.Afa.keys() and self.Amount > threshold_amount:
			# it has NO tag, but the amount is above the threshold_amount
			# so use the default value instead
			tmp_all_years = self.Afa['default']
		else:
			# the amount is below the threshold_amount
			tmp_all_years = 0

		return (tmp_this_year, tmp_all_years)

	def get_yearly_amount(self):
		# get the general yearly amount for this expense

		if self.Tag in self.Afa.keys() and self.Amount > threshold_amount:
			# it has a tag and the amount is above the threshold_amount
			if self.Afa[self.Tag] == 0:
				# it is a ZERO afa-value ... so the amount has to be zero
				# otherwise it would be difiding by ZERO... uh oh!
				return 0.0
			else:
				# it is a afa-value above ZERO
				return self.Amount / self.Afa[self.Tag]
		elif not self.Tag in self.Afa.keys() and self.Amount > threshold_amount:
			# it has NO tag, but the amount is above the threshold_amount
			# so use the default value instead
			return self.Amount / self.Afa['default']
		elif self.Tag in self.Afa.keys() and self.Amount < threshold_amount:
			# tag is in afa, but threshold is below
			if self.Afa[self.Tag] == 0:
				# it is a ZERO afa-value ... so the amount has to be zero
				return 0.0
			else:
				# it is a afa-value above ZERO
				# but this amount is below threshold, so just use the normal amount
				return self.Amount
		else:
			# the amount is below the threshold_amount and has no tag in afa
			return self.Amount

	def get_actual_year_amount(self, actual_year):
		# gets the amount for this actual year.
		# if it's after the years, in which the expense could reduce the tax, then
		# there won't be an amount, since it already reduced the tax throughout the years

		# cycle through the years till actual_year
		tmp_start_amount = self.Amount
		for x in xrange(self.Date.year,actual_year):
			tmp_start_amount -= self.get_yearly_amount()

		# return the value, but make it ZERO, if it's under ZERO
		if tmp_start_amount <= 0:
			return 0.0
		else:
			return self.get_yearly_amount()






# DO THE MAGIC WORK

# generate All_Expenses variable
All_Expenses = All_Expenses_Class(year)

# cycle through the years - from max_years_into_past to year+1
for actual_year in xrange(max_year_into_past,year+1):
	for post in LED.query('-p ' + str(actual_year) + ' ' + expenses_account):
		# only consider expense as expense, when amount is > 0
		if post.amount > 0:
			amt = re.findall(r'\d*\.\d+|\d+', str(post.amount).replace(',', '.'))
			All_Expenses.add( post.date, str(post.xact.payee), str(post.account), float(amt[0]) if amt else 0.0, str(post.xact.code), get_last_tag_of_posting(post), str(post.note).split(':')[0].strip() )

# output the magic expenses caluclation
All_Expenses.show_tax_reduction()


# generate income, taxes, pre-tax income and after-tax income

# income
Total_Income = 0.0
for post in LED.query('-p ' + str(actual_year) + ' ' + income_account):
	Total_Income += float(post.amount)
if Total_Income < 0.0:
	Total_Income = Total_Income * -1

# pre-tax income
Pre_Tax_Income = Total_Income - All_Expenses.Total_Amount

# taxes and after-tax income
Taxes = configuration.calculate_taxes( Pre_Tax_Income )[0]
After_Tax_Income = configuration.calculate_taxes( Pre_Tax_Income )[1]

# output the income stuff
print CL_ACC + 'Total income: ' + CL_VAL + str(Total_Income)
print CL_ACC + 'Pre-tax income: ' + CL_VAL + str(Pre_Tax_Income)
print CL_ACC + 'Taxes: ' + CL_VAL + str(Taxes)
print CL_DIM + '--- --- --- --- --- ---'
print CL_ACC + 'After-tax income: ' + CL_VAL + str(After_Tax_Income) + CL_E
print