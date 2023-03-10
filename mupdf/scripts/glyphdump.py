#!/usr/bin/env python3

import sys

agl = []
aglseen = {}
single_from_name = []
multi_from_name = []
name_from_single = {}
code_from_multi = {}

print("/* This file was generated by scripts/glyphdump.py. Do not edit. */")
print()

def readlist(filename):
	f = open(filename, "r")
	for line in f.readlines():
		if line[0] == '#':
			continue
		line = line[:-1]
		name, alts = line.split(';')
		for list in alts.split(','):
			list = [int(x, 16) for x in list.split(' ')]
			okay = True
			for ucs in list:
				if ucs > 0xffff:
					okay = False
				#if ucs >= 0xe000 and ucs <= 0xf8ff:
				#	okay = False
			if okay and name not in aglseen:
				agl.append((name, list))
				aglseen[name] = True

readlist("scripts/glyphlist.txt")
readlist("scripts/texglyphlist.txt")

for name, ucslist in agl:
	num = len(ucslist)
	if num == 1:
		ucs = ucslist[0]
		single_from_name.append((name, ucs))
		if ucs not in name_from_single:
			name_from_single[ucs] = []
		name_from_single[ucs].append(name)
	else:
		multi_from_name.append((name, ucslist))

def dumplist(list):
	for item in list:
		sys.stdout.write(item)

single_from_name.sort()
singlenames = []
singlecodes = []
for name, ucs in single_from_name:
	singlenames.append("\"%s\",\n" % name)
	singlecodes.append("0x%04x,\n" % ucs)

multi_from_name.sort()
multinames = []
multioffsets = []
multicodes = []
for name, ucslist in multi_from_name:
	multinames.append("\"%s\",\n" % name)
	multioffsets.append("%d,\n" % len(multicodes))
	multicodes.append("%d," % len(ucslist))
	for ucs in ucslist:
		multicodes.append(" 0x%04x," % ucs)
	multicodes.append("\n");

keys = list(name_from_single.keys())
keys.sort()
dupoffsets = []
dupnames = []
for ucs in keys:
	list = name_from_single[ucs]
	if len(list) > 1:
		ofs = len(dupnames)
		dupoffsets.append("0x%04x, %d,\n" % (ucs, ofs))
		for name in list:
			dupnames.append("\"%s\", " % name)
		dupnames.append("0,\n")

print("static const char *single_name_list[] = {")
dumplist(singlenames)
print("};")
print()
print("static const unsigned short single_code_list[] = {")
dumplist(singlecodes)
print("};")
print()
if False:
	print("static const char *multi_name_list[] = {")
	dumplist(multinames)
	print("};")
	print()
	print("static const unsigned short multi_offset_list[] = {")
	dumplist(multioffsets)
	print("};")
	print()
	print("static const unsigned short multi_code_list[] = {")
	dumplist(multicodes)
	print("};")
	print()
print("static const unsigned short agl_dup_offsets[] = {")
dumplist(dupoffsets)
print("};")
print()
print("static const char *agl_dup_names[] = {")
dumplist(dupnames)
print("};")
