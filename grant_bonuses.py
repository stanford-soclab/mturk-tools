from mturk.mturk import MechanicalTurk
import sys
import csv

def make_bonus_api_call(mturk_obj, assign_id, worker_id, amount, message):

	request_dict = {
					"AssignmentId": assign_id,
					"WorkerId": worker_id,
					"BonusAmount.1.Amount": amount,
					"BonusAmount.1.CurrencyCode": 'USD',
					"Reason": message
					}
	response = mturk_obj.request('GrantBonus', request_dict)
	if not response.valid:
		print 'Error granting bonus'
		print response

def grant_bonuses(bonus_file, amount=1, message=""):

	mt = MechanicalTurk()
	with open(bonus_file, 'rb') as csvfile:
		csvreader = csv.reader(csvfile)
		for row in csvreader:
			assign_id = row[0]
			worker_id = row[1]
			if len(row) > 2 and row[2] != '':
				bonus_amount = float(row[2])
			else:
				bonus_amount = amount
			if len(row) > 3 and row[3] != '':
				bonus_msg = row[3]
			else:
				bonus_msg = message
			print assign_id + '\t' + worker_id + '\t' + str(bonus_amount) + '\t' + str(bonus_msg)
			make_bonus_api_call(mt, assign_id, worker_id, bonus_amount, bonus_msg)


def main():
	bonus_file = sys.argv[1]
	amount = 1
	if len(sys.argv) > 2:
		amount = float(sys.argv[2])
	bonus_message = ""
	if len(sys.argv) > 3:
		bonus_message = sys.argv[3]
	grant_bonuses(bonus_file, amount=amount, message=bonus_message)

if __name__ == "__main__":
    main()