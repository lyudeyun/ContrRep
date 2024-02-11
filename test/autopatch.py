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
mut_file = []
mut_idx = []
noise_rep_idx = []
mut_op_mode_list = []
mut_op_noise_list = []
# DE
pop_K_ratio = ''
max_gen = ''
gen_span = ''
F = ''
CR = ''
mut_sgy = ''
cr_sgy = ''
init_type = ''
init_folder = ''
# repair parameters
sel_flag = ''
ts_size = ''
ts_mode = ''
pert_level = ''
search_mode = ''
rep_mode_list = []
budget = ''
# parallel computing 
core_num = ''
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
			elif arg == 'mut_file':
				mut_file.append(argu[0])
			elif arg == 'mut_idx':
				mut_idx.append(argu[0])
			elif arg == 'noise_rep_idx':
				noise_rep_idx.append(argu[0])
			elif arg == 'mut_op_mode':
				mut_op_mode_list.append(argu[0])
			elif arg == 'mut_op_noise':
				mut_op_noise_list.append(argu[0])
			elif arg == 'pop_K_ratio':
				pop_K_ratio = argu[0]
			elif arg == 'max_gen':
				max_gen = argu[0]
			elif arg == 'gen_span':
				gen_span = argu[0]
			elif arg == 'F':
				F = argu[0]
			elif arg == 'CR':
				CR = argu[0]
			elif arg == 'mut_sgy':
				mut_sgy = argu[0]
			elif arg == 'cr_sgy':
				cr_sgy = argu[0]
			elif arg == 'init_type':
				init_type = argu[0]
			elif arg == 'init_folder':
				init_folder = argu[0]
			elif arg == 'sel_flag':
				sel_flag = argu[0]
			elif arg == 'ts_size':
				ts_size = argu[0]
			elif arg == 'ts_mode':
				ts_mode = argu[0]
			elif arg == 'pert_level':
				pert_level = argu[0]
			elif arg == 'budget':
				budget = argu[0]
			elif arg == 'search_mode':
				search_mode = argu[0]
			elif arg == 'rep_mode':
				rep_mode_list.append(argu[0])
			elif arg == 'core_num':
				core_num = argu[0]
			else:
				continue
			if linenum == 0:
				status = 0
