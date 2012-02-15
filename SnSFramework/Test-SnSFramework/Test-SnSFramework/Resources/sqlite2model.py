import re
import sys
import getopt
import datetime
import getpass
import subprocess
import json


GLOBAL_OPTIONS 	= {}	#Keys should include: file, table, force, json, sql
GLOBAL_COLORS	= {}


##########################################################
# 	CAPITALIZE FIRST LETTER ONLY
##########################################################
def capitalize_first_only(string):
	return (str.capitalize(string[0])+string[1:])
##########################################################
# 	OPTIONS
##########################################################
def parse_options():
	global GLOBAL_OPTIONS
	
	# Setup
	GLOBAL_OPTIONS['output'] = '.'
	GLOBAL_OPTIONS['parent'] = False
	
	# Read arguments
	args = sys.argv[1:]
	opts, extraparams = getopt.getopt(args, 'o:t:p:i:fjsu', ['parent','output=', 'table=', 'project=', 'id=', 'force', 'json', 'sql', 'underscore'])
	for o,p in opts:
		if o == '--table' or o == '-t':
			GLOBAL_OPTIONS['table'] = p
		if o == '--force' or o == '-f':
			GLOBAL_OPTIONS['force'] = True
		if o == '--json' or o == '-j':
			GLOBAL_OPTIONS['json'] = True
		if o == '--sql' or o == '-s':
			GLOBAL_OPTIONS['sql'] = True
		if o == '--underscore' or o == '-u':
			GLOBAL_OPTIONS['underscore'] = True
		if o == '--project' or o == '-p':
			GLOBAL_OPTIONS['project'] = p
		if o == '--id' or o == '-i':
			GLOBAL_OPTIONS['id'] = p
		if o == '--output' or o == '-o':
			GLOBAL_OPTIONS['output'] = p
		if o == '--parent':
			GLOBAL_OPTIONS['parent'] = True
	
	if 'sql' in GLOBAL_OPTIONS and 'id' not in GLOBAL_OPTIONS:
		print_error("SQL option provided with no id (primary key)")
		print_usage()
		sys.exit(1)
				
	if 'project' not in GLOBAL_OPTIONS:
		print_error("Missing project name")
		print_usage()
		sys.exit(1)
		
	if len (extraparams) > 0:
		GLOBAL_OPTIONS['file'] = extraparams[0]
	else:
		print_error("Missing database model file name")
		print_usage()
		sys.exit(1)
		
##########################################################
# 	USAGE
##########################################################
def print_usage():
	print GLOBAL_COLORS['light-cyan']
	print """Usage:
	Parses the file passed in parameter (which should have a SQLite database format)
	and for all the tables found, create the header and implementation files.
	ex:  python sqlite2model.py  -js -p Test model.sql
	Mendatory parameters:
	-p --project      [project]      The project linked to 
	                  [filename]     The path for the database model
	Additional parameters:
	-i --id           [id]           The main id used for all tables
	                                 This is especially useful to have all BOs inehit from a master one
	   --parent                      Goes along with the id option and creates the parent files with 'id' attribute
	-t --table        [tablename]    Only the table mentioned (tablename) will be parsed
	-o --output       [folder]       The path for the output files
	-f --force                       Force the file, if already existing, to be overwritten 
	-s --sql                         Adds SQLite init method from a sqlite3statement.
	                                 Note that if you specify the sql option then the id paremeter becomes mendatory
	-j --json                        Adds JSON init methods from a NSDictionary holding JSON
	-u --underscore                  The class attributes will be preceded by a '_' character
	                                 This will result in for ex: @synthesize propertyA = _propertyA;"""
	print GLOBAL_COLORS['reset']

##########################################################
# 	PROCESS COMMENT
##########################################################
def comment(text,tabs=0):
	cmt = ''
	for i in range(0,tabs):
		cmt = "\t" + cmt
	cmt = "%s/****** %s ******/\n" % (cmt,text)
	return cmt

##########################################################
# 	PROCESS PRAGMA
##########################################################	
def pragma(text):
	prg = '#pragma mark - %s\n\n' % text
	return prg
	
