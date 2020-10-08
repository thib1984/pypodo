from pathlib import Path
from termcolor import colored
from colorama import Fore, Style

import os
import sys
import re

STR_PATH_HOME__TODO_ = str(Path.home()) + '/.todo'

def help():
	help_txt = """\
	
NAME
       pypodo

SYNOPSIS
       pypodo is a todolist tool which works with a .todo file positionned the root of the home directory
       pypodo [MODE] [PARAMETERS]...

       help  : display this help
            pypodo help
       list  : print the todolist with an index for each task, with tag filtered on [PARAMETER]
            pypodo list #print the todolist
            pypodo list linux #print the todolist filtered on tag linux
       add   : add [PARAMETER]... to the todolist with an index autogenerated
            pypodo add "my first task" "my second task" #add the task "my first task" and the task "my second task" to the todolist
       del   : delete task(s) identified with the index equals to [PARAMETER]... from the todolis
            pypodo del 3 4 #deletes the task identified by index equals 3 and 4	
       tag   : add the tag [PARAMETER[1]] to the task the task identified with the index equals to [PARAMETER[2]]... or without parameters, display the tags of the todolist
            pypodo tag linux 3 4 #add the tag linux to the task identified with the index equals to 3 and 4
            pypodo tag	#print the tags of the todolist
       untag : delete the tag identidied by [PARAMETER1] in the task definied by the [PARAMETER2]... or without parameter, display task without tags
            pypodo untag linux 3 4 #delete the tag linux from the task identified by index equals 3 and 4
            pypodo untag #print the todolist filtered on untagged tasks	
       sort  : reorder the todolist in consecutives index
            pypodo sort	#reorder the todolist in consecutives index	
              			
	"""
	print(help_txt)

# list the .todo possibly filtered on the tags corresponding to the parameter 
def list(open = open):
	check()
	if len(sys.argv) > 3:
		sys.exit(colored("error : 0 or 1 parameter is needed for pypodo list - the tag",'red'))
	vide = 'true'
	with open(STR_PATH_HOME__TODO_, 'r') as f:
		for line in f.readlines():
			# without filter -> we print all
			if len(sys.argv) == 2:
				task = Fore.GREEN + re.sub("#.*","",re.sub("^[^ ]+ ","",line.rstrip('\n')))
				index = Fore.BLUE + line.split(' ', 1)[0]
				tags = Fore.YELLOW + re.sub("^[^#]+ #","#",re.sub("^[^#]+$","",re.sub("^[^ ]+ ","",line.rstrip('\n'))))
				tags = re.sub("#urgent",Fore.RED+"#urgent"+Fore.YELLOW,tags)
				print(index +" "+ task + tags)
				vide = 'false'	
			# with filter -> we check tag
			elif len(sys.argv) == 3:
				if '#'+sys.argv[2] in line:
					#print(line, end = '')
					tag=sys.argv[2]
					# regex to search tags "#toto " or "#toto" at the end of the line
					if re.findall("#"+re.escape(tag)+'( |$)',line.rstrip('\n')):
						task = Fore.GREEN + re.sub("#.*","",re.sub("^[^ ]+ ","",line.rstrip('\n')))
						index = Fore.BLUE + line.split(' ', 1)[0]
						tags = Fore.YELLOW + re.sub("^[^#]+ #","#",re.sub("^[^#]+$","",re.sub("^[^ ]+ ","",line.rstrip('\n'))))
						tags = re.sub("#urgent",Fore.RED+"#urgent"+Fore.YELLOW,tags)
						print(index +" "+ task + tags)
						vide = 'false'
	if vide == 'true':
		if len(sys.argv) == 3:
			print(colored("warning : the filtered todolist is empty","yellow"))
		else:
			print(colored("warning : the todolist is empty","yellow"))




# list the .todo possibly filtered on the tags corresponding to the parameter 
def listnotag(open = open):
	check()
	if len(sys.argv) > 2:
		sys.exit(colored("error : 0 parameter is needed for pypodo listnotag",'red'))
	vide = 'true'
	with open(STR_PATH_HOME__TODO_, 'r') as f:
		for line in f.readlines():
			if not '#' in line:
				task = Fore.GREEN + re.sub("#.*","",re.sub("^[^ ]+ ","",line.rstrip('\n')))
				index = Fore.BLUE + line.split(' ', 1)[0]
				tags = Fore.YELLOW + re.sub("^[^#]+ #","#",re.sub("^[^#]+$","",re.sub("^[^ ]+ ","",line.rstrip('\n'))))
				tags = re.sub("#urgent",Fore.RED+"#urgent"+Fore.YELLOW,tags)
				print(index +" "+ task + tags)
				vide = 'false'
	if vide == 'true':
		print(colored("warning : the filtered todolist with no tag is empty","yellow"))