# script name 
for phi_i in range(len(phi_str)):
		ds = dataset_tbr[phi_i]
		property = phi_str[phi_i].split(';')
		filename = model + '_spec_' + str(phi_i + 1) + '_selflag_' + sel_flag +  '_tssize_' + ts_size + '_tsmode_' + ts_mode + '_mutidx_' + mut_idx[phi_i] + '_noiseidx_' + str(noise_rep_idx[phi_i]) + '_searchmode_' + search_mode + '_budget_' + budget + '_Repair'
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
			bm.write('\t x_gain = D_run.ps_x.gain;\n')
			bm.write('\t x_gain = diag(x_gain);\n')
			bm.write('\t x_offset = D_run.ps_x.xoffset;\n')
			bm.write('\t y_gain = D_run.ps_y.gain;\n')
			bm.write('\t y_offset = D_run.ps_y.xoffset;\n')
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
			bm.write('M = load(\'' + mut_file[phi_i] + '\');\n')
			bm.write('mut_i = ' + mut_idx[phi_i] + ';\n')
			bm.write('noise_rep_idx = ' + noise_rep_idx[phi_i] + ';\n')
			
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
			
			# DE
			bm.write('DE_param.pop_K_ratio = ' + pop_K_ratio + ';\n')
			bm.write('DE_param.max_gen = ' + max_gen + ';\n')
			bm.write('DE_param.gen_span = ' + gen_span + ';\n')
			bm.write('DE_param.F = ' + F + ';\n')
			bm.write('DE_param.CR = ' + CR + ';\n')
			bm.write('DE_param.mut_sgy = ' + mut_sgy + ';\n')
			bm.write('DE_param.cr_sgy = ' + cr_sgy + ';\n')
			bm.write('DE_param.init_type = \'' + init_type + '\';\n')
			bm.write('DE_param.init_folder = \'' + init_folder + '\';\n')

			# repair parameters
			bm.write('sel_flag = ' + sel_flag + ';\n')
			bm.write('ts_size = ' + ts_size + ';\n')
			bm.write('ts_mode = \'' + ts_mode + '\';\n')
			bm.write('pert_level = ' + pert_level + ';\n')
			bm.write('budget = ' + budget + ';\n')
			bm.write('search_mode = \'' + search_mode + '\';\n')
			bm.write('rep_mode_list = {\'' + rep_mode_list[0] + '\'')
			for repmode in rep_mode_list[1:]:
				bm.write(',')
				bm.write('\'' + repmode + '\'')
			bm.write('};\n')
			
			# parallel computing
			bm.write('core_num = ' + core_num + ';\n')
			bm.write('rng(round(rem(now, 1)*1000000));\n')
			bm.write(bench + ' = AutoPatch(bm, mdl, mdl_cp, D_run, is_nor, D, D_size, net, nn_stru, T, Ts, in_name, in_range, in_span, icc_name, ic_const, ics_name, oc_name, oc_span, phi_str, spec_i, sel_flag);\n')
			bm.write('mutant = M.mutants{1,mut_i};\n')
			bm.write('for pi = 1:numel(mut_op_prop_list)\n')
			bm.write('\t cur_mut_op_mode = mut_op_prop_list{1,pi}.mode;\n')
			bm.write('\t cur_mut_op_noise = mut_op_prop_list{1,pi}.noise;\n')
			bm.write('\t if strcmp(cur_mut_op_mode, \'noise\')\n')
			bm.write('\t\t DE_param.pop_size = DE_param.pop_K_ratio * mutant.K * (1 + cur_mut_op_noise);\n')
			bm.write('\t elseif strcmp(cur_mut_op_mode, \'opacity\')\n')
			bm.write('\t\t DE_param.pop_size = DE_param.pop_K_ratio * mutant.K;\n')
			bm.write('\t elseif strcmp(cur_mut_op_mode, \'precise\')\n')
			bm.write('\t\t DE_param.pop_size = DE_param.pop_K_ratio * mutant.K;\n')
			bm.write('\t else\n')
			bm.write('\t\t error(\'Check your mutation modes!\')\n')
			bm.write('\t end\n')
			bm.write('\t for rmi = 1:numel(rep_mode_list)\n')
			bm.write('\t\t cur_rep_mode = rep_mode_list{1, rmi};\n')
			bm.write('\t\t for bi = 1:budget\n')
			bm.write('\t\t\t mutateWeight(' + bench + '.mdl_m, mutant.bug_mdl, mutant.mut_mode, mutant.mut_op);\n')
			bm.write('\t\t\t repLog_ID = struct;\n')
			bm.write('\t\t\t repLog_ID.mut_op_mode = cur_mut_op_mode;\n')
			bm.write('\t\t\t repLog_ID.mut_op_noise = cur_mut_op_noise;\n')
			bm.write('\t\t\t repLog_ID.K = mutant.K;\n')
			bm.write('\t\t\t repLog_ID.mut_i = mut_i;\n')
			bm.write('\t\t\t repLog_ID.bi = bi;\n')
			# find the idx of the mutated (FL results) according to the mode and noise 
			bm.write('\t\t\t for i = 1:numel(mutant.mut_op_prop_list)\n')
			bm.write('\t\t\t\t if isequal(mutant.mut_op_prop_list{1,i}, mut_op_prop_list{1,pi})\n')
			bm.write('\t\t\t\t\t break;\n')
			bm.write('\t\t\t\t end\n')
			bm.write('\t\t\t end\n')
			bm.write('\t\t\t res_name = [mdl_cp, \'_bug_\', num2str(mutant.bug_lb), \'_\', num2str(mutant.bug_ub), \'_distmode_\', mutant.dist_mode, \'_K_\', num2str(mutant.K), \'_candmode_\', mutant.cand_mode, \'_\', cur_mut_op_mode, \'_\', num2str(cur_mut_op_noise), \'_tssize_\', num2str(ts_size), \'_searchmode_\', search_mode, \'_repmode_\', cur_rep_mode, \'_mutant_\', num2str(mut_i), \'_budget_\', num2str(bi), \'.mat\'];\n')
			bm.write('\t\t\t res_name_prefix = [mdl_cp, \'_bug_\', num2str(mutant.bug_lb), \'_\', num2str(mutant.bug_ub), \'_distmode_\', mutant.dist_mode, \'_K_\', num2str(mutant.K), \'_candmode_\', mutant.cand_mode, \'_\', cur_mut_op_mode, \'_\', num2str(cur_mut_op_noise), \'_tssize_\', num2str(ts_size), \'_searchmode_\', search_mode, \'_repmode_\', cur_rep_mode, \'_mutant_\', num2str(mut_i), \'_budget_\', num2str(bi)];\n')
			bm.write('\t\t\t tic;\n')
			bm.write('\t\t\t if strcmp(search_mode, \'DE\')\n')
			bm.write('\t\t\t\t [bestInd, bestFitness, bestRobList, X_log, fitnessX_log, roblistX_log] = ' + bench + '.altWeightSearch(mutant, mutant.mutated_sps_weight_list{noise_rep_idx, i}, cur_rep_mode, pert_level, DE_param, repLog_ID, core_num, res_name_prefix, cur_mut_op_mode, cur_mut_op_noise);\n')
			bm.write('\t\t\t elseif strcmp(search_mode, \'random\')\n')
			bm.write('\t\t\t\t [bestInd, bestFitness, bestRobList, X_log, fitnessX_log, roblistX_log] = ' + bench + '.randomRepair(mutant, mutant.mutated_sps_weight_list{noise_rep_idx, i}, cur_rep_mode, DE_param, repLog_ID, core_num, res_name_prefix, cur_mut_op_mode, cur_mut_op_noise);\n')
			bm.write('\t\t\t else\n')
			bm.write('\t\t\t\t error(\'Check the search_mode!\');\n')
			bm.write('\t\t\t end\n')
			bm.write('\t\t\t rep_time = toc;\n')
			bm.write('\t\t\t save(res_name, "mutant", "cur_mut_op_mode", "cur_mut_op_noise", "DE_param", "bestInd", "bestFitness", "bestRobList", "X_log", "fitnessX_log", "roblistX_log", "rep_time");\n')
			bm.write('\t\t\t delete(fullfile([\'breach/Ext/ModelsData/\', \'*_breach.slx\']));\n')
			bm.write('\t\t\t delete(fullfile([\'*.slx\']));\n')
			bm.write('\t\t\t delete(fullfile([\'*.slx.autosave\']));\n')
			bm.write('\t\t\t delete(fullfile([\'*.slx.r202*\']));\n')
			bm.write('\t\t\t delete(fullfile([\'*_breach.slxc\']));\n')
			bm.write('\t\t end\n')
			bm.write('\t end\n')
			bm.write('end\n')
	
			bm.write('logname = ' + logname + ';\n')
			bm.write('sendEmail(logname);\n')
			bm.write('quit force\n')
			bm.write('EOF\n')