##########################################################
# 	HEADER COMMENTS 
##########################################################
def comments_file(f):
	user  = subprocess.Popen(["finger", getpass.getuser()], stdout=subprocess.PIPE).communicate()[0]
	user = re.search(r'Name:\s*(.*)',user).group(1)
	return'''//
//  %s
//	%s
//
// 	This file was generated by %s
//
//  Created by %s on %s.
//  Copyright %s Smart&Soft. All rights reserved.
//
''' % (f.name, GLOBAL_OPTIONS['project'], __file__, user, datetime.date.today(), datetime.date.today().year )

##########################################################
# 	SETUP OUTPUT COLORS
##########################################################
def setup_colors():
	global GLOBAL_COLORS
	
	GLOBAL_COLORS['red'] 	= '\033[91m'
	GLOBAL_COLORS['green'] 	= '\033[92m'
	GLOBAL_COLORS['yellow'] = '\033[93m'
	GLOBAL_COLORS['blue'] 	= '\033[94m'
	GLOBAL_COLORS['pink'] 	= '\033[95m'
	GLOBAL_COLORS['cyan'] 	= '\033[96m'
	GLOBAL_COLORS['white'] 	= '\033[98m'
	

	GLOBAL_COLORS['light-red'] 		= '\033[31m'
	GLOBAL_COLORS['light-green'] 	= '\033[32m'
	GLOBAL_COLORS['light-yellow'] 	= '\033[33m'
	GLOBAL_COLORS['light-blue'] 	= '\033[34m'
	GLOBAL_COLORS['light-pink'] 	= '\033[35m'
	GLOBAL_COLORS['light-cyan'] 	= '\033[36m'
	GLOBAL_COLORS['light-white']	= '\033[38m'
	
	GLOBAL_COLORS['reset']	 = '\033[0m'
	
def print_error(error):
	print GLOBAL_COLORS['light-red'] + str(error) + GLOBAL_COLORS['reset']

def print_ok(text):
	sep = '\n**************************************\n'
	print GLOBAL_COLORS['light-green'] + sep + str(text) + sep + GLOBAL_COLORS['reset']
##########################################################
# 	TEST STRINGS
##########################################################
def is_string(key):
	return re.match(r'varchar|text', key, re.IGNORECASE)
def is_date(key):
	return re.match(r'date', key, re.IGNORECASE)
def is_bool(key):
	return re.match(r'bool', key, re.IGNORECASE)
def is_integer(key):
	return re.match(r'integer', key, re.IGNORECASE)
def is_object(key):
	return is_date(key) or is_string(key)

def is_parent(table):
	return GLOBAL_OPTIONS['parent']	and table == GLOBAL_OPTIONS['project']
##########################################################
# 	INTERFACE
##########################################################
def header(file, table, attributes):
	
	underscore = ''
	if 'underscore' in GLOBAL_OPTIONS:
		underscore = '_'
		
	comments = comments_file(file)
	json = process_json_header(table, attributes)
	sql  = process_sql_header(table, attributes)	
	
	properties = comment("Properties")
	init = ''
	
	includes = ''
	includes += ('\n#import "%s.h"\n' % GLOBAL_OPTIONS['project']) if not is_parent(table) and GLOBAL_OPTIONS['parent'] else ''
	
	protocols = '<SQLiteStorable>' if 'sql' in GLOBAL_OPTIONS else ''
	##########################################################
	# 	Interface
	interface = "@interface %s : %s %s\n{\n" %  (table,GLOBAL_OPTIONS['project'] if GLOBAL_OPTIONS['parent'] and not is_parent(table) else 'NSObject', protocols)
	init = '\n- (id)initWith'
	for k in attributes:
		for v in attributes[k]:
			properties = properties + '@property (nonatomic'
			if is_bool(k):
				interface += '\tBOOL\t'
				properties = properties + ') BOOL '
				init += '%s:(Boolean)i%s' % (v, capitalize_first_only(v))
			elif is_integer(k):
				interface += '\tNSInteger '
				properties = properties + ') NSInteger '
				init += '%s:(NSInteger)i%s' % (v, capitalize_first_only(v))
			elif is_string(k):
				interface = interface + '\tNSString*\t'
				properties = properties + ', retain) NSString* '
				init += '%s:(NSString*)i%s' % (v, capitalize_first_only(v))
			elif is_date(k):
				interface = interface + '\tNSDate*\t'
				properties = properties + ', retain) NSDate* '
				init += '%s:(NSDate*)i%s' % (v, capitalize_first_only(v))
			else:
				print_error('Unknown data type: %s' % k)
				sys.exit(1)
				
			interface += underscore + v + ";\n"
			properties = properties + v + ";\n"
			init += ' '
			
	init += ';\n'
	interface += "}\n\n"
	
	end = "\n\n@end\n"
		
	file.writelines([comments,includes,json['pre-interface'],sql['pre-interface'],interface,properties,init,json['interface'],sql['interface'],end])
	
	return
	
