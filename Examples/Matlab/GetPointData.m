% [x,y,usd] = GetPointData(filename, domainname, channelname, signalname, displayname,
%   point, frame)
% 
% Gets original or user defined data from a polytec file.
%
% filename is the path of the .pvd or .svd file
% domainname is the name of the domain, e.g. 'FFT' or 'Time'
% channelname is the name of the channel, e.g. 'Vib' or 'Ref1' or 'Vib &
%   Ref1' or 'Vib X' or 'Vib Y' or 'Vib Z'.
% signalname is the name of the signal, e.g. 'Velocity' or 'Displacement'
% displayname is the name of the display, e.g. 'Real' or 'Magnitude' or
%   'Samples'. If the display name is 'Real & Imag.' the data is returned
%   as complex values.
% point is the (1-based) index of the point to get data from. If point is
%   0 the data of all points will be returned. y will contain the data of
%   point i at row index i.
% frame is the frame number of the data. for data acquired in MultiFrame
%   mode, 0 is the averaged frame and 1-n are the other frames. For user
%   defined datasets the frame number is in the range 1-n where n is the
%   number of frames in the user defined dataset. For all other data,
%   use frame number 0.
%
% returns x, the x axis values of the data
% returns y, the data. colomns correspond to the x-axis, rows to the point
%   index. for point = 0: rows for points that have no data are set to zeros.
% returns usd, a struct describing the signal
%
function [x,y,usd] = GetPointData(filename, domainname, channelname, signalname, displayname, point, frame)
%
file = actxserver('PolyFile.PolyFile');
try
    file.Open(filename);
    pointdomains = file.GetPointDomains();
    pointdomain = pointdomains.Item(domainname);
    channel = pointdomain.Channels.Item(channelname);
    signal = channel.Signals.Item(signalname);
    display = signal.Displays.Item(displayname);
    %
    signalDesc = signal.Description;
    xaxis = signalDesc.XAxis;
    yaxis = signalDesc.YAxis;
    x = xaxis.Min:(xaxis.Max - xaxis.Min)/(xaxis.MaxCount - 1):xaxis.Max;
    %
    usd.Name = signalDesc.Name;
    usd.Complex = signalDesc.Complex;
    usd.DataType = signalDesc.DataType;
    usd.DomainType = signalDesc.DomainType;
    usd.FunctionType = signalDesc.FunctionType;
    usd.PowerSignal = signalDesc.PowerSignal;
    usd.Is3D = signalDesc.ResponseDOFs.Count > 0 && ~isempty(strfind(signalDesc.ResponseDOFs.Direction, 'ptcVector'));
    responseDOFs = signalDesc.ResponseDOFs;
    if (responseDOFs.Count == 0)
        usd.ResponseDOFs = [];
    else
        for i=1:responseDOFs.Count
            usd.ResponseDOFs(i) = struct(responseDOFs.Item(i));
        end
    end
    referenceDOFs = signalDesc.ReferenceDOFs;
    if (referenceDOFs.Count == 0)
        usd.ReferenceDOFs = [];
    else
        for i=1:referenceDOFs.Count
            usd.ReferenceDOFs(i) = struct(referenceDOFs.Item(i));
        end
    end
    usd.DbReference = signalDesc.DbReference;
    usd.XName = xaxis.Name;
    usd.XUnit = xaxis.Unit;
    usd.XMin = xaxis.Min;
    usd.XMax = xaxis.Max;
    usd.XCount = xaxis.MaxCount;
    usd.YName = yaxis.Name;
    usd.YUnit = yaxis.Unit;
    usd.YMin = yaxis.Min;
    usd.YMax = yaxis.Max;
    %
    datapoints = pointdomain.datapoints;
    if (point == 0)
        % get data of all points
        y = [];
        for i=1:datapoints.count
            datapoint = datapoints.Item(i);
            if ~isempty(strfind(channel.caps, 'ptcChannelCapsUser'))        
                ytemp = double(datapoint.GetData(display, frame));
                if (length(ytemp) > 0)
                    % not all points might have user defined data attached.
                    % polytec file access returns an empty array in this case.
                    if (isempty(y))
                        y = zeros(datapoints.count, length(ytemp));
                    end
                    y(i,1:length(ytemp)) = ytemp;
                end
            else
                try
                    % ignore errors because of invalid data, the result row
                    % will contain zeros in this case
                    ytemp = double(datapoint.GetData(display, frame));
                    if (isempty(y))
                        y = zeros(datapoints.count, length(ytemp));
                    end
                    y(i,:) = ytemp;
                catch
                end
            end
        end
    else
        datapoint = datapoints.Item(point);
        y = double(datapoint.GetData(display, frame));
    end
    % handle complex data
    if (usd.Complex == 1 && ~isempty(strfind(display.Type, 'ptcDisplayRealImag')))
        realData = y(:,1:2:end);
        imagData = y(:,2:2:end);
        y = complex(realData, imagData);
    end
    %
    file.Close();
    delete(file);
catch
    if file.IsOpen == 1
        file.Close();
    end
    delete(file);
    rethrow(lasterror);
end
