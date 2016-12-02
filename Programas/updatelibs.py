import os
#import mimetypes
#import hashlib
#import urllib2
import argparse
import shutil

#def get_redirected_url(url):
#	opener = urllib2.build_opener(urllib2.HTTPRedirectHandler)
#	request = opener.open(url)
#	return request.url

def BuscarLibrerias(dir):
	r=[]
	for root, dirs, files in os.walk(dir):
		for file in files:
			f,e = os.path.splitext(file)
			if e.upper() == '.DLL':
				#print str(os.path.join(root,file))
				r.append(str(os.path.join(root,file)))
	return sorted(r)	
def BuscarBinDebug(dir):
	r=[]
	for root, dirs, files in os.walk(dir):
		for d in dirs:
			if os.path.basename(root).upper() == 'BIN' and d.upper() == 'DEBUG':
				r.append(root)
	return sorted(r)

parser = argparse.ArgumentParser(prog='updatelibs')
parser.add_argument('-branch',default='trunk')
parser.add_argument('directorio',nargs='*')
opt = parser.parse_args()

directorios=[]
if len(opt.directorio):
	directorios=opt.directorio
else:
	directorios.append('.')

for directorio in directorios:
	for d in BuscarBinDebug(directorio):
		print 'Directorio ' + d
		for f in BuscarLibrerias(d):
			libdir = os.path.join( os.path.dirname(os.path.dirname(os.path.dirname(f))),'lib')
			if not os.path.isdir(libdir):
				os.makedirs(libdir)
			print 'Copiando ' + os.path.basename(f)
			shutil.copyfile(f, os.path.join(libdir, os.path.basename(f)))