##########################################################
# 	IMPLENTATION
##########################################################
def implementation(file, table, attributes):
	
	underscore = ''
	if 'underscore' in GLOBAL_OPTIONS:
		underscore = '_'
	
	comments = comments_file(file)
	includes = '\n#import "%s.h"\n' % table
	impl = "\n@implementation %s\n\n" % table
	
	##########################################################
	# 	synthesize
	synth = ''
	for k in attributes:
		for v in attributes[k]:
			synth += "@synthesize " + v + " = " + underscore + v + ";\n"
	synth += '\n'
	##########################################################
	# 	init	
	init = pragma('Init Methods')
	init += '- (id)initWith'
	objects = ''
	for k in attributes:
		for v in attributes[k]:
			if is_bool(k):
				init += '%s:(Boolean)i%s' % (v, capitalize_first_only(v))
				objects += '\t\t%s = i%s' % (v, capitalize_first_only(v))
			elif is_integer(k):
				init += '%s:(NSInteger)i%s' % (v, capitalize_first_only(v))
				objects += '\t\t%s = i%s' % (v, capitalize_first_only(v))
			elif is_string(k):
				init += '%s:(NSString*)i%s' % (v, capitalize_first_only(v))
				objects += '\t\t%s = [i%s retain]' % (v, capitalize_first_only(v))
			elif is_date(k):
				init += '%s:(NSDate*)i%s' % (v, capitalize_first_only(v))
				objects += '\t\t%s = [i%s retain]' % (v, capitalize_first_only(v))
			else:
				print_error('Unknown data type: %s' % k)
				sys.exit(1)
			init += ' '
			objects += ';\n'
				
	init += '\n{\n'
	init += '\tif (self = [super init])\n\t{\n%s' % objects
	init += '\t}\n\treturn self;\n}\n'
	


	##########################################################
	# 	dealloc
	dealloc = '- (void)dealloc\n{\n'
	for k in attributes:
		for v in attributes[k]:
			val = ''
			if is_object(k):
				val += '\t[%s%s release];\n' % (underscore,v)
				dealloc += val
	dealloc += '\n\t[super dealloc];\n}\n'
	
	json = process_json_implementation(table, attributes)
	sql = process_sql_implementation(table, attributes)
	
	##########################################################
	# 	description
	description = '- (NSString*)description\n{\n'
	format = ''
	elts = []
	for k in attributes:
		for v in attributes[k]:
			format+="-%@- "
			if is_object(k):
				elts.append('[NSString stringWithFormat:@"%s: %%@", self.%s]' % (v, v)) 
			else:
				elts.append('[NSString stringWithFormat:@"%s: %%d", self.%s]' % (v, v)) 
				
	description += '\treturn [NSString stringWithFormat:@"%%@: %s", self.class, \n\t\t%s];' % (format,',\n\t\t'.join(elts))
	description += '\n}\n'
	end = "\n\n@end\n"
	file.writelines([comments,includes,impl,synth,init,dealloc,description,sql,json,end])
		
	return
	
##########################################################
# 	PROCESS TABLE
##########################################################
def process_table(table, attributes):
	
	output = '%s/%s' % (GLOBAL_OPTIONS['output'],table)
	fileH = open(output+'.h', 'w')
	fileM = open(output+'.m', 'w')	
	
	print "Processing table: %s" % table
	#print(json.dumps (attributes, indent=4))
	
	header(fileH, table, attributes)
	implementation(fileM, table,  attributes)

	fileH.close()
	fileM.close()
	
