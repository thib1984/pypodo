from pathlib import Path

def list():
    check()
    import sys
    home = str(Path.home())
    with open(home+"/.todo", 'r') as f:
    	for line in f.readlines():
    		if len(sys.argv) < 2:
    			print(line, end = '')		
    		elif '#'+sys.argv[1] in line:
    			print(line, end = '')

def add():
    check()
    import sys
    home = str(Path.home())
    with open(home+"/.todo", 'r') as f:
    	lines = f.readlines()
    	if len(lines) > 0:
    		last_line = lines[len(lines)-1]
    		index = int(last_line.split()[0])+1
    	else:
    		index = 1	
    with open(home+"/.todo", 'a') as f:
    	f.write(str(index)+" "+sys.argv[1]+'\n')		

def delete():
	check()
	import sys
	import re
	home = str(Path.home())
	if len(sys.argv) > 1:
		with open(home+"/.todo", 'r') as f:
			lines = f.readlines()
		with open(home+"/.todo", 'w') as f:	    
			for line in lines:
				if not re.findall("^"+sys.argv[1]+' ',line):
					f.write(line)		

def clear():
	check()
	import sys
	import re
	index=1
	home = str(Path.home())
	with open(home+"/.todo", 'r') as f:
		lines = f.readlines()
	with open(home+"/.todo", 'w') as f:	    
		for line in lines:
			replaced = re.sub("^\d+ ",str(index)+" ", line)
			index=index+1
			f.write(replaced)

def check():
	import sys
	import re
	index=1
	home = str(Path.home())
	with open(home+"/.todo", 'a+') as f:
		lines = f.readlines()   
		for line in lines:
			if not re.findall("^\d+ ",line):
				sys.exit("erreur : vérifier le fichier .todo")
				

if __name__ == "__list__":
    list()
if __name__ == "__add__":
    add()
if __name__ == "__delete__":
    delete()
if __name__ == "__clear__":
    clear()    
