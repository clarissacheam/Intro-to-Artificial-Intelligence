from expand import expand
from queue import SimpleQueue, PriorityQueue
from collections import deque

def a_star_search (dis_map, time_map, start, end):
# This implementation uses PriorityQueue to help facilitate getting the lowest f-score
# by using fscore as the key for prioritization purpose in the priority queue
	unvisited = PriorityQueue()
	trackings = {start: {"gscore": 0, "fscore": 0, "prev": None}}
	unvisited.put((0, start))
	visited = {}
	found = False

	while not unvisited.empty():
		curr = unvisited.get()
		min_node = curr[1]

		#found the target
		if min_node == end:
			visited[min_node] = trackings[min_node]
			found = True
			break
		#skip if we have visited the node before
		if min_node not in visited.keys():
			visited[min_node] = trackings[min_node]
			nodes = expand(min_node, time_map)
			for n in nodes:
				#compute g-score and f-score
				gscore = time_map[min_node][n] + trackings[min_node]['gscore']
				fscore = int (gscore + dis_map[n][end])
				#update tracking only if new gscore is smaller
				if n in trackings.keys():
					if gscore < trackings[n]['gscore']:
						trackings[n]['gscore'] = gscore
						trackings[n]['fscore'] = fscore
						trackings[n]['prev'] = min_node
				else:
					trackings[n] = {'gscore': gscore, 'fscore': fscore, 'prev': min_node}
				unvisited.put((fscore, n))
			#once used, pop out of trackings
			trackings.pop(min_node)
	#prepare shortest path from visited container
	path = deque()
	if found == True:
		n = end
		while visited[n]['prev'] is not None:
			path.appendleft(n)
			n = visited[n]['prev']
		path.appendleft(start)
	return list(path)

def depth_first_search(time_map, start, end):
	# keep track of visited nodes
	visited = set()
	# level and node are pushed onto the stack. level is for identifying the depth where the
	# target node are found, this is to help backtrace of path from target node to start
	# when target it found
	stack = [(0, start)]
	tracks = {}
	found = False
	level_idx = 0

	while stack:
		(level, s) = stack.pop()
		level_idx = level
		visited.add(s)
		# tracks are used to track the path of the search
		if level in tracks.keys():
			if s not in tracks[level]:
				tracks[level].append(s)
		else:
			tracks[level] = [s]
		# target found, we exit the loop
		if s == end:
			found = True
			break
		else:
			# if not, we find all the visitable children and push to the stack
			nodes = expand(s, time_map)
			for n in nodes:
				stack.append((level + 1, n))
	# when target is found, we backtrace the path from target node to start node
	# using information in track (visited nodes) and time_map (hint path is reachable)
	if found:
		path = deque()
		path.append(end)
		n = end
		for lvl in reversed(range(level_idx + 1)):
			for t in tracks[lvl]:
				if time_map[t][n] is not None:
					n = t
					path.appendleft(t)
	return list(path)

def breadth_first_search(time_map, start, end):
	# keep track of visited nodes
	visited = set()
	# level and node are put onto the queue. level is for identifying the depth the
	# target node are found, this is to help backtrace of path from target node to start
	# when target it found
	queue = SimpleQueue()
	tracks = {}
	found = False
	level_idx = 0
	queue.put((0, start))
	while queue:
		# dequeue one item from the queue
		(level, s) = queue.get()
		# making sure we only visit the node once
		if s in visited:
			continue
		else:
			level_idx = level
			visited.add(s)
			# tracks are used to track the path of the search
			if level in tracks.keys():
				if s not in tracks[level]:
					tracks[level].append(s)
			else:
				tracks[level] = [s]
			# target found, we exit the loop
			if s == end:
				found = True
				break
			else:
				# if not, we find all the visitable children and put it in the queue
				nodes = expand(s, time_map)
				for n in nodes:
					if n not in visited:
						queue.put((level + 1, n))
	# when target is found, we backtrace the path from target node to start node
	# using information in track (visited nodes) and time_map (hint path is reachable)
	if found:
		path = deque()
		path.append(end)
		n = end
		for lvl in reversed(range(level_idx + 1)):
			for t in tracks[lvl]:
				if time_map[n][t] is not None:
					n = t
					path.appendleft(t)
	return list(path)