# list the .todo possibly filtered on the tags corresponding to the parameter 
def listtag(open = open):
	check()
	if len(sys.argv) > 2:
		sys.exit(colored("error : 0 parameter is needed for pypodo listtag",'red'))
	vide = 'true'
	with open(STR_PATH_HOME__TODO_, 'r') as f:
		my_list = []
		for line in f.readlines():
			for part in line.split():
				if "#" in part:
					
					my_list.append(part)
					vide = 'false'
		print(colored("\n".join(sorted(set(my_list))),"green"))
	if vide == 'true':
		print(colored("warning : the filtered todolist with no tag is empty","yellow"))

def sort_uniq(sequence):
	import itertools
	return (x[0] for x in itertools.groupby(sorted(sequence)))
							
# adds the tasks as a parameter to the todolist (by calculating their indexes).					
def add(open = open):
	check()
	if len(sys.argv) < 3:
		sys.exit("error : 1 or more parameter is needed for pypodo add - tasks") 
	else:
		# loop on the indexes
		for x in range(2, len(sys.argv)): 
			task=sys.argv[x]
			# check format : words* #tag1 #tag2 : task at free format, tags in one word prefixed by #
			if not re.findall("^([^# ])([^#])*( #[^ #]+)*$",task):
				print(colored("warning : the task has not a valid format - "+task,"yellow"))
			else: 
				with open(STR_PATH_HOME__TODO_, 'r') as f:
					lines = f.readlines()
				# index calculation	
				if len(lines) > 0:
					last_line = lines[len(lines)-1]
					index = int(last_line.split()[0])+1
				else:
					index = 1
				# adding task to the todolist		
				with open(STR_PATH_HOME__TODO_, 'a') as f:
					f.write(str(index)+" "+task+'\n')		
					print(colored("info : task is added to the todolist - " + str(index)+" "+task,"green"))	

# removes the tasks whose indexes are provided as a parameter	
def delete(open = open):
	check()
	if len(sys.argv) >= 3:
		# loop on the indexes
		for x in range(2, len(sys.argv)):
			index=sys.argv[x]
			# check the numeric format of the index
			if not re.findall("^\\d+$",index):
				print(colored("warning : the index to delete is not in numeric format - " + index,"yellow"))
			else:	
				index_existant = 'false' 
				with open(STR_PATH_HOME__TODO_, 'r') as f:
					lines = f.readlines()
				with open(STR_PATH_HOME__TODO_, 'w') as f:	    
					for line in lines:
						# if the current row doesn't contain the index it is kept
						if not re.findall("^"+index+' ',line):
							f.write(line)
						# else it is deleted by not being copied
						else:
							print(colored("info : task deleted from the todolist - " + line.rstrip('\n'),"green"))
							index_existant = 'true'
				if index_existant == 'false':
					print(colored("warning : no task is deleted from the todolist, not existing index - "+ index,"yellow"))					
	else:
		sys.exit(colored("error : 1 or more parameter is needed for pypodo add - indexes to delete in numeric format","red"))							


# sort the list in successive ascending order
def sort(open = open):
	check()
	if len(sys.argv) != 2:
		sys.exit(colored("error : 0 parameter is needed for pypodo sort","red")) 
	else:
		vide = 'true'
		index=1
		with open(STR_PATH_HOME__TODO_, 'r') as f:
			lines = f.readlines()
		with open(STR_PATH_HOME__TODO_, 'w') as f:	    
			for line in lines:
				# we replace the existing index by the current index that we increment
				replaced = re.sub("^\\d+ ",str(index)+" ", line)
				index=index+1
				f.write(replaced)
				vide = 'false'
		if vide == 'true':
			print(colored("warning : the todolist is empty - nothing to do","yellow"))
		else:
			print(colored("info : the todolist is sorted","green"))
			list(open)		
			
