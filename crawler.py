import  urllib2, re, os
def crawler(args):
	flags_short = ["-u", "-d", "-t"]
	url = ""
	to_path = ""
	ftype = ""
	page = ""	
	relative_links_regex = "(?<=href=\")[A-Za-z0-9_\.//-]+."
	absolute_links_regex = "http[s]?://(?:[a-zA-Z0-9]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-zA-Z][0-9a-zA-Z]))+."
	if len(args) > 1:
		arg_nr = 0 
		while arg_nr < len(args):
			if args[arg_nr] in flags_short:
				if len(args)-1 > arg_nr:
					if args[arg_nr] == "-u":
						url = args[arg_nr+1]
						arg_nr = arg_nr+1
					if args[arg_nr] == "-d":
						to_path = args[arg_nr+1]
						arg_nr = arg_nr+1
					if args[arg_nr] == "-t":
						ftype = args[arg_nr+1]
						arg_nr = arg_nr+1
				else:
					print "Too few arguments!"
					quit()
			else:
				print "Invalid argument!"
				print args[arg_nr]
			arg_nr=arg_nr+1
	else:
		print "Too few arguments!" 
		quit()
	
	try:
		request = urllib2.Request(url)
		response = urllib2.urlopen(request)
		page = response.read()
	except urllib2.URLError, exception:
		print exception
		quit()

	if not os.path.exists(to_path) and len(to_path)>0:
		os.makedirs(to_path)
	relative_links = parse_page(page, relative_links_regex+ftype)
	absolute_links = parse_page(page, absolute_links_regex+ftype)
	for link in relative_links:
		download_file(url + link, to_path)
	for link in absolute_links:
		download_file(link, to_path)	

def parse_page(page, regex):
	matches= []	
	for match in re.findall(regex, page):
		matches.append(match)
	return matches


def download_file( file_url, to_path):
	opener = urllib2.build_opener()
	try:
		fstream = opener.open(file_url)
		target = fstream.read()
		if os.path.exists(to_path) and len(to_path)>0:
 			os.makedirs(to_path)
		file_name = os.path.basename(file_url)
		file_name = to_path+file_name
		fout = open(file_name, "wb")
		fout.write(target)
		fout.close()
		return True
	except urllib2.URLError, exception:
		print exception
		return False 
