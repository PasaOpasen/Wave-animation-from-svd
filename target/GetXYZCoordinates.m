% XYZ = GetXYZCoordinates(filename, point)
% ----------------------------------------
% Gets XYZ coordinates of the scan points from a polytec file.
%
% This is only possible for files containing 3D geometry or that have
%   a distance to the object specified. Otherwise there will be an
%   error message.
%
% filename is the path of the .svd file
% 
% point is the (1-based) index of the point to get the coordinates from. If point is
%   0 the coordiantes of all points will be returned. XYZ will contain the data of
%   point i at row index i.
%
% returns the xyz coordinates. columns correspond to the geometry X, Y, Z
%   in meter, rows to the point index.
%
function XYZ = GetXYZCoordinates(filename, point)
%

file = actxserver('PolyFile.PolyFile');
try
    file.Open(filename);
    measpoints = file.Infos.MeasPoints;
 
    if (point == 0)
        XYZ=zeros(measpoints.count,3);
        for i=1:measpoints.count
            measpoint=measpoints.Item(int32(i));
            [X,Y,Z]=measpoint.CoordXYZ();
            XYZ(i,:)=[X,Y,Z];                  
        end
    else
        measpoint=measpoints.Item(int32(point));
        [X,Y,Z]=measpoint.CoordXYZ();
        XYZ=[X,Y,Z];
    end
    file.Close();
    delete(file);
catch
    if file.IsOpen == 1
        file.Close();
    end
    delete(file);
    rethrow(lasterror);
end