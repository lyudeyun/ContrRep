import sys
# path
addpath = []
# dataset for simulation
is_nor = ''
dataset_run = ''
# dataset
dataset_tbr = []
D_size = ''
# model parameters
bench = ''
model = ''
model_cp = ''
parameters = []
# io parameters
in_name = []
in_range = []
in_span = []
icc_name = []
ic_const = []
ics_name = []
oc_name = []
oc_span = []
# nn parameters
nn = ''
nn_stru = ''
# specification
phi_str = []
# mutation parameters
mut_mode = ''
bound_mode = ''
bug_lb = ''
bug_ub = ''
dist_mode = ''
K = ''
bcr = ''
cand_mode = ''
mut_op_mode_list = []
mut_op_noise_list = []
noise_rep_num = ''
date = ''
trial = ''
mut_file = ''
# repair parameters
sel_flag = ''
ts_size = ''
ts_mode = ''
# script parameters
status = 0
arg = ''
linenum = 0

with open(sys.argv[1],'r') as conf:
	for line in conf.readlines():
		argu = line.strip().split()
		if status == 0:
			status = 1
			arg = argu[0]
			linenum = int(argu[1])
		elif status == 1:
			linenum = linenum - 1
			if arg == 'addpath':
				addpath.append(argu[0])
			elif arg == 'dataset_run':
				dataset_run = argu[0]
			elif arg == 'dataset_tbr':
				dataset_tbr.append(argu[0])
			elif arg == 'D_size':
				D_size = argu[0]
			elif arg == 'is_nor':
				is_nor = argu[0]
			elif arg == 'bench':
				bench = argu[0]
			elif arg == 'model':
				model = argu[0]
			elif arg == 'model_cp':
				model_cp = argu[0]
			elif arg == 'parameters':
				parameters.append(argu[0])
			elif arg == 'in_name':
				in_name.append(argu[0])
			elif arg == 'in_range':
				in_range.append([float(argu[0]),float(argu[1])])
			elif arg == 'in_span':
				# print(len(argu))
				in_span = '{'
				for idx in range(len(argu)-1):
					in_span = in_span + argu[idx]+','
					# print(argu[idx])
				in_span = in_span + argu[len(argu)-1] + '}'
			elif arg == 'icc_name':
				icc_name.append(argu[0])
			elif arg == 'ic_const':
				ic_const.append(argu[0])
			elif arg == 'ics_name':
				ics_name.append(argu[0])
			elif arg == 'oc_name':
				oc_name.append(argu[0])
			elif arg == 'oc_span':
				# print(len(argu))
				oc_span = '{'
				for idx in range(len(argu)-1):
					oc_span = oc_span + argu[idx] + ','
					# print(argu[idx])
				oc_span = oc_span + argu[len(argu)-1] + '}'
			elif arg == 'nn':
				nn = argu[0]
			elif arg == 'nn_stru':
				nn_stru = argu[0]
			elif arg == 'phi_str':
				complete_phi = argu[0] + ';' + argu[1]
				for a in argu[2:]:
					complete_phi = complete_phi + ' ' + a
				phi_str.append(complete_phi)
			elif arg == 'mut_mode':
				mut_mode = argu[0]
			elif arg == 'bound_mode':
				bound_mode = argu[0]
			elif arg == 'bug_lb':
				bug_lb = argu[0]
			elif arg == 'bug_ub':
				bug_ub = argu[0]
			elif arg == 'dist_mode':
				dist_mode = argu[0]
			elif arg == 'bcr':
				bcr = argu[0]
			elif arg == 'K':
				K = argu[0]
			elif arg == 'cand_mode':
				cand_mode = argu[0]
			elif arg == 'mut_op_mode':
				mut_op_mode_list.append(argu[0])
			elif arg == 'mut_op_noise':
				mut_op_noise_list.append(argu[0])
			elif arg == 'noise_rep_num':
				noise_rep_num = argu[0]
			elif arg == 'date':
				date = argu[0]
			elif arg == 'trial':
				trial = argu[0]
			elif arg == 'sel_flag':
				sel_flag = argu[0]
			elif arg == 'ts_size':
				ts_size = argu[0]
			elif arg == 'ts_mode':
				ts_mode = argu[0]
			else:
				continue
			if linenum == 0:
				status = 0

# script name 
for phi_i in range(len(phi_str)):
		ds = dataset_tbr[phi_i]
		property = phi_str[phi_i].split(';')
		filename = model + '_spec_' + str(phi_i + 1) + '_selflag_' + sel_flag + '_mutmode_' + mut_mode + '_boundmode_' + bound_mode + '_distmode_' + dist_mode + '_K_' + K + '_candmode_' + cand_mode + '_tssize_' + ts_size + '_tsmode_' + ts_mode + '_bcr_' + bcr + '_trial_' + trial + '_Date_' + date + '_BugInjection'
		print(filename)
		logname = '\'./output/' + filename + '.log\''
		param = '\n'.join(parameters)
		with open('scripts/'+filename,'w') as bm:
			bm.write('#!/bin/sh\n')
			bm.write('matlab -nodesktop -nosplash <<EOF\n')
			bm.write('clear;\n')
			bm.write('close all;\n')
			bm.write('clc;\n')
			bm.write('bdclose(\'all\');\n')
			# addpath
			for ap in addpath:
				bm.write('addpath(genpath(\'' + ap + '\'));\n')
			# load dataset for simulation 
			bm.write('dataset_run = \'' + dataset_run + '\';\n')
			bm.write('if strcmp(dataset_run, \'Null.mat\')\n')
			bm.write('\t D_run = \'\';\n')
			bm.write('else\n')
			bm.write('\t D_run = load(dataset_run);\n')
			bm.write('end\n')
			# load dataset
			if ds != '':
				bm.write('D = load(\'' + ds + '\');\n')
			bm.write('D_size = ' + D_size + ';\n')
			# model parameters info
			bm.write('bm = \'' + bench + '\';\n')
			bm.write('mdl = \''+ model + '\';\n')
			bm.write('mdl_cp = \''+ model_cp + '\';\n')
			bm.write(param + '\n')

			bm.write('is_nor = ' + is_nor + ';\n')
			bm.write('if is_nor == 1\n')
			bm.write('\tx_gain = D_run.ps_x.gain;\n')
			bm.write('\tx_gain = diag(x_gain);\n')
			bm.write('\tx_offset = D_run.ps_x.xoffset;\n')
			bm.write('\ty_gain = D_run.ps_y.gain;\n')
			bm.write('\ty_offset = D_run.ps_y.xoffset;\n')
			bm.write('end\n')

			# io parameters
			bm.write('in_name = {\'' + in_name[0] + '\'')
			for inname in in_name[1:]:
				bm.write(',')
				bm.write('\'' + inname + '\'')
			bm.write('};\n')

			bm.write('in_range = {[' + str(in_range[0][0]) + ' ' + str(in_range[0][1]) + ']')
			for ir in in_range[1:]:
				bm.write(',[' + str(ir[0]) + ' ' + str(ir[1]) + ']')
			bm.write('};\n')
			
			bm.write('in_span = ' + in_span + ';\n')

			if icc_name == []:
				bm.write('icc_name = {};\n')
			else:
				bm.write('icc_name = {\'' + icc_name[0] + '\'')
				for iccname in icc_name[1:]:
					bm.write(',')
					bm.write('\'' + iccname + '\'')
				bm.write('};\n')
				
			if ic_const == []:
				bm.write('ic_const = {};\n')
			else:
				bm.write('ic_const = {' + ic_const[0])
				for iccon in ic_const[1:]:
					bm.write(',')
					bm.write('' + iccon)
				bm.write('};\n')

			bm.write('ics_name = {\'' + ics_name[0] + '\'')
			for icsname in ics_name[1:]:
				bm.write(',')
				bm.write('\'' + icsname + '\'')
			bm.write('};\n')

			bm.write('oc_name = {\'' + oc_name[0] + '\'')
			for ocname in oc_name[1:]:
				bm.write(',')
				bm.write('\'' + ocname + '\'')
			bm.write('};\n')

			bm.write('oc_span = ' + oc_span + ';\n')

			# nn parameters
			bm.write('nn = load(\'' + nn + '\');\n')
			bm.write('net = nn.net;\n')
			bm.write('nn_stru = ' + nn_stru + ';\n')

			# specification
			bm.write('phi_str = \'' + property[1] + '\';\n')
			bm.write('spec_i = ' + str(phi_i + 1) + ';\n')

			# mutation parameters
			bm.write('mut_conf.mut_mode = \'' + mut_mode + '\';\n')
			bm.write('mut_conf.bound_mode = \'' + bound_mode + '\';\n')
			bm.write('mut_conf.bug_lb = ' + bug_lb + ';\n')
			bm.write('mut_conf.bug_ub = ' + bug_ub + ';\n')
			bm.write('mut_conf.dist_mode = \'' + dist_mode + '\';\n')
			bm.write('mut_conf.K = ' + K + ';\n')
			bm.write('mut_conf.bcr = ' + bcr + ';\n')
			bm.write('mut_conf.cand_mode = \'' + cand_mode + '\';\n')
			bm.write('mut_conf.date = \'' + date + '\';\n')

			bm.write('mut_op_prop_list = {};\n')
			bm.write('mut_op_mode_list = {\'' + mut_op_mode_list[0] + '\'')
			for mutopmode in mut_op_mode_list[1:]:
				bm.write(',')
				bm.write('\'' + mutopmode + '\'')
			bm.write('};\n')

			bm.write('mut_op_noise_list = {' + mut_op_noise_list[0] + '')
			for mutopnoise in mut_op_noise_list[1:]:
				bm.write(',')
				bm.write('' + mutopnoise + '')
			bm.write('};\n')
			
			bm.write('noise_rep_num = ' + noise_rep_num + ';\n')

			bm.write('for momi = 1:numel(mut_op_mode_list)\n')
			bm.write('\t if strcmp(mut_op_mode_list{1,momi}, \'precise\')\n')
			bm.write('\t\t cur_mut_op_prop.mode = \'precise\';\n')
			bm.write('\t\t cur_mut_op_prop.noise = 0;\n')
			bm.write('\t\t mut_op_prop_list{end+1} = cur_mut_op_prop;\n')
			bm.write('\t\t continue;\n')
			bm.write('\t end\n')
			bm.write('\t for moni = 1:numel(mut_op_noise_list)\n')
			bm.write('\t\t cur_mut_op_prop.mode = mut_op_mode_list{1,momi};\n')
			bm.write('\t\t cur_mut_op_prop.noise = mut_op_noise_list{1,moni};\n')
			bm.write('\t\t mut_op_prop_list{end+1} = cur_mut_op_prop;\n')
			bm.write('\t end\n')
			bm.write('end\n')
			
			bm.write('mut_conf.mut_op_prop_list = mut_op_prop_list;\n')
			bm.write('mut_conf.noise_rep_num = ' + noise_rep_num + ';\n')

			bm.write('trial = ' + trial + ';\n')
			
			# repair parameters
			bm.write('sel_flag = ' + sel_flag + ';\n')
			bm.write('ts_size = ' + ts_size + ';\n')
			bm.write('ts_mode = \'' + ts_mode + '\';\n')

			bm.write(bench + ' = AutoPatch(bm, mdl, mdl_cp, D_run, is_nor, D, D_size, net, nn_stru, T, Ts, in_name, in_range, in_span, icc_name, ic_const, ics_name, oc_name, oc_span, phi_str, spec_i, sel_flag);\n')
			bm.write('TS = generateTestSuite(' + bench + '.D, ts_size, ts_mode);\n')
			bm.write('candidate = ' + bench + '.selectCandidate(TS, mut_conf.cand_mode);\n')
			# perform bug injection trial times
			bm.write('mutants = cell(1,trial);\n')
			bm.write('for mi = 1:trial\n')
			bm.write('\t mutant = ' + bench + '.bugInjection(TS, candidate, mut_conf, mi);\n')
			bm.write('\t mutants{1,mi} = mutant;\n')
			bm.write('end\n')
			if bound_mode == 'natural':
				mut_file = model + '_spec_' + str(phi_i + 1) + '_selflag_' + sel_flag + '_mutmode_' + mut_mode + '_boundmode_' + bound_mode + '_distmode_' + dist_mode + '_K_' + K + '_candmode_' + cand_mode + '_tssize_' + ts_size + '_tsmode_' + ts_mode + '_bcr_' + bcr + '_trial_' + trial + '_' + date + '.mat'
			elif bound_mode == 'specify':
				mut_file = model + '_spec_' + str(phi_i + 1) + '_selflag_' + sel_flag + '_mutmode_' + mut_mode + '_boundmode_' + bound_mode + '_lb_' + bug_lb + '_ub_' + bug_ub + '_distmode_' + dist_mode + '_K_' + K + '_candmode_' + cand_mode + '_tssize_' + ts_size + '_tsmode_' + ts_mode + '_bcr_' + bcr + '_trial_' + trial + '_' + date + '.mat'
			bm.write('save(\'' + mut_file + '\', "mutants");\n')
			bm.write('delete(fullfile([\'breach/Ext/ModelsData/\', \'*_breach.slx\']));\n')
			bm.write('delete(fullfile([\'*.slx\']));\n')
			bm.write('delete(fullfile([\'*.slx.autosave\']));\n')
			bm.write('delete(fullfile([\'*.slx.r202*\']));\n')
			bm.write('delete(fullfile([\'*_breach.slxc\']));\n')
			bm.write('logname = ' + logname + ';\n')
			bm.write('sendEmail(logname);\n')
			bm.write('quit force\n')
			bm.write('EOF\n')