# encoding=utf-8
# Generated by cpy
# 2020-12-09 13:31:40.048927
import os, sys
from sys import stdin, stdout

#### start cpy import ###
from engine import CpyEngine
cpy = CpyEngine()
dstfile = cpy.compile('/home/jure/workspace/ssdb-saverio.git/tools/ssdb_cli/util.cpy', '', '/home/jure/workspace/ssdb-saverio.git/tools/_cpy_/ssdb_cli')
#### end cpy import ###
from util import *
fp = None
progress = 0
read_size = 0
total_size = 0

def write_line(params):
	pass
	gs = globals()

	_cpy_r_0 = _cpy_l_1 = params
	if type(_cpy_r_0).__name__ == 'dict': _cpy_b_3=True; _cpy_l_1=_cpy_r_0.iterkeys()
	else: _cpy_b_3=False;k=-1
	for _cpy_k_2 in _cpy_l_1:
		if _cpy_b_3: k=_cpy_k_2; v=_cpy_r_0[_cpy_k_2]
		else: k += 1; v=_cpy_k_2
		pass
		params[k] = str(v).encode('string-escape')
	line = (str('\t').join(params) + '\n')
	gs['read_size'] += len(line)
	gs['fp'].write(line)

def show_progress():
	pass
	gs = globals()
	progress = gs['progress']
	read_size = gs['read_size']
	total_size = gs['total_size']
	progress_2 = int(float(read_size) / total_size * 100)

	if ((progress_2 - progress)>=5 or read_size==total_size):
		pass
		gs['progress'] = progress_2
		sys.stdout.write("%2d%%\n" % (progress_2))

def my_readline(c):
	pass

	if c==None:
		pass
		c = ''
	try:
		pass
		return raw_input(c)
	except Exception , e:
		pass
	return ''

def run(link, args):
	pass
	gs = globals()
	kstart = ''
	kend = ''
	hstart = ''
	hend = ''
	zstart = ''
	zend = ''
	qstart = ''
	qend = ''
	output_file = False
	interactive = False

	_cpy_r_4 = _cpy_l_5 = args
	if type(_cpy_r_4).__name__ == 'dict': _cpy_b_7=True; _cpy_l_5=_cpy_r_4.iterkeys()
	else: _cpy_b_7=False;
	for _cpy_k_6 in _cpy_l_5:
		if _cpy_b_7: arg=_cpy_r_4[_cpy_k_6]
		else: arg=_cpy_k_6
		pass

		if arg=='-i':
			pass
			interactive = True
		else:
			pass
			output_file = arg

	if output_file==False:
		pass
		sys.stderr.write('Usage: export [-i] out_file\n')
		return 

	if os.path.exists(output_file):
		pass
		print (('Error: ' + output_file) + ' already exists!')
		return 

	if interactive:
		pass
		sys.stdout.write("input KV range[start, end]: \n")
		kstart = my_readline('  start(inclusive, default none): ')
		kend = my_readline('    end(inclusive, default none): ')
		sys.stdout.write("input HASH range: \n")
		hstart = my_readline('  start(inclusive, default none): ')
		hend = my_readline('    end(inclusive, default none): ')
		sys.stdout.write("input ZSET range: \n")
		zstart = my_readline('  start(inclusive, default none): ')
		zend = my_readline('    end(inclusive, default none): ')
		sys.stdout.write("input QUEUE range: \n")
		qstart = my_readline('  start(inclusive, default none): ')
		qend = my_readline('    end(inclusive, default none): ')
	gs['fp'] = open(output_file, 'w')
	gs = globals()
	gs['total_size'] = dbsize(link)

	if gs['total_size']<=0:
		pass
		gs['total_size'] = 1
	gs['total_size'] *= 1024 * 1024
	ls = SSDB_kv_scan(link)
	ls.set_range(kstart, kend)
	r = link.request('get', [ls.key])

	if r.ok():
		pass
		write_line(['set', ls.key, r.data])

	while ls.next():
		pass
		show_progress()
		write_line(['set', ls.key, ls.val])
	ls = SSDB_hash_list(link)
	ls.set_range(hstart, hend)
	scan = SSDB_hash_scan(link)
	scan.name = ls.key

	while scan.next():
		pass
		show_progress()
		write_line(['hset', ls.key, scan.key, scan.val])

	while ls.next():
		pass
		scan = SSDB_hash_scan(link)
		scan.name = ls.key

		while scan.next():
			pass
			show_progress()
			write_line(['hset', ls.key, scan.key, scan.val])
	ls = SSDB_zset_list(link)
	ls.set_range(zstart, zend)
	scan = SSDB_zset_scan(link)
	scan.name = ls.key

	while scan.next():
		pass
		show_progress()
		write_line(['zset', ls.key, scan.key, scan.val])

	while ls.next():
		pass
		scan = SSDB_zset_scan(link)
		scan.name = ls.key

		while scan.next():
			pass
			show_progress()
			write_line(['zset', ls.key, scan.key, scan.val])
	ls = SSDB_queue_list(link)
	ls.set_range(qstart, qend)
	scan = SSDB_queue_scan(link)
	scan.name = ls.key

	while scan.next():
		pass
		show_progress()
		write_line(['qpush', ls.key, scan.val])

	while ls.next():
		pass
		scan = SSDB_queue_scan(link)
		scan.name = ls.key

		while scan.next():
			pass
			show_progress()
			write_line(['qpush', ls.key, scan.val])

	if gs['fp']:
		pass
		gs['fp'].close()
	gs['read_size'] = gs['total_size']
	show_progress()
	print 'done.'