##########################################################
# 	SQL
##########################################################
def process_sql_header(table, attributes):
	
	ret = {'pre-interface':'','interface': ''}
	if 'sql' not in GLOBAL_OPTIONS:
		return ret
		
	cmt = "\n" +  comment ('SQLite')
	includes = cmt + '\n#import <sqlite3.h>\n'
	
	defines = ''
	
	##########################################################
	# 	Print Column
	val = 0
	for k in attributes:
		for v in attributes[k]:
			defines = defines + '#define k%s%sColumn %d\n' % (table, capitalize_first_only(v), val)
			val += 1
	defines = defines + "\n"
	
	##########################################################
	# 	Print ColumnName
	for k in attributes:
		for v in attributes[k]:
			defines += '#define k%s%sColumnName @"%s"\n' % (table, capitalize_first_only(v), v)
			#defines = defines + '#define k'+str.capitalize(v)+'ColumnName'+"\t@"+'"'+v+'"'+"\n"
	defines += "\n"
	
	##########################################################
	# 	SQL
	sql = cmt + '- (id)initWithSQLiteStatement:(sqlite3_stmt*)iStatement;\n'
	sql += '- (NSString*) sqlID;\n' if not GLOBAL_OPTIONS['parent'] or is_parent(table) else ''
	sql += '+ (NSString*) sqlColumnNameID;\n' if not GLOBAL_OPTIONS['parent'] or is_parent(table) else ''
	
	ret = {'pre-interface':includes + defines,'interface': sql}
	return ret
	
def process_sql_implementation(table, attributes):
	if 'sql' not in GLOBAL_OPTIONS:
		return ""
		
	underscore = ''
	if 'underscore' in GLOBAL_OPTIONS:
		underscore = '_'
			
	
	sql = "\n" +  pragma ('SQLite Init Methods')

	##########################################################
	# 	SQL
	sql += '- (id)initWithSQLiteStatement:(sqlite3_stmt*)iStatement\n' 
	sql += '{\n\tif (self = [super init%s])\n\t{\n'  % ('WithSQLiteStatement:iStatement' if not is_parent(table) and GLOBAL_OPTIONS['parent'] else '')
	
	columns = []
	
	insert_format = []
	insert_values = []
	
	update_format = []
	update_values = []
	for k in attributes:
		for v in attributes[k]:
			val = ''
			columns.append('@"%s"' % v)
			update_values.append('@"%s", %s' % (v,v))
			if is_bool(k) or is_integer(k):
				val = 'sqlite3_column_int(iStatement, k%s%sColumn);\n' % (table,capitalize_first_only(v))
				insert_format.append('%u')
				insert_values.append(v)
				update_format.append('%@ = %u')
			elif is_string(k):
				val = '[[NSString alloc] initWithSQLiteStatement:iStatement column:k%s%sColumn];\n' % (table,str.capitalize(v))
				insert_format.append("'%@'")
				insert_values.append('[%s stringByEscapingSingleQuotesForSQLite]' % v)
				update_format.append("%@ = '%@'")
			elif is_date(k):
				val = '[[NSDate alloc] initWithSQLiteStatement:iStatement fn:k%s%sColumn];\n' % (table,str.capitalize(v))
				insert_format.append("'%@'")
				insert_values.append(v)
				update_format.append("%@ = '%@'")
			else:
				print_error('Unhandled data type [%s] for SQL' % k)
				sys.exit(1)
			sql += '\t\t%s%s = %s' % (underscore, v, val)
	sql += '\t}\n\n'
	sql += '\treturn self;\n}\n'
	
	##########################################################
	# 	SQLite Storable
	storable = '\n' + pragma('SQLiteStorable')
	array = '[[super class] columnsForSQL]' if not is_parent(table) and GLOBAL_OPTIONS['parent'] else '[NSArray array]'
	
	##########################################################
	# 	sqlColumnNameID and sqlID
	if 'id' in GLOBAL_OPTIONS:
		storable+='''+ (NSString*)sqlColumnNameID
{
	return @"%s";
}

- (NSString*)sqlID
{
	return [NSString stringWithFormat:@"%%d", %s];
}	
''' % (GLOBAL_OPTIONS['id'], GLOBAL_OPTIONS['id']) if not GLOBAL_OPTIONS['parent'] or is_parent(table) else ''
 
	##########################################################
	# 	columnsForSQL
	storable+='''+ (NSArray*)columnsForSQL
{
    // Retreive main object ID
    NSMutableArray* aArray = [NSMutableArray arrayWithArray:%s];

    // Add necessary columns
    [aArray addObjectsFromArray:[NSArray arrayWithObjects:%s, nil]];

    return aArray;
}
''' % (array,', '.join(columns))

	##########################################################
	# 	sqlValuesForInsert
	storable+='''
-(NSString*)sqlValuesForInsert
{
    NSString* aValues = @"";
    
    aValues = [NSString stringWithFormat:@"%s",
               \t%s];
    
    return aValues;
}
''' % (', '.join(insert_format), ',\n\t\t\t\t'.join(insert_values))

