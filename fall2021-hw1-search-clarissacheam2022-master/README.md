# HW1—Search

## Back Story

You work at a food delivery startup called BigByte. The company consists of two people, Willie and you, both alumni of Nerdwestern University located in Heavanston. Of the two, you take care of software engineering and Willie handles the rest. 

BigByte's target client restaurants and ordering customers are all based in Heavanston, which has a handful of landmarks and a heavily fluctuating traffic pattern. To ensure that your delivery fleet works efficiently, Willie asked you to come up with a route planning system. 

All major map services are expensive and your startup begins its services in a week, so you'll have to come up with something yourself and do it fast. Fortunately, restaurants and Heavanston residents' homes are close to landmarks, and you only need to tell delivery drivers how best to reach one landmark from another. You have a printed map of all Heavanston roads and data from a traffic survey maintained by University Archive. For you, that means you only need to write three (3) more pieces of software before the launch: an implementation each of **Breadth-first Search (BFS)**, **Depth-first Search (DFS)**, and the **A\* algorithm** that all find the best way to travel between any pair of landmarks in town. You're implementing three algorithms because you want to eventually do a comparative analysis of all three to select the best one.

## Task Parameters

A diagram explaining the relative position of major landmarks of Heavanston is shown below. 

<img src="map.png" width="60%">

Now, Willie understands the gravity of the task he's handed you. As such, he has supplied you with a few different maps you can use to develop the software. These maps can be found in the `a_star_gradingtests.py` file. The file also has tests that you can use to test your software. **Willie's only going to accept your work if your code passes all the tests.** Additionally, in order to test for robustness of your softare, **Willie may also use some additional tests that he's not willing to show you now.** They will be different from the tests he's supplied you with but similar enough that if your implementation is correct, it should pass the unseen tests too as long as you don't obtain any shortcuts (e.g., hardcoding, writing code specifically aimed at passing the tests while not implementing the desired algorithm, etc.) 

Things to note about the maps:

1. If you look at the test functions, you'll see that certain tests use certain maps. Please be mindful of that.

2. The maps for DFS don't have any loops, so even if you don't keep a list of expanded nodes, you should be alright. Note that this means that once a node is expanded, it doesn't show up again further down that same branch. However, the same node can show up on different branches of the tree, which means in the entire search, the same node can be expanded more than once. In case you choose to keep track of expanded nodes, that should not prevent you from expanding a node that you already expanded on a different branch earlier.

3. The maps for BFS, however, may contain loops, so it's best to maintain a list of expanded nodes. Willie said the *Artificial Intelligence: A Modern Approach* book has stuff about BFS.

4. Your algorithms will the calculate fastest (thinking shortest in time) route between any pairs of the landmarks.

5. Your A\* function will be given two routing maps as inputs. The first map specifies the straight-line distance between two landmarks (Willie measured the printed map and did the data entry); we will refer to this as the **distance map**. The second map is based on the data from the Archive traffic survey. It specifies the expected time it takes a driver to go from one landmark to a neigbhoring landmark; we will refer to this as the **time map**. For all three implementations (BFS, DFS, and A\*), you will use the time differences between places as the main metric, not distance. However, for A\*, you will use the distances between places as the **heuristic** (how far you're from the destination). In other words, for A\*, the distance from the start to your current location will be time-based, but the distance from your current location to the destination will be distance-based.

When passed to your A\* implementation, both the distance map and the time map are stored in the same format (a Python dictionary). The following is an example time map.

```python
Time_map = {
'Campus':
	{'Campus':None,'Whole_Food':4,'Beach':3,'Cinema':None,'Lighthouse':1,'Ryan Field':None,'YWCA':None},
'Whole_Food':
	{'Campus':4,'Whole_Food':None,'Beach':4,'Cinema':3,'Lighthouse':None,'Ryan Field':None,'YWCA':None},
'Beach':
	{'Campus':4,'Whole_Food':4,'Beach':None,'Cinema':None,'Lighthouse':None,'Ryan Field':None,'YWCA':None},
'Cinema':
	{'Campus':None,'Whole_Food':4,'Beach':None,'Cinema':None,'Lighthouse':None,'Ryan Field':None,'YWCA':2},
'Lighthouse':
	{'Campus':1,'Whole_Food':None,'Beach':None,'Cinema':None,'Lighthouse':None,'Ryan Field':1,'YWCA':None},
'Ryan Field':
	{'Campus':None,'Whole_Food':None,'Beach':None,'Cinema':None,'Lighthouse':2,'Ryan Field':None,'YWCA':5},
'YWCA':
	{'Campus':None,'Whole_Food':None,'Beach':None,'Cinema':3,'Lighthouse':None,'Ryan Field':5,'YWCA':None}}
```

In this example, the traffic time between Campus and Beach is `3`. `None` indicates that there is no road which directly connects the two landmarks. Off-road driving is prohibited by local law, so drivers must only take the roads marked on the diagram above. Combining this legal requirement and with the volatile traffic pattern of Heavanston, it is certain that the distance map can only be used as a heuristic for the A\* algorithm. It is also noteworthy that the time it takes traveling on the two sides of the same road is most likely different. 

## Homework Deliverable

For this homework, you must implement all three (3) functions in `student_code.py`. Each function must return a path from landmark `start` to landmark `end`.

Note that:

* The result must be a list of strings. Each string contains _only_ the name of a landmark. The order of the strings in the list denotes the order in which the landmarks are reached along the path;
* The result list should _begin_ with the name of the `start` landmark and _terminate_ with the name of the `end` landmark. (Thus, the path from `A` to `A` is the list `[A]`);
* The cost of a path between two connected landmarks is the total expected traffic time that must be spent travelling all landmarks in the order specified by the path. 

Your `a_star_search` function must implement an A\* **graph** search algorithm, and it must use the `expand` function in `expand.py`. With the `expand` function, we can verify that the correct number of nodes are expanded. As a reminder, graph search algorithms do not expand nodes that have already been visited. 

Your BFS and DFS implementations will essentially be **tree** search algorithms operating on the graphs that the maps form.

Furthermore, the Autograder that Willie will use to test your code assumes that all of the code that is needed to properly grade your assignment submission is included in `student_code.py`. Please adhere to this constraint as you develop your response. 

Additionally, you should feel invited to use Python modules for your data structures, but you need to implement A\* yourself.
