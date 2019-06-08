import numpy as np 
import random
import ast
import math
import copy;

itr = 15000;
alpha = 0.5;
gamma = 0.8;
thresh = 50;		# for preventing useless iterations when the answer is found

Q = [];
R = [];
cnt = 0;
LEFT = 0;
UP = 1;
RIGHT = 2;
DOWN = 3;
visited = [];

Dir = { (1,0) : RIGHT , (-1,0) : LEFT , (0,-1) : UP , (0, 1):DOWN}

def getAct(neighborList , state):
	res = [];
	for i in range(0,len(neighborList)):
		tmp = tuple ( [neighborList[i][0] - state[0] , neighborList[i][1] - state[1]] ) ;
		res.append(Dir[tmp]);
	return res;

		
def getMaxAct(actList , state):
	maxInd = actList[0];
	for i in range(1,len(actList)):
		if(Q[state[0]][state[1]][actList[i]] > Q[state[0]][state[1]][maxInd]) :
			maxInd = actList[i];
	Maxes = [];
	for i in range(0,len(actList)):
		if(Q[state[0]][state[1]][actList[i]] == Q[state[0]][state[1]][maxInd]):
			Maxes.append(actList[i]);
	return random.choice(Maxes);


def doAction(maxAct , state):
	if(maxAct == LEFT):
		return (state[0] - 1, state[1]);
	elif(maxAct == UP):
		return (state[0], state[1]-1);
	elif(maxAct == RIGHT):
		return (state[0] + 1, state[1] );
	elif(maxAct == DOWN):
		return (state[0], state[1] + 1);


def getMaxQ(maze, state):
	'''
	actList = getAct(maze.get_neighbors(state),state);
	Max = 0;
	for act in actList:
		if(Max < Q[state[0]][state[1]][act]):
			Max = Q[state[0]][state[1]][act];
	return Max;
	'''
	return max(Q[state[0]][state[1]]);


def R1(maze,state):

	if maze.goal in maze.get_neighbors(state) :
		return 10;

	return 0;


def R2(maze,state):
	
	if maze.goal in maze.get_neighbors(state) :
		return 2*(maze.nrows + maze.ncols);

	if len(maze.get_neighbors(state)) == 1:
		return -2*(maze.nrows + maze.ncols);

	return reduce(lambda x, y: x + y, Q[state[0]][state[1]]) / len(Q[state[0]][state[1]]);


	
def solve(maze):
	path = [];
	state = maze.start;
	global visited;
	visited = [];
	global Q;
	Qp = copy.copy(Q);
	global cnt;
	cnt = 0;
	while ( state != maze.goal ):
		cnt += 1;
		
		actList = getAct(maze.get_neighbors(state),state);
		maxAct = getMaxAct(actList , state);

		if tuple([state,maxAct]) not in visited:
			visited.append(tuple([state,maxAct]));	
			Qp[state[0]][state[1]][maxAct] = (1.0 - alpha) * Q[state[0]][state[1]][maxAct] + alpha*(R1(maze,state)+ gamma*getMaxQ(maze,doAction(maxAct,state)) );

		path.append(state);
		state = doAction(maxAct,state);
	global Q;
	Q = copy.copy(Qp);
	path.append(state);
	
	return path;


def solver(maze):

	global Q,R;
	Q = np.zeros((maze.nrows,maze.ncols,4));
	last  = 0;
	lastCnt = 0;

	L = [];

	for i in range(0,itr):
	
		t = len(solve(maze));

		L.append(t);
		if t != last:	# the answer is changed
			last = t;
			lastCnt = 1;
		else:
			lastCnt += 1;


		if i % 1 == 0:
			print i , t;


		if lastCnt == thresh:	# its been "thresh" iterations that answer was the same so the path is found
			break;
		
		
	print L;
	return solve(maze);

