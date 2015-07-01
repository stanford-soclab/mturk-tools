import mturk
import sys
import re
#TODOs:
#1. see if this still works in windows (and probably get xmltodict on lab's windows machines)
#2. set the secret key as an environment variable (rather than as something in a text file that gets passed around everywhere)
def load_email(message_file):
	with open(message_file) as f:
		lines = f.readlines()
		subj = lines[0].strip()
		body = "".join(lines[1:])
	return subj, body

def contact_worker(worker_id, message, m):
	print "Contacting worker "+worker_id
	subj, body = load_email(message)

	email_result = m.request("NotifyWorkers",
				{"Subject":subj,
				 "MessageText":body,
				 "WorkerId":worker_id})
	if not email_result.get_response_element("IsValid"):
		print "Error Occured contacting worker "+worker_id


def meets_qualification(qual, qualified_vals, curr_worker):
	this_qualval = qual.get_response_element("IntegerValue")

	if (qualified_vals == -1):
		if (this_qualval != None):
			return True
		else:
			return False
	if (this_qualval != None):
		this_qualval = int(this_qualval)
		for qualval in qualified_vals:
			if this_qualval == qualval:
				return True	
	return False

def recontact_workers(worker_list, qualification_id, qualified_vals, message):
	m = mturk.MechanicalTurk()
	with open(worker_list,'rb') as f:
		for line in f:
			curr_worker = re.sub(r'(\r\n|\r|\n)', '\n', line).strip()
			if qualification_id is None:
				contact_worker(curr_worker, message, m)
			else:
				qual = m.request("GetQualificationScore",
									{"QualificationTypeId":qualification_id,
									 "SubjectId":curr_worker})
				if (meets_qualification(qual, qualified_vals, curr_worker)):
					contact_worker(curr_worker, message, m)

def main():
	worker_list = sys.argv[1]
	message = sys.argv[2]
	if len(sys.argv) == 3:
		recontact_workers(worker_list, qualification_id=None, qualified_vals=-1, message=message)
	else:
		qualification_id = sys.argv[3]
		if (len(sys.argv) > 4):
			qualified_vals = [int(x) for x in sys.argv[4].split("-")]
		else:
			qualified_vals = -1
		recontact_workers(worker_list, qualification_id, qualified_vals, message)	


if __name__ == "__main__":
    main()