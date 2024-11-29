#!/usr/bin/python3


#1.get protein sequence from NCBI
#2.do alignment
#3.set a threshold for similarity of the sequence
#4.use relatively similar sequences to generate a conservation plot



import os
import subprocess

#1.define a function to get protein from NCBI, user should specify protein family and taxonomic group
#should be interactive, but the user may input wrong things...

def get_pro():
	pro_family=input("Please enter the protein family:")
	tax_group=input("Please enter the taxonomic group:")
	output_seq="pro_seq.fasta"
#do the esearch&efetch commands in bash, use try to check first
	try:
		esearch=f"esearch -db protein -query \"{pro_family}[Protein Name] AND {tax_group}[Organism]\""
		efetch=f"efetch -format fasta"
#it's strange that I can't use pipe to connect esearch and efetch like this:
#"esearch -db protein -query \"{pro_family}[Protein Name] AND {tax_group}[Organism]\ | efetch -format fasta"
#and I can't use subprocess to run esearch first and use it again to run efetch? :(
		combine=f"{esearch}|{efetch}"
		with open(output_seq, "w") as file:
			subprocess.run(combine, shell=True, check=True, stdout=file)
			print(f"protein sequence has been saved to {output_seq}")
	except subprocess.CalledProcessError as e:
		print("Error occured when getting the sequence \n did you correctly enter the protein family and taxonomic group? \n it may also because the NCBI didn't work", e)

get_pro()
#Run the function to let user get sequence. User can enter the protein family and taxonomic group and the fetched sequences will be stored in a file called pro_seq.fasta
#We can use "cat" to see the content of protein sequence we got in the 1st step now.
"""print("Let's have a brief look of the sequence we've got")
subprocess.run("head pro_seq.fasta", shell=True)"""
#just want to let the user have a brief idea of what they got. But there were some error when I added these two lines.


#2.Do multiple sequence alignment
def multi_seq_align():
	input_file=input("You've got a set of protein sequences. \nPlease enter the name of it so we can do the alignment: ")
	#I can also directly let "input=pro_seq.fasta"......So the user can stop here to decide whether to continue using precious sequence.
	output_file="aligned_pro_seq.fasta"
	try:
		clustalo=f"clustalo -i {input_file} -o {output_file} --wrap=80 --force"
		subprocess.run(clustalo,shell=True,check=True)
		#write a command in bash to do multiple sequence alignment, "--wrap=80"makes each line of the output file no longer than 80.
		#add a "--force" here to cover old file with a new one
		print(f"Results of alignment were saved in {output_file}")
	except subprocess.CalledProcessError as e:
		print("Error occured when doing alignment", e)

multi_seq_align()
"""print("Here are the first 10 lines of the aligned sequences.")
subprocess.run("head pro_seq_aligned", shell=True)"""


#3.Now that we've got the aligned sequences. User should be able to decide the degree of similarity.
#Make a fuction for user to set a threshold. Only sequence with higher degree of similarity can be passed to the following plot drawing part.
def similar_seq():
	input_file=input("Please enter the name of an aligned protein sequence file (aligned_pro_seq.fasta): ")
	threshold=float(input("Please enter the similarity threshold (a number from 0 to 100): "))
	output_file="similar_aligned_pro_seq.fasta"
	try:
		infoalign=f"infoalign -sequence {input_file} -outfile seq_similarity.txt"
		subprocess.run(infoalign, shell=True, check=True)
		#use a tool called "infoalign" in EMBOSS in bash to calculate the similarity of sequences
		selected_seqs=[]
                #create an empty list to store selected sequencses
		with open("seq_similarity.txt", "r") as file:
			lines=file.readlines()
			#get every lines of the file, should contain the sequences or their similarity degree(called identity)
			for line in lines:
				if "Sequence:" in line:
					seq_name=line.split(":")[1].strip()
					#if the line contains a sequence name, split it by ":", remove the first part "the name: Sequence" and hopefully get the second(the protein name and its sequence?).
				elif "Identity:" in line:
					identity=float(line.split(":")[1].replace("%","").strip())
					#if the line contains the degree of similarity, remove the name and %, only extract the number
					if identity >= threshold:
						selected_seqs.append(seq_name)
						#in every loop, if the degree of similarity is higher than the threshold, store the name of it
						#store the selected names of sequences in the list
		with open(input_file,"r") as f, open(output_file,"w") as out_f:
			write_seq=False
			for line in f:
				if line.startswith(">"):
					seq_id = line[1:].strip()
					write_seq = seq_id in selected_seqs
				if write_seq:
					out_f.write(line)
			print(f"Filtered sequences saved to {output_file}")
	except subprocess.CalledProcessError as e:
		print(f"Error occured during similarity filtering", e)


similar_seq()
#Now the selected similar sequences are stored in a list called "selected_seqs"

#I think it's strange to set both degree of similarty threshold and the number of sequences we want to use to generate the plot?
#If I set a threshold for the number of sequences I want to use, I may not use all of the sequences with higher degree of similarity than the "similarity threshold"?
#4.We can use it to generate the conservation plot
def conservation_plot():
	selected_seqs=input("if you want to continue, please enter \"similar_aligned_pro_seq.fasta\" here: ")
	output_file="conservation_plot.png"

	try:
		plotcon = f"plotcon -sequence {selected_seqs} -graph png -gtitle \"Conservation Plot\""
		subprocess.run(plotcon, shell=True, check=True)
		print(f"Successfully created {conservation_plot.png}")
	except subprocess.CalledProcessError as e:
		print(f"Error occurred when generating the conservation plot:", e)

conservation_plot()

















