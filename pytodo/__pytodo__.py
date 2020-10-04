from pathlib import Path

def help():
	help_txt = """\
# pytodo

pytodo is a todolist program who works with a .todo file at the root of the home directory

## Install

```
git clone https://github.com/thib1984/pytodo.git
cd pytodo
pip3 install --user .
```
or directly
```
pip3 install --user git+https://github.com/thib1984/pytodo.git#egg=pytodo
```

## Utilisation

```
pytodo-add "to do work #name_of_tag" #add the task 'to do work' with the tag 'name_of_tag'
pytodo-add "to do other_work #name_of_other_tag" #add the other task 'to do other_work' with the tag 'name_of_other_tag'
pytodo-add "to do other_big_work #name_of_other_tag" #add the other task 'to do other_big_work' with the tag 'name_of_tag'
pytodo-list #print the todolist with an index for each task
>1 to do work #name_of_tag
>2 to do other_work #name_of_other_tag
>3 to do other_big_work #name_of_other_tag
pytodo-list "name_of_tag" #print the todolist filtered to the tag name_of_tag
>1 to do work #name_of_tag
pytodo-del 2 #delete the second task of the todolist
pytodo-list #print the todolist with an index for each task
>1 to do work #name_of_tag
>3 to do other_big_work #name_of_other_tag
pytodo-clear #reorder the todolist in consecutives index
pytodo-list #print the todolist with an index for each task
>1 to do work #name_of_tag
>2 to do other_big_work #name_of_other_tag
pytodo-tag 1 new_tag #add a tag to the first task
pytodo-list #print the todolist with an index for each task
>1 to do work #name_of_tag #new_tag
>2 to do other_big_work #name_of_other_tag
pytodo-untag 1 #remove tags from the first task
pytodo-list #print the todolist with an index for each task
>1 to do work
>2 to do other_big_work #name_of_other_tag
```

## Uninstall

```
pip3 uninstall pytodo
```
	"""
	print(help_txt)

def list():
	import sys
	check()
	home = str(Path.home())
	if len(sys.argv) > 2:
		sys.exit("0 ou 1 parametre attendu pour pytodo-list : le tag")
	with open(home+"/.todo", 'r') as f:
		for line in f.readlines():
			if len(sys.argv) == 1:
				print(line, end = '')	
			elif len(sys.argv) == 2:
				if '#'+sys.rgv[1] in line:
					print(line, end = '')
					
def add():
	import sys
	check()
	home = str(Path.home())
	if len(sys.argv) != 2:
		sys.exit("1 et 1 seul parametre attendu pour pytodo-add : la tache a ajouter") 
	else:
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
	import sys
	import re
	check()
	home = str(Path.home())
	if len(sys.argv) == 2:
		if not re.findall("^\d+$",sys.argv[1]):
			sys.exit("1 et 1 seul parametre attendu pour pytodo-del : l index a supprimer au format numerique")		
		with open(home+"/.todo", 'r') as f:
			lines = f.readlines()
		with open(home+"/.todo", 'w') as f:	    
			for line in lines:
				if not re.findall("^"+sys.argv[1]+' ',line):
					f.write(line)	
	else:
		sys.exit("1 et 1 seul parametre pour attendu pytodo-del : l index a supprimer au format numerique")							

def clear():
	import sys
	import re
	check()
	if len(sys.argv) != 1:
		sys.exit("0 parametre attendu pour pytodo-clear") 
	else:
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
	import os
	index=1
	home = str(Path.home())
	file_exists = os.path.isfile(home+"/.todo") 
	if file_exists:
		with open(home+"/.todo", 'r') as f:
			for line in f.readlines():
				if not re.findall("^\d+ ",line):
					sys.exit("erreur : vérifier le fichier .todo")
	else:
		open(home+"/.todo", "w")

				
def untag():
	import sys
	import re
	check()
	home = str(Path.home())
	if len(sys.argv) == 2:
		if not re.findall("^\d+$",sys.argv[1]):
			sys.exit("1 et 1 seul parametre attendu pour pytodo-untag : l index dont le tag doit etre supprime")		
		with open(home+"/.todo", 'r') as f:
			lines = f.readlines()
		with open(home+"/.todo", 'w') as f:	    
			for line in lines:
				if not re.findall("^"+sys.argv[1]+' ',line):
					f.write(line)
				if re.findall("^"+sys.argv[1]+' ',line):
					f.write(re.sub(" #.*" ,"", line))	
					#f.write(" ".join(line,"#"+sys.argv[2]))								
	else:
		sys.exit("1 et 1 seul parametre pour attendu pytodo-untag : l index dont le tag doit etre supprime")	


def tag():
	import sys
	import re
	check()
	home = str(Path.home())
	if len(sys.argv) == 3:
		if not re.findall("^\d+$",sys.argv[1]):
			sys.exit("2 parametres attendus pour pytodo-tag : l index de la tache au format numérique et le tag à ajouter")		
		with open(home+"/.todo", 'r') as f:
			lines = f.readlines()
		with open(home+"/.todo", 'w') as f:	    
			for line in lines:
				if not re.findall("^"+sys.argv[1]+' ',line):
					f.write(line)
				if re.findall("^"+sys.argv[1]+' ',line):
					f.write(line.rstrip('\n')+" #"+sys.argv[2]+"\n")
					#f.write(" ".join(line,"#"+sys.argv[2]))
					#f.write(re.sub(".$" ," #"+sys.argv[2], line))								
	else:
		sys.exit("2 parametres attendus pour pytodo-tag : l index de la tache au format numérique et le tag à ajouter")	

if __name__ == "__list__":
    list()
if __name__ == "__add__":
    add()
if __name__ == "__delete__":
    delete()
if __name__ == "__clear__":
    clear()    
if __name__ == "__help__":
    help()
if __name__ == "__untag__":
    untag()
if __name__ == "__tag__":
    tag()
