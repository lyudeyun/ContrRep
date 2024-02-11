function [lb, ub] = obtainBound(sps_weight_info)
% obtainBound function can determine the lower bound and the upper bound of the suspicious weight values in the same layer.
%
% Inputs:
%   sps_weight_info: includes the information of each suspicious weight, including layer_idx, right_endpoint_idx, left_endpoint_idx, weight_value.
% Outputs:
%   lb: lower bound
%   ub: upper bound

[row, ~] = size(sps_weight_info);

lb = zeros(1,row);
ub = zeros(1,row);

% obtain all the layer indexs 
layers = unique(sps_weight_info(:,1));

% classify the weights based on their layers and calculate the boundaries of different layers
min_layer = min(layers);
max_weight = accumarray(sps_weight_info(:,1) - min_layer + 1, sps_weight_info(:,4), [], @max);
min_weight = accumarray(sps_weight_info(:,1) - min_layer + 1, sps_weight_info(:,4), [], @min);

% temporarily use this method
for i = 1: row
    
    idx = find(layers == sps_weight_info(i,1));

    max_w = max_weight(idx,1);
    min_w = min_weight(idx,1);

    if min_w < 0
        lb(1,i) = 2 * min_w;
    else
        lb(1,i) = min_w/2;
    end
    if max_w > 0
        ub(1,i) = 2 * max_w;
    else
        ub(1,i) = max_w/2;
    end
end

end