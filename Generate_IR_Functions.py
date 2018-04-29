from sympy import *

x=Symbol('x')#, real=True, nonzero=True)
y=Symbol('y')#, real=True)
k=Symbol('k')#, real=True)

#Dictionnary used for fast switch from RPN/Polish Notation to Infix notation
prec_dict =  {'sqrt':5, 'exp':5,  'log':5, '**':4, '*':3, '/':3, '+':2, '-':2}
assoc_dict = {'sqrt':0, 'exp':0,  'log':0, '**':1, '*':0, '/':0, '+':0, '-':0}
arity_dict = {'sqrt':1, 'exp':1,  'log':1, '**':2, '*':2, '/':2, '+':2, '-':2}

#Check for valid RPN --> True if lst in a valid RPN, false else
def rpn(lst) :
	"""
	Input : a list representing a function
	Output : True if lst represent a valid reverse polish notation, false otherwise
	"""
	stack=[]
	res=""
	for char in lst :
		if(char in l_Binary) :
			if(len(stack)<2) :
				return False
			a=str(stack.pop())
			b=str(stack.pop())
			stack.append('('+a+char+b +')')

		elif (char in l_Unary) :
			if(len(stack)<1) :
				return False
			a=str(stack.pop())
			stack.append(char+'('+a+')')
		else :
			stack.append(char)
	#If final stack length is over 1 then the last computation went wrong... or the input isnt a valid reverse Polish notation
	if(len(stack)!=1) :
		return False
	else :
		return True

#Creating a node class to switch from RPN notation to Infix
class Node:
    def __init__(self,x,op,y=None):
        global prec_dict,assoc_dict,arity_dict
        self.precedence = prec_dict[op]
        self.assocright = assoc_dict[op]
        self.arity = arity_dict[op]
        self.op = op

        if not self.assocright and self > x and \
           isinstance(x, Node) and self.arity == 2:
                self.x = x.x
                self.y = Node(x.y, x.op, y)
        else:
            self.x = x
            self.y = y

    def __str__(self):
        # Actual node is an unary operator
        if self.y == None:
            return self.op+'('+ str(self.x) +')'

        # Determine left side string
        strY = str(self.y)
        if  self.y < self or \
            (self.y == self and self.assocright) or \
            (strY[0] is '-' and self.assocright):

            strY = '('+strY+')'

        # Determine right side string and operator
        strX = str(self.x)
        strOp = self.op
        if self.op is '+' and not isinstance(self.x, Node) and strX[0] is '-':
            strX = strX[1:]
            strOp = '-'
        elif self.op is '-' and not isinstance(self.x, Node) and strX[0] is '-':
            strX = strX[1:]
            strOp = '+'
        elif self.x < self or \
             (self.x == self and not self.assocright and \
              getattr(self.x, 'op', 1) != getattr(self, 'op', 2)):
            strX = '('+strX+ ')'


        return ' '.join([strY, strOp, strX])

	#Determine precedence between nodes
    def __cmp__(self, other):
        if isinstance(other, Node):
            return cmp(self.precedence, other.precedence)
        return cmp(self.precedence, prec_dict.get(other,9))

#Switch from a valid RPN notation to a valid infix notation
def switchNotation(s):
    global prec_dict, arity_dict
    stack=[]
    for token in s:
        if token in prec_dict:
            if arity_dict[token] == 1:
                stack.append(Node(stack.pop(),token))
            elif arity_dict[token] == 2:
                stack.append(Node(stack.pop(),token,stack.pop()))
        else:
            stack.append(token)

    return str(stack[0])


#Check if functions are valid for IR
def checkFunction(function) :
	i=0.1
	dx=diff(function, x)
	#If x inst in dx then the next derivative regarding x will be 
	#equal to zero then the function will not be valid for IR.
	if("x" in str(dx)) :
		dy=diff(function, y)
		dx2= diff(dx, x)
		while(i<=10) :
			j=0.1
			while(j<=1) :
				#As soon one of the next condition isnt filled, the 
				#function isnt valid, we return False.
				try :
					if(function.evalf(subs={x:i, y:j, k:1}) < 0) :
						return False
					if(dx.evalf(subs={x:i, y:j, k:1}) <= 0) :
						return False
					if(dy.evalf(subs={x:i, y:j, k:1}) >= 0) :
						return False
					if(dx2.evalf(subs={x:i, y:j, k:1}) >= 0) :
						return False
				#except ZeroDivisionError :
				#	return ValueError
				except :
					return ValueError

				j=j+0.1
			i=i+0.1
		return True

	else :
		return False

#Generate functions until depth "prof" and check and save every functions 
# deeper than "userDepth". Partial results are saved every "save" times.
def combs(items, prof, userDepth, save) :
	accum = [[],]
	final=[]
	ok=0
	okDone=0
	for pos in range(prof):
		print("Depth : " + str(pos+1))
		old = accum
		accum =  []
		for comb in old:
			for item in items:
				testing=list(comb) + [item]
				b=rpn(testing)
				if((b==True) or list(set([item]) & set(l_Var))==[item] or list(set([item]) & set(l_Unary))==[item]) :
					if(set(testing) & set(l_Var) != [] ) :
						accum.append(testing)
				
				#For less calculation, we only start to check functions deeper than userDepth
				if(pos+1>=userDepth and b==True) :
					if(("x" in testing) and ("y" in testing)) :
						fun = eval(switchNotation(testing))
						if(checkFunction(fun) == True) : #checking for valid functions:
							final.append(fun)
							ok=ok+1
							#Allow to get partials results if calculation are too long.
							#Just need to set "save".
							if(ok==save) :
								okDone+=1
								ok=0
								print(str(okDone*save) + " functions saved...")
								finalLst=set(final)
								finalLstStrings=[]
								for elem in finalLst :
									finalLstStrings.append(str(elem)+'\n')
								gFunc = open('generatedFunctions', 'w')
								gFunc.writelines(finalLstStrings)
								gFunc.close()
					
	return final

#Lists of operators and variables/constants
l_Binary=["+", "*", "/", "-", "**"]
l_Unary=["sqrt", "log", "exp"]
l_Var=["x", "y", "k"]
operators=l_Binary+l_Unary
items = l_Binary+l_Var+l_Unary

depth = int(raw_input("Enter max depth : ")) 
userDepth = int(raw_input("Keep functions >= ? : "))
save = int(raw_input("Save every ? valid results : "))
print("\n")

#Start calculations
finalLst = combs(items, depth, userDepth, save)
print("\nDone.\n\n")

print(str(len(items)) + " items selected.")
#Remove doublets, can be improved
finalLst=set(finalLst)
print("Final list contains : " + str(len(finalLst)))

print("\nSaving in file \"generatedFunctions\"...")
finalLstString=[]
#Switch the list to strings. Allow to create a readable file
for elem in finalLst :
	finalLstString.append(str(elem)+'\n')

gFunc = open('generatedFunctions', 'w')
gFunc.writelines(finalLstString)
gFunc.close()
print('Done.\n')