# various checks on the todo file
def check(open = open):
	file_exists = os.path.isfile(STR_PATH_HOME__TODO_) 
	if file_exists:
		with open(STR_PATH_HOME__TODO_, 'r') as f:
			error = 'false'
			for line in f.readlines():
				# verification regex, index + task + possible tags
				if not re.findall("^\\d+ ([^#])+( #[^ #]+)*$",line.rstrip('\n')):
					print(colored("warning : this line has not a valid format in .todo - "+line.rstrip('\n'),"yellow"))
					error = 'true'
		if error == 'true':
			sys.exit(colored("error : verify the .todo file","red"))			
	else:
		open(STR_PATH_HOME__TODO_, "w")

# untag tasks				
def untag(open = open):
	check()
	if len(sys.argv) == 2:
		listnotag(open)
	elif len(sys.argv) >= 4:
		tag=sys.argv[2]
		if not re.findall("^[^ #]+$",tag):
			sys.exit(colored("error : the tag has not a valid format - "+tag),"red")		
		# loop on the indexes
		for x in range(3, len(sys.argv)):
			index=sys.argv[x]
			if not re.findall("^\\d+$",index):
				print(colored("warning : the index to untag is not in numeric format - " + index,"yellow"))
			else:	
				index_trouve = 'false'
				with open(STR_PATH_HOME__TODO_, 'r') as f:
					lines = f.readlines()
				with open(STR_PATH_HOME__TODO_, 'w') as f:	    
					for line in lines:
						if not re.findall("^"+index+' ',line):
							f.write(line)
						if re.findall("^"+index+' ',line):
							if re.findall("#"+re.escape(tag)+'( |$)',line.rstrip('\n')):
								f.write(re.sub("#"+re.escape(tag)+'( |$)' ,"", line).rstrip('\n').rstrip()+'\n')
								print(colored("info : tag deleted from the task of the todolist - " + line.rstrip('\n') + " -> " + re.sub("#"+re.escape(tag)+'( |$)',"", line.rstrip('\n')),"green"))
							else:
								f.write(line)
								print(colored("warning : no tags is deleted from the todolist for the task - "+line.rstrip('\n'),"yellow"))	
							index_trouve = 'true'
				if index_trouve == 'false':
					print(colored("warning : no task with index - "+index,"yellow"))											
	else:
		sys.exit(colored("error : 1 parameter is needed for pypodo untag : the index of the task whose tags to delete","red"))	


# tagging task
def tag(open = open):
	check()
	if len(sys.argv) == 2:
		listtag(open)
	elif len(sys.argv) >= 4:
		tag=sys.argv[2]
		if not re.findall("^[^ #]+$",tag):
			sys.exit(colored("error : the tag has not a valid format - "+tag,'red'))	
		# loop on the indexes		
		for x in range(3, len(sys.argv)):
			index=sys.argv[x]		
			if not re.findall("^\\d+$",index):
				print(colored("warning : the index to tag is not in numeric format - " + index,"yellow"))
			else:	
				index_trouve = 'false'
				with open(STR_PATH_HOME__TODO_, 'r') as f:
					lines = f.readlines()
				with open(STR_PATH_HOME__TODO_, 'w') as f:	    
					for line in lines:
						if not re.findall("^"+index+' ',line):
							f.write(line)
						if re.findall("^"+index+' ',line):
							f.write(line.rstrip('\n')+" #"+tag+"\n")
							print(colored("info : tag added to the task of the todolist - " + line.rstrip('\n') + " -> " + line.rstrip('\n')+" #"+tag,"green")) 
							index_trouve = 'true'	
				if index_trouve == 'false':
					print(colored("warning : no task with number is in the todolist - "+index,"yellow"))										
	else:
		sys.exit(colored("error : 2 or more parameters are needed for pypodo tag : the tag to added and indexes of the task are in numeric format","red"))	

def pypodo():	
	import sys
	if len(sys.argv) == 1:
	    help()
	elif sys.argv[1] == "list":
	    list()
	elif sys.argv[1] == "add":
	    add()
	elif sys.argv[1] == "del":
	    delete()
	elif sys.argv[1] == "sort":
	    sort()    
	elif sys.argv[1] == "help":
	    help()
	elif sys.argv[1] == "untag":
	    untag()
	elif sys.argv[1] == "tag":
	    tag()
	elif sys.argv[1] == "help":
	    help()	 	 
	else:
	     help()	
	      
