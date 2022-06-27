#!/bin/python3

import re
import os
import click

@click.command()
@click.argument("filename", nargs=1)
@click.option("-o", "--outdir", default=".",
	help="Output direectory (default current)")
@click.option("-r", "--auto-ref", is_flag=True, default=True, show_default=True,
	help="Use bad regex to remove reference section")
@click.option("-f", "--auto-fig", is_flag=True, default=True, show_default=True,
	help="Remove figure legends")
@click.option("-s", "--auto-sup", is_flag=True, default=True, show_default=True,
	help="Remove supplementary matertial")
def remove_patches(filename, outdir, auto_ref, auto_fig, auto_sup):
	"""Removes figure text that clumps in patches"""
	f = open(filename, "r")
	s = []
	l = []

	for line in f.readlines():
		s.append(line.strip())

	for i in s:
		l.append(len(i.split()))

	patch = []
	start = 0
	end = 0
	new = True
	for p, i in enumerate(l):
		if i < 5:
			if new == True:
				start = p
				end = p
				new = False
			if new == False:
				end = p
		else:
			if end-start > 3:
				patch.append((start,end))
			new = True
	
		for r in patch:
			for x in range(r[0], r[1]+1):
				s[x] = ""


	def combine_paras(s):
		"""Combine the paragraphs from seperated newlines"""
		c = ""
		for l in s:
				if l != "":
					c = c+l
					space = True
				if l == "" and space == True:
					c = c+"\n\n"
					space = False
		s = c.split("\n")
		
		for p, l in enumerate(s):
			if l.startswith("Article"):
				s[p] = l[-8:]

		return(s)
	

	def rm_refs(s, auto_sups, thresh=0):
		"""Poorly remove references"""
		#for i in s:
		#	if "✉ " in i:
		#		print(i)
		# ([A-Z][a-z]{1,}\d?[\s,\,]\s[A-Z])\.?
		# (([A-Z][a-z]{1,}\-)?[A-Z][a-z]{1,}\d?[\s,\,]{1,2}[A-Z]\.)
		ref = []
		for p, i in enumerate(s):
			# not safe
			ref.append((len(re.findall(r"(([A-Z][a-z]{1,}\-)?[A-Z][a-z]{1,}\d?[\s,\,]{1,2}[A-Z]\.)", i)), 
						len(re.findall(r"([A-Z][a-z]{1,}\d?[\s,\,]\s[A-Z])\.?", i))))
			#if ref[p] > 0:
			#	print(s[p], ref[p])
			if ref[p][0] == 0 and len(s[p]) == 0:
				ref[p] = (-1, -1)
		
		count = 0
		new = True
		likely = []
		start = 0
		end = -1
		for p, x in enumerate(ref):
			if sum(x) > 0 and new == True:
				start = p
				new = False
				count = 0
			if sum(x) > 0 and new == False:
				end = p
			if sum(x) == 0:
				count += 2
			if sum(x) < 0:
				count -= 1
			if count > 2:
				if end > start and new == False:
					likely.append((start, end))
				new = True
		#print(likely)
		j = []
		rmr = set()
		if auto_sups == True:
			limit = len(s)
			if len(likely) > 0:
				for l in likely:
					for z in range(l[0], l[1]+1):
						rmr.add(z)
					if l[1] - l[0] > 4:
						limit = l[0]
			for p, i in enumerate(ref):
				if i[0] <= thresh:
					if p not in rmr:
						j.append(s[p])
				if p > limit:
					#print("limit reached")
					return j
		if auto_sups == False:
			for l in likely:
				for z in range(l[0], l[1]+1):
					rmr.add(z)
			for p, i in enumerate(ref):
				if i[0] <= thresh:
					if p not in rmr:
						j.append(s[p])
		return j
				

	def rm_figs(s):
		"""Remove figure legends"""
		j = []
		rmr = set()
		for p, i in enumerate(s):
			# very poor, probably use regex
			if i.startswith("Fig."):
				rmr.add(p)
				continue
			if i.startswith("Supplementary"):
				rmr.add(p)
			if i.startswith("Extended Data Fig."):
				rmr.add(p)
		#print(rmr)
		#for i in rmr:
		#	print(s[i])
		for p, i in enumerate(s):
			if p not in rmr:
				j.append(i)
		return j

	
	def remove_strs(s):
		"""Remove string that makes harder to read"""
		for p, i in enumerate(s):
			# duplicates but very small files ¯\_(ツ)_/¯
			s[p] = re.sub(r"([\(,;]Extend.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]extend.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]Figure.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]Fig.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]fig.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]Reference.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]Ref.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]ref.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]Supplmentary.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]Supp.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]supp.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]Tabel.*?\))", "", i)
			s[p] = re.sub(r"([\(,;]table.*?\))", "", i)

			# simple email
			s[p] = re.sub(r"\S+@\S+\.\S+", "", i)
			# url
			s[p] = re.sub(r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})", "", i)
		return s

	def write_file(filename, outdir, s):
		"""Write filtered result to txt file"""
		out = os.path.basename(filename).split(".")[0]+"_filtered.txt"
		space = False
		with open(os.path.join(outdir, out), "w") as f:
			for l in s:
				if l != "":
					f.write(l)
					space = True
				if l == "" and space == True:
					f.write("\n\n")
					space = False
	
	s = combine_paras(s)
	if auto_ref == True:
		s = rm_refs(s, auto_sup)
	if auto_fig == True:
		s = rm_figs(s)
	s = remove_strs(s)
	outname = os.path.basename(filename).split(".")[0]+"_filtered.txt"
	write_file(filename, outdir, s)
	print(f"file {outname} written to {outdir}")

	#return s


if __name__ == "__main__":
	remove_patches()
