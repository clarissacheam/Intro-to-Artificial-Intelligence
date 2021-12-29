import unittest
import student_code as sc
import expand
import sys, signal

time_map1 = {
	'Campus':{ 'Campus':None, 'Whole_Food':1, 'Beach':1, 'Cinema':None, 'Lighthouse':1, 'Ryan_Field':None, 'YWCA':None },
	'Whole_Food':{ 'Campus':1, 'Whole_Food':None, 'Beach':1, 'Cinema':1, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':None },
	'Beach':{ 'Campus':1, 'Whole_Food':1, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':None },
	'Cinema':{ 'Campus':None, 'Whole_Food':1, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':1 },
	'Lighthouse':{ 'Campus':1, 'Whole_Food':None, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':1, 'YWCA':None },
	'Ryan_Field':{ 'Campus':None, 'Whole_Food':None, 'Beach':None, 'Cinema':None, 'Lighthouse':1, 'Ryan_Field':None, 'YWCA':1 },
	'YWCA':{ 'Campus':None, 'Whole_Food':None, 'Beach':None, 'Cinema':1, 'Lighthouse':None, 'Ryan_Field':1, 'YWCA':None }
}

dis_map2 = {
	'Campus':{ 'Campus':0, 'Whole_Food':3, 'Beach':5, 'Cinema':5, 'Lighthouse':1, 'Ryan_Field':2, 'YWCA':12 },
	'Whole_Food':{ 'Campus':3, 'Whole_Food':0, 'Beach':3, 'Cinema':3, 'Lighthouse':4, 'Ryan_Field':5, 'YWCA':8 },
	'Beach':{ 'Campus':5, 'Whole_Food':3, 'Beach':0, 'Cinema':8, 'Lighthouse':5, 'Ryan_Field':7, 'YWCA':12 },
	'Cinema':{ 'Campus':5, 'Whole_Food':3, 'Beach':8, 'Cinema':0, 'Lighthouse':7, 'Ryan_Field':7, 'YWCA':2 },
	'Lighthouse':{ 'Campus':1, 'Whole_Food':4, 'Beach':5, 'Cinema':7, 'Lighthouse':0, 'Ryan_Field':1, 'YWCA':15 },
	'Ryan_Field':{ 'Campus':2, 'Whole_Food':5, 'Beach':7, 'Cinema':7, 'Lighthouse':1, 'Ryan_Field':0, 'YWCA':12 },
	'YWCA':{ 'Campus':12, 'Whole_Food':8, 'Beach':12, 'Cinema':2, 'Lighthouse':15, 'Ryan_Field':12, 'YWCA':0 } }

time_map2 = {
	'Campus':{ 'Campus':None, 'Whole_Food':28, 'Beach':13, 'Cinema':None, 'Lighthouse':11, 'Ryan_Field':None, 'YWCA':None },
	'Whole_Food':{ 'Campus':14, 'Whole_Food':None, 'Beach':14, 'Cinema':13, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':None },
	'Beach':{ 'Campus':14, 'Whole_Food':14, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':None },
	'Cinema':{ 'Campus':None, 'Whole_Food':14, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':12 },
	'Lighthouse':{ 'Campus':11, 'Whole_Food':None, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':11, 'YWCA':None },
	'Ryan_Field':{ 'Campus':None, 'Whole_Food':None, 'Beach':None, 'Cinema':None, 'Lighthouse':12, 'Ryan_Field':None, 'YWCA':15 },
	'YWCA':{ 'Campus':None, 'Whole_Food':None, 'Beach':None, 'Cinema':13, 'Lighthouse':None, 'Ryan_Field':15, 'YWCA':None } }


dis_map5 = {
	'Campus':{ 'Campus':0, 'Whole_Food':3, 'Beach':5, 'Cinema':5, 'Lighthouse':1, 'Ryan_Field':2, 'YWCA':12, 'CVS': 4 },
	'Whole_Food':{ 'Campus':3, 'Whole_Food':0, 'Beach':3, 'Cinema':3, 'Lighthouse':4, 'Ryan_Field':5, 'YWCA':8, 'CVS': 3 },
	'Beach':{ 'Campus':5, 'Whole_Food':3, 'Beach':0, 'Cinema':8, 'Lighthouse':5, 'Ryan_Field':7, 'YWCA':12, 'CVS': 6 },
	'Cinema':{ 'Campus':5, 'Whole_Food':3, 'Beach':8, 'Cinema':0, 'Lighthouse':7, 'Ryan_Field':7, 'YWCA':2, 'CVS': 4 },
	'Lighthouse':{ 'Campus':1, 'Whole_Food':4, 'Beach':5, 'Cinema':7, 'Lighthouse':0, 'Ryan_Field':1, 'YWCA':15, 'CVS': 5 },
	'Ryan_Field':{ 'Campus':2, 'Whole_Food':5, 'Beach':7, 'Cinema':7, 'Lighthouse':1, 'Ryan_Field':0, 'YWCA':12 , 'CVS': 4},
	'YWCA':{ 'Campus':12, 'Whole_Food':8, 'Beach':12, 'Cinema':2, 'Lighthouse':15, 'Ryan_Field':12, 'YWCA':0, 'CVS': 5 }, 
	'CVS': { 'Campus':12, 'Whole_Food':8, 'Beach':12, 'Cinema':2, 'Lighthouse':15, 'Ryan_Field':12, 'YWCA':0, 'CVS': 0}}

time_map5 = {
	'Campus':{ 'Campus':None, 'Whole_Food':28, 'Beach':13, 'Cinema':None, 'Lighthouse':11, 'Ryan_Field':None, 'YWCA':None, 'CVS': None },
	'Whole_Food':{ 'Campus':14, 'Whole_Food':None, 'Beach':14, 'Cinema':13, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':None, 'CVS': 6 },
	'Beach':{ 'Campus':14, 'Whole_Food':14, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':None, 'CVS': None },
	'Cinema':{ 'Campus':None, 'Whole_Food':14, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':12, 'CVS': None },
	'Lighthouse':{ 'Campus':11, 'Whole_Food':None, 'Beach':None, 'Cinema':None, 'Lighthouse':None, 'Ryan_Field':11, 'YWCA':None, 'CVS': None },
	'Ryan_Field':{ 'Campus':None, 'Whole_Food':None, 'Beach':None, 'Cinema':None, 'Lighthouse':12, 'Ryan_Field':None, 'YWCA':15, 'CVS': None },
	'YWCA':{ 'Campus':None, 'Whole_Food':None, 'Beach':None, 'Cinema':13, 'Lighthouse':None, 'Ryan_Field':15, 'YWCA':None, 'CVS': None }, 
	'CVS': { 'Campus':7, 'Whole_Food':None, 'Beach':None, 'Cinema':6, 'Lighthouse':None, 'Ryan_Field':None, 'YWCA':None, 'CVS': None } }

dis_mapM = {
	'a': { 'a':0, 'b':1, 'c':2, 'd':3, 'e':1, 'f':2, 'g':3, 'h':4, 'i':2, 'j':3, 'k':4, 'l':5, 'm':3, 'n':4, 'o':5, 'p':6},
	'b': { 'a':1, 'b':0, 'c':1, 'd':2, 'e':2, 'f':1, 'g':2, 'h':3, 'i':3, 'j':2, 'k':3, 'l':4, 'm':4, 'n':3, 'o':4, 'p':5},
	'c': { 'a':2, 'b':1, 'c':0, 'd':1, 'e':3, 'f':2, 'g':1, 'h':2, 'i':4, 'j':3, 'k':2, 'l':3, 'm':5, 'n':4, 'o':3, 'p':4},
	'd': { 'a':3, 'b':2, 'c':1, 'd':0, 'e':4, 'f':3, 'g':2, 'h':1, 'i':5, 'j':4, 'k':3, 'l':2, 'm':6, 'n':5, 'o':4, 'p':3},
	'e': { 'a':1, 'b':2, 'c':3, 'd':4, 'e':0, 'f':1, 'g':2, 'h':3, 'i':1, 'j':2, 'k':3, 'l':4, 'm':2, 'n':3, 'o':4, 'p':5},
	'f': { 'a':2, 'b':1, 'c':2, 'd':3, 'e':1, 'f':0, 'g':1, 'h':2, 'i':2, 'j':1, 'k':2, 'l':3, 'm':3, 'n':2, 'o':3, 'p':4},
	'g': { 'a':3, 'b':2, 'c':1, 'd':2, 'e':2, 'f':1, 'g':0, 'h':1, 'i':3, 'j':2, 'k':1, 'l':2, 'm':4, 'n':3, 'o':2, 'p':3},
	'h': { 'a':4, 'b':3, 'c':2, 'd':1, 'e':3, 'f':2, 'g':1, 'h':0, 'i':4, 'j':3, 'k':2, 'l':1, 'm':5, 'n':4, 'o':2, 'p':2},
	'i': { 'a':2, 'b':3, 'c':4, 'd':5, 'e':1, 'f':2, 'g':3, 'h':4, 'i':0, 'j':1, 'k':2, 'l':3, 'm':1, 'n':2, 'o':3, 'p':4},
	'j': { 'a':3, 'b':2, 'c':3, 'd':4, 'e':2, 'f':1, 'g':2, 'h':3, 'i':2, 'j':0, 'k':1, 'l':2, 'm':2, 'n':1, 'o':2, 'p':3},
	'k': { 'a':4, 'b':3, 'c':2, 'd':3, 'e':3, 'f':2, 'g':1, 'h':2, 'i':2, 'j':1, 'k':0, 'l':1, 'm':3, 'n':2, 'o':1, 'p':2},
	'l': { 'a':5, 'b':4, 'c':3, 'd':2, 'e':4, 'f':3, 'g':2, 'h':1, 'i':3, 'j':2, 'k':1, 'l':0, 'm':4, 'n':3, 'o':2, 'p':1},
	'm': { 'a':3, 'b':4, 'c':5, 'd':6, 'e':2, 'f':3, 'g':4, 'h':5, 'i':1, 'j':2, 'k':3, 'l':4, 'm':0, 'n':1, 'o':2, 'p':3},
	'n': { 'a':4, 'b':3, 'c':4, 'd':5, 'e':3, 'f':2, 'g':3, 'h':4, 'i':2, 'j':1, 'k':2, 'l':3, 'm':1, 'n':0, 'o':1, 'p':2},
	'o': { 'a':5, 'b':4, 'c':3, 'd':4, 'e':4, 'f':3, 'g':2, 'h':3, 'i':3, 'j':2, 'k':1, 'l':2, 'm':2, 'n':1, 'o':0, 'p':1},
	'p': { 'a':6, 'b':5, 'c':4, 'd':3, 'e':5, 'f':4, 'g':3, 'h':2, 'i':4, 'j':3, 'k':2, 'l':1, 'm':3, 'n':2, 'o':1, 'p':0}
}

time_mapM = {
	'a': { 'a':None, 'b':1, 'c':None, 'd':None, 'e':1, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None, 'l':None, 'm':None, 'n':None, 'o':None, 'p':None},
	'b': { 'a':1, 'b':None, 'c':1, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None, 'l':None, 'm':None, 'n':None, 'o':None, 'p':None},
	'c': { 'a':None, 'b':1, 'c':None, 'd':1, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None, 'l':None, 'm':None, 'n':None, 'o':None, 'p':None},
	'd': { 'a':None, 'b':None, 'c':1, 'd':None, 'e':None, 'f':None, 'g':None, 'h':1, 'i':None, 'j':None, 'k':None, 'l':None, 'm':None, 'n':None, 'o':None, 'p':None},
	'e': { 'a':1, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':1, 'j':None, 'k':None, 'l':None, 'm':None, 'n':None, 'o':None, 'p':None},
	'f': { 'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':1, 'h':None, 'i':None, 'j':1, 'k':None, 'l':None, 'm':None, 'n':None, 'o':None, 'p':None},
	'g': { 'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':1, 'g':None, 'h':1, 'i':None, 'j':None, 'k':None, 'l':None, 'm':None, 'n':None, 'o':None, 'p':None},
	'h': { 'a':None, 'b':None, 'c':None, 'd':1, 'e':None, 'f':None, 'g':1, 'h':None, 'i':None, 'j':None, 'k':None, 'l':None, 'm':None, 'n':None, 'o':None, 'p':None},
	'i': { 'a':None, 'b':None, 'c':None, 'd':None, 'e':1, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None, 'l':None, 'm':1, 'n':None, 'o':None, 'p':None},
	'j': { 'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':1, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None, 'l':None, 'm':None, 'n':1, 'o':None, 'p':None},
	'k': { 'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None, 'l':1, 'm':None, 'n':None, 'o':None, 'p':None},
	'l': { 'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':1, 'l':None, 'm':None, 'n':None, 'o':None, 'p':1},
	'm': { 'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':1, 'j':None, 'k':None, 'l':None, 'm':None, 'n':None, 'o':None, 'p':None},
	'n': { 'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':1, 'k':None, 'l':None, 'm':None, 'n':None, 'o':1, 'p':None},
	'o': { 'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None, 'l':None, 'm':None, 'n':1, 'o':None, 'p':1},
	'p': { 'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None, 'l':1, 'm':None, 'n':None, 'o':1, 'p':None}
}

time_mapT = {
	'a': {'a':None, 'b':1, 'c':1, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None},
	'b': {'a':None, 'b':None, 'c':None, 'd':1, 'e':1, 'f':1, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None},
	'c': {'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':1, 'h':1, 'i':None, 'j':None, 'k':None},
	'd': {'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None},
	'e': {'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None},
	'f': {'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':1, 'j':1, 'k':None},
	'g': {'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None},
	'h': {'a':None, 'b':None, 'c':None, 'd':None, 'e':1, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':1},
	'i': {'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None},
	'j': {'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None},
	'k': {'a':None, 'b':None, 'c':None, 'd':None, 'e':None, 'f':None, 'g':None, 'h':None, 'i':None, 'j':None, 'k':None}
}

def interrupt(a,b):
	sys.exit(1)

class UnitTests(unittest.TestCase):

	def test1(self):
		expand.expand_count = 0
		path = sc.breadth_first_search(time_map1, 'Campus', 'Ryan_Field')
		self.assertEqual(path, ['Campus', 'Lighthouse', 'Ryan_Field'])
		self.assertEqual(expand.expand_count, 5)

	def test2(self):
		expand.expand_count = 0
		path = sc.breadth_first_search(time_mapM, 'a', 'g')
		self.assertEqual(path, ['a', 'b', 'c', 'd', 'h', 'g'])
		self.assertEqual(expand.expand_count, 8)

	def test3(self):
		expand.expand_count = 0
		path = sc.depth_first_search(time_mapT, 'a', 'e')
		self.assertEqual(path, ['a', 'c', 'h', 'e'])
		self.assertEqual(expand.expand_count, 4)
	
	def test4(self):
		expand.expand_count = 0
		path = sc.depth_first_search(time_mapT, 'a', 'd')
		self.assertEqual(path, ['a', 'b', 'd'])
		self.assertEqual(expand.expand_count, 11)	

	def test5(self):
		#signal.signal(signal.SIGALRM, interrupt)
		expand.expand_count = 0
		#signal.alarm(30)
		path = sc.a_star_search(dis_map2, time_map2, 'Whole_Food', 'Ryan_Field')
		self.assertEqual(path, ['Whole_Food', 'Campus', 'Lighthouse', 'Ryan_Field'])
		self.assertEqual(expand.expand_count, 5)

	def test6(self):
		#signal.signal(signal.SIGALRM, interrupt)
		expand.expand_count = 0
		#signal.alarm(30)
		path = sc.a_star_search(dis_map2, time_map2, 'YWCA', 'Campus')
		self.assertEqual(path, ['YWCA', 'Ryan_Field', 'Lighthouse', 'Campus'])
		self.assertEqual(expand.expand_count, 5)

	def test7(self):
		#signal.signal(signal.SIGALRM, interrupt)
		expand.expand_count = 0
		#signal.alarm(30)
		path = sc.a_star_search(dis_map5, time_map5, 'CVS', 'Whole_Food')
		self.assertEqual(path, ['CVS', 'Cinema', 'Whole_Food'])
		self.assertEqual(expand.expand_count, 3)

	def test8(self):
		#signal.signal(signal.SIGALRM, interrupt)
		expand.expand_count = 0
		#signal.alarm(30)
		path = sc.a_star_search(dis_map5, time_map5, 'Ryan_Field', 'CVS')
		self.assertEqual(path, ['Ryan_Field', 'YWCA', 'Cinema', 'Whole_Food', 'CVS'])
		self.assertEqual(expand.expand_count, 7)

	def test9(self):
		#signal.signal(signal.SIGALRM, interrupt)
		expand.expand_count = 0
		#signal.alarm(30)
		path = sc.a_star_search(dis_map5, time_map5, 'Campus', 'CVS')
		self.assertEqual(path, ['Campus', 'Beach', 'Whole_Food', 'CVS'])
		self.assertEqual(expand.expand_count, 5)

	def test10(self):
		#signal.signal(signal.SIGALRM, interrupt)
		expand.expand_count = 0
		#signal.alarm(30)
		path = sc.a_star_search(dis_map5, time_map5, 'Campus', 'Cinema')
		self.assertEqual(path, ['Campus', 'Beach', 'Whole_Food', 'CVS', 'Cinema'])
		self.assertEqual(expand.expand_count, 6)

	def test11(self):
		#signal.signal(signal.SIGALRM, interrupt)
		expand.expand_count = 0
		#signal.alarm(30)
		path = sc.a_star_search(dis_mapM, time_mapM, 'a', 'p')
		self.assertEqual(path, ['a', 'b', 'c', 'd', 'h', 'g', 'f', 'j', 'n', 'o', 'p'])
		self.assertEqual(expand.expand_count, 13)

	def test12(self):
		#signal.signal(signal.SIGALRM, interrupt)
		expand.expand_count = 0
		#signal.alarm(30)
		path = sc.a_star_search(dis_mapM, time_mapM, 'h', 'p')
		self.assertEqual(path, ['h', 'g', 'f', 'j', 'n', 'o', 'p'])
		self.assertEqual(expand.expand_count, 8)

	def test13(self):
		#signal.signal(signal.SIGALRM, interrupt)
		expand.expand_count = 0
		#signal.alarm(30)
		path = sc.a_star_search(dis_mapM, time_mapM, 'h', 'a')
		self.assertEqual(path, ['h', 'd', 'c', 'b', 'a'])
		self.assertEqual(expand.expand_count, 4)

	def test14(self):
		#signal.signal(signal.SIGALRM, interrupt)
		expand.expand_count = 0
		#signal.alarm(30)
		path = sc.a_star_search(dis_mapM, time_mapM, 'l', 'n')
		self.assertEqual(path, ['l', 'p', 'o', 'n'])
		self.assertEqual(expand.expand_count, 4)

if __name__== "__main__": unittest.main()