######	####################################################
	# 	sqlValuesForUpdate
	storable+='''
- (NSString*)sqlValuesForUpdate
{
	NSString* aValues = @"";
    
    aValues = [NSString stringWithFormat:@"%s", 
               \t%s];
    
    return aValues;
    
}
''' % (', '.join(update_format), ',\n\t\t\t\t'.join(update_values))

	return sql + storable
	

##########################################################
# 	JSON
##########################################################
def process_json_header(table, attributes):
	ret = {'pre-interface':'','interface':''}
	if 'json' not in GLOBAL_OPTIONS:
		return ret
		
	cmt = "\n" +  comment ('JSON')
	defines = cmt
	methods = ''
	
	# 	Keys
	for k in attributes:
		for v in attributes[k]:
			defines += '#define k%s%sKey "%s"\n' % (table,capitalize_first_only(v),v)
	defines += '\n'
	# 	Methods
	methods += cmt + '- (id)initWithJSONDictionary:(NSDictionary*)iDictionary;\n'
	
	ret =  {'pre-interface':defines,'interface':methods}
	return ret
def process_json_implementation(table, attributes):
	
	if 'json' not in GLOBAL_OPTIONS:
		return ""
		
	underscore = ''
	if 'underscore' in GLOBAL_OPTIONS:
		underscore = '_'
		
	json = "\n" +  pragma ('JSON Methods')
	
	##########################################################
	# 	Dictionary
	json += '- (id)initWithJSONDictionary:(NSDictionary*)iDictionary\n'
	json += '{\n\tif (self = [super init%s])\n\t{\n' % ('WithJSONDictionary:iDictionary' if not is_parent(table) and GLOBAL_OPTIONS['parent'] else '')
	for k in attributes:
		for v in attributes[k]:
			val = ''
			if is_bool(k) or is_integer(k):
				val = '[NSString integerFromDictionary:iDictionary key:k%s%sKey];\n' % (table,capitalize_first_only(v))
			elif is_string(k):
				val = '[[NSString alloc] initWithDictionary:iDictionary key:k%s%sKey];\n' % (table,capitalize_first_only(v))
			elif is_date(k):
				val = '[[NSDate alloc] initWithDictionary:iDictionary key:k%s%sKey];\n' % (table,capitalize_first_only(v))
			else:
				print_error('Unhandled data type [%s] for JSON' % k)
				sys.exit(1)
			json  += '\t\t%s%s = %s' % (underscore, v, val)
	json  += '\t}\n\n'
	json  += '\treturn self;\n}\n'

	return json
	
##########################################################
# 	UTILS
##########################################################
def file_content(filename):
	try:
		handler = open(GLOBAL_OPTIONS['file'], 'r')
		content =  handler.read()
		handler.close()
	except Exception as ex:
		print_error("Failed to read file: %s" % filename )
		print_error(ex)
		sys.exit(1)
	
	return content
##########################################################
# 	MAIN
##########################################################
def __main__():
	# Let's create a file and write it to disk.
	setup_colors()
	parse_options()
	
	content = file_content(GLOBAL_OPTIONS['file'])
	
	##########################################################
	# Special treatment for the project if the common id is given
	if GLOBAL_OPTIONS['parent'] and 'id' in GLOBAL_OPTIONS:
		process_table(GLOBAL_OPTIONS['project'], {'INTEGER' : [GLOBAL_OPTIONS['id']]})
	
	for MTable in re.finditer(r'create table\s*(\w+)\(([^;]+)\);', content, re.IGNORECASE|re.MULTILINE):
		
		attributes = {}
		table =  MTable.group(1)

		MContent  = re.findall(r'(\w+)\s+([a-z]+)[^,]+,', MTable.group(2), re.IGNORECASE)
		print_error(MContent)	
		
		for m in MContent:
			if m[1] not in attributes:
				attributes[m[1]] = []
			if not GLOBAL_OPTIONS['parent'] or 'id' in GLOBAL_OPTIONS and GLOBAL_OPTIONS['id'] != m[0]:
				attributes[m[1]].append(m[0])
			
			
		process_table(table, attributes)
		
	print_ok ('Model %s succesfully converted' % GLOBAL_OPTIONS['file'])
	
# run
__main__()

