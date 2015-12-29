#!/usr/bin/python

import argparse, json, sys, traceback, re, os

path = os.path.dirname(__file__)

class Case:
	def __init__(self, f, i, o):
		self.f = f
		self.i = i
		self.o = o

	def sol(self, s, e = None):
		self.s = s
		self.e = e
		self.failed = self.o != self.s
		self.error = self.e != None
		if self.error:
			self.case = 0
		elif self.failed:
			self.case = 1
		else:
			self.case = 2

	def __str__(self):
		return "(function: %s, input: %s, output: %s, expected_output: %s, error: %s)" % (self.f, self.i, self.s, self.o, self.e)

	def __repr__(self):
		return self.__str__()

def test_io(module, cases):
	for case in cases:
		yield check_io(module, *case)

def check_io(module, i, o, fn='main'):
	e = None
	sol = None
	try:
		sol = getattr(module,fn)(i)
	except Exception as ex:
		e = sys.exc_info()
	case = Case(fn, i, o)
	case.sol(sol, e)
	return case

def main():
	parser = argparse.ArgumentParser(description="Test your solution of a projecteuler's problem.")
	parser.add_argument('-n','--number', metavar='problem_number', type=int,help='the number of the problem')
	parser.add_argument('file', metavar='file', type=str,help='the solution')

	args = parser.parse_args()

	basename = os.path.basename(args.file)
	dirname = os.path.dirname(args.file)
	filename, file_extension = os.path.splitext(basename)

	if not args.number:
		m = re.search('\d+',filename)
		if not m:
			raise Exception("I cannot guess the problem number please specify it with -n.")
		args.number = m.group(0)


	sys.path.append(dirname)
	module = __import__(filename)

	with open(os.path.join(path, 'tests.json')) as f:
		tests = json.load(f)
	try:
		cases = tests[str(args.number)]
	except KeyError:
		raise Exception("There is no cases for this problem.")

	cs = test_io(module, cases)
	repr_cases(list(cs))

class TCs:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def repr_cases(cases):
	HR = '-'*80
	COLORS = {2:TCs.OKGREEN, 1:TCs.WARNING, 0:TCs.FAIL}
	REPR_CHAR = {2:'.', 1:'F', 0:'E'}
	count = [0]*3
	chars = ""
	for i in cases:
		count[i.case]+=1
		chars += "%s%s%s"%(COLORS[i.case],REPR_CHAR[i.case],TCs.ENDC)
	print chars
	for i in cases:
		if i.error:
			print HR
			print "input %s for the function %s"%(i.i, i.f)
			traceback.print_exception(*i.e)
		elif i.failed:
			print HR
			print "input %s for the function %s\n%s exepected but got %s" %(i.i, i.f, i.o, i.s)
	print HR
	print "%i/%i passed"%(count[2],sum(count))



if __name__ == "__main__":
	main()