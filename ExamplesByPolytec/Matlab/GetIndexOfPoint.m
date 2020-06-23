% [index] = GetIndexOfPoint(filename, point)
% 
% Gets index of a point from its number. As you can change point indices
% in .svd files, you have to translate an index displayed in the software
% to an index that corresponds to the index into e.g. the measpoints
% or datapoints collection. You can use the returned index
% as input for the point parameter of the GetPointData function.
%
% filename is the path of the .svd file
% point is the (1-based) index of the point as displayed in the software
%
% returns index, the index into the measpoints or datapoints collection
%
function index = GetIndexOfPoint(filename, point)
%
file = actxserver('PolyFile.PolyFile');
invoke(file, 'open', filename);
infos=file.infos;
measpoints=get(infos, 'Item', 'MeasPoints');    
index = invoke(measpoints, 'LabelToIndex', point);
invoke(file, 'close');
delete(file);