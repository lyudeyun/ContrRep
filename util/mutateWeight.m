function mutateWeight(mdl, bug_mdl, mut_mode, mut_op)
% mutateWeight function can mutate weights of the given simulink model based on mut_mode and mut_op.
%
% Inputs:
%   mdl: simulink model
%   bug_mdl: the name of the mutated simulink model 
%   mut_op: mutation operator
% Outputs:
%   bug_mdl: the simulink model with the inserted weight bugs
%   sps_weight: suspicious weight

%%% usage of find_system function
% nn_blocks = find_system('WT_FFNN_trainbfg_5_5_5_Dec_22/Feed-Forward Neural Network','LookUnderMasks','on');
% nn_blocks consists of the name of all the blocks

%%% usage of get_param function
% param_list = get_param('model/XXX_block','DialogParameters')
% param_list contains all of the numeric fields about XXX_block, then you
% can rerun this funtion to get the value of the numeric field you want
% get_param('model/XXX_block','numeric field 1')
%%% usage of set_param function
% set_param('model/XXX_block','numeric field 1', 'value')

% obtain the absolute path of the original model file
mdl_path = which([mdl, '.slx']);
% delete it if it exists.
if isfile([bug_mdl, '.slx'])
    delete([bug_mdl, '.slx']);
end
% copy original simulink model to initialize the mutated simulink model
copyfile(mdl_path, [bug_mdl, '.slx']);
load_system(bug_mdl);

% insert the bugs one by one
for bi = 1:size(mut_op, 1)
    layer_idx = mut_op(bi, 1);
    right_idx = mut_op(bi, 2);
    left_idx = mut_op(bi, 3);
    bug_value = mut_op(bi, 4);
    % obtain the name of current suspicious weight. But currently, matlab
    % can only obtain all weights whose right endpoints are the same as that of current
    % suspicious weight.
    if layer_idx == 1
        if contains(bug_mdl, 'WT') || contains(bug_mdl, 'ACC')
            % weight block name
            weight_str = [bug_mdl, '/Feed-Forward Neural Network/Layer ', num2str(layer_idx), '/IW{1,1}/IW{1,1}(', ...
                num2str(right_idx), ',:)'''];
        elseif contains(bug_mdl, 'AFC')
            weight_str = [bug_mdl, '/Air Fuel Control Model 1/Feed-Forward Neural Network/Layer ', num2str(layer_idx), '/IW{1,1}/IW{1,1}(', ...
                num2str(right_idx), ',:)'''];
        elseif contains(bug_mdl, 'SC')
            weight_str = [bug_mdl, '/Subsystem/Feed-Forward Neural Network/Layer ', num2str(layer_idx), '/IW{1,1}/IW{1,1}(', ...
                num2str(right_idx), ',:)'''];
        else
            error('The target blocks can not be found!');
        end
    else
        if contains(bug_mdl, 'WT') || contains(bug_mdl, 'ACC')
            weight_str = [bug_mdl, '/Feed-Forward Neural Network/Layer ', ...
                num2str(layer_idx), '/LW{', num2str(layer_idx), ',', num2str(layer_idx-1), '}/IW{', num2str(layer_idx), ',', num2str(layer_idx-1), ...
                '}(', num2str(right_idx), ',:)'''];
        elseif contains(bug_mdl, 'AFC')
            weight_str = [bug_mdl, '/Air Fuel Control Model 1/Feed-Forward Neural Network/Layer ', ...
                num2str(layer_idx), '/LW{', num2str(layer_idx), ',', num2str(layer_idx-1), '}/IW{', num2str(layer_idx), ',', num2str(layer_idx-1), ...
                '}(', num2str(right_idx), ',:)'''];
        elseif contains(bug_mdl, 'SC')
            weight_str = [bug_mdl, '/Subsystem/Feed-Forward Neural Network/Layer ', ...
                num2str(layer_idx), '/LW{', num2str(layer_idx), ',', num2str(layer_idx-1), '}/IW{', num2str(layer_idx), ',', num2str(layer_idx-1), ...
                '}(', num2str(right_idx), ',:)'''];
        else
            error('The target blocks can not be found!');
        end
    end

    % includes all weights whose right endpoints are the same as that of current
    % target weight.
    cur_weight_row_str = get_param(weight_str, 'Value');

    % split the str by semicolon ';'
    cur_weight_row_str = erase(cur_weight_row_str, '[');
    cur_weight_row_str = erase(cur_weight_row_str, ']');
    cur_weight_row_cell = strsplit(cur_weight_row_str, ';');

    if strcmp(mut_mode, 'plus')
        % obtain the target weight
        target_weight_str = cur_weight_row_cell{1,left_idx};
        % we can specify the number of significant digits of vpa funciton. Since the target weight is
        % in a state of flux, there is no need to pursue a absolutely precious value.
        target_weight = vpa(target_weight_str, 100);
        % insert the weight bug
        target_weight = target_weight + bug_value;
        % sym to str
        target_weight_str = char(target_weight);
        % replace sps_weight_str with target_weight_str
        cur_weight_row_cell{1,left_idx} = target_weight_str;
    elseif strcmp(mut_mode, 'replace')
        % replace the original weight with bug_value
        cur_weight_row_cell{1,left_idx} = num2str(bug_value);
    end

    % assemble cur_weight_row_str
    new_weight_row_str = '';
    new_weight_row_str = strjoin(cur_weight_row_cell, ';');
    new_weight_row_str = ['[', new_weight_row_str, ']'];

    % apply the weight with a inserted bug
    set_param(weight_str, 'Value', num2str(new_weight_row_str));
end
% save the model with a weight bug
% save_system(bug_mdl, [],'OverwriteIfChangedOnDisk',true);
save_system(bug_mdl);
close_system(bug_mdl);
end
 