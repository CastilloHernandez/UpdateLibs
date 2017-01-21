import os
import hashlib
import argparse
import shutil

def hash_file(filename):
   # Calcula hash SHA-1 de un archivo en bloques de 1024 bytes 

   h = hashlib.sha1()
   with open(filename,'rb') as file:
       chunk = 0
       while chunk != b'':
           chunk = file.read(1024)
           h.update(chunk)
   return h.hexdigest()

def BuscarLibrerias(dir):
	r=[]
	for root, dirs, files in os.walk(dir):
		for file in files:
			f,e = os.path.splitext(file)
			if e.upper() == '.DLL':
				r.append(str(os.path.join(root,file)))
	return sorted(r)	
	
def BuscarBinDebug(dir):
	r=[]
	for root, dirs, files in os.walk(dir):
		for d in dirs:
			if os.path.basename(root).upper() == 'BIN' and d.upper() == 'DEBUG':
				r.append(os.path.join(root,d))
	return sorted(r)

parser = argparse.ArgumentParser(prog='updatelibs')
parser.add_argument('directorio',nargs='*')
opt = parser.parse_args()

directorios=[]
if len(opt.directorio):
	directorios=opt.directorio
else:
	directorios.append('.')

for directorio in directorios:
	for d in BuscarBinDebug(directorio):
		print '> ' + d
		for f in BuscarLibrerias(d):
			libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(f))),'lib')
			if not os.path.isdir(libdir):
				os.makedirs(libdir)
			dest=os.path.join(libdir, os.path.basename(f))
			if os.path.exists(dest):
				hashdest=hash_file(dest)
				if hashdest == hash_file(f):
					print '  ' + os.path.basename(f)
				else:
					print '* ' + os.path.basename(f)
					shutil.copyfile(f, dest)
			else:
				print '+ ' + os.path.basename(f)
				shutil.copyfile(f, dest)

