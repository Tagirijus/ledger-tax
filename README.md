# Ledger command line accounting - tax calculator in python

## Descrption

This program uses your ledger journal to calculate the tax you have to pay for a specific year and shows your real income (according to the german tax law). Use with care, since results may not be the real results the law office would calculate. Moreover some equations are not that correct maybe.


## Configuration

The program can only start, if the environment variable `LEDGER_FILE` is set.


## Usage

You can have one *parameter* which is the year. Without this *parameter* the last year is used. The idea is: you have to make the tax return for the last year.

In the ledger journal a transaction posting needs a tag, which will be the category for this specific expense. In the afa.txt table this category is used.

Example: you have bought a new computer. In germany you have to distribute this expense over three years. Say this computer expense was 900.00 € and you have bought it in the year 2014. In this case you could reduce 300.00 € for three years (2014-2016) from your income to lower your taxes. A ledger journal entry could look like this:

	2014/04/01 * (a55) A new workstation for the work
	 ; :computer:
	 Expenses  € 900.00
	 Assets

This way the ledger-tax program would look at the tag `computer`, then look into the `afa.txt` table, see that computer is something you can distribute for `3` years and calculates the real income, taxes, etc. considering the expenses.


## Feedback, Questions, etc.

E-Mail me, if something is unclear. More features may follow (especially for the german *turnover tax* / *sales tax*.)