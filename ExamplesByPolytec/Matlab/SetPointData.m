% SetPointData(filename, domain, usd, removeexisting, point, frame, y)
%
% Set UDDS in the given domain ('FFT' or 'Time'). usd is a struct
% describing the signal. Either create it or modify the usd you have got
% from the GetPointData function. y contains the data. point is
% the point index. If point is 0, the data in the rows of y are set
% to the different points. Then the row index corresponds to the point index.
% frame is the frame number. You have to specify a frame number starting from 1.
% Remember, data must be put with the sequential increasing number of frame.
% If removeexisting is true (1), then a signal with the same name is
% removed (including all its data) before the new one is created.
% 
function SetPointData(filename, domain, usd, removeexisting, point, frame, y)
%
file = actxserver('PolyFile.PolyFile');
try
    file.Readonly = 0;
    file.Open(filename);
    % create the build flags
    ptcBuildPointData3d = 722751;
    pointdomains = file.GetPointDomains(ptcBuildPointData3d);
    % create and fill the user signal description
    sigdesc = actxserver('PolySignal.SignalDescription');
    sigdesc.Name = usd.Name;
    sigdesc.DataType = usd.DataType;
    domainType = 'ptcDomainSpectrum';
    if (strcmpi(domain, 'FFT') == 0)
        domainType = 'ptcDomainTime';
    end
    sigdesc.DomainType = domainType;
    sigdesc.FunctionType = usd.FunctionType;
    sigdesc.Complex = usd.Complex;
    sigdesc.PowerSignal = usd.PowerSignal;
    sigdesc.DbReference = usd.DbReference;
    for i=1:length(usd.ResponseDOFs)
        dof = usd.ResponseDOFs(i);
        newDof = sigdesc.ResponseDOFs.Add();
        newDof.ChannelName = dof.ChannelName;
        newDof.Direction = dof.Direction;
        newDof.Node = dof.Node;
        newDof.NodeDescription = dof.NodeDescription;
        newDof.Quantity = dof.Quantity;
        newDof.Unit = dof.Unit;
        newDof.release;
    end
    for i=1:length(usd.ReferenceDOFs)
        dof = usd.ReferenceDOFs(i);
        newDof = sigdesc.ReferenceDOFs.Add();
        newDof.ChannelName = dof.ChannelName;
        newDof.Direction = dof.Direction;
        newDof.Node = dof.Node;
        newDof.NodeDescription = dof.NodeDescription;
        newDof.Quantity = dof.Quantity;
        newDof.Unit = dof.Unit;
        newDof.release;
    end
    sigdesc.XAxis.Name = usd.XName;
    sigdesc.XAxis.Unit = usd.XUnit;
    sigdesc.XAxis.Min = usd.XMin;
    sigdesc.XAxis.Max = usd.XMax;
    sigdesc.XAxis.MaxCount = usd.XCount;
    sigdesc.YAxis.Name = usd.YName;
    sigdesc.YAxis.Unit = usd.YUnit;
    sigdesc.YAxis.Min = usd.YMin;
    sigdesc.YAxis.Max = usd.YMax;
    % check if a user signal with the same name exists
    existingSignal = pointdomains.FindSignal(sigdesc, 1);
    if (isempty(existingSignal) == 0)
        if (removeexisting == 1)
            % remove the signal (and its data)
            existingSignal.Channel.Signals.Remove(existingSignal.Name);
            existingSignal.release;
            usersignal = pointdomains.AddSignal(sigdesc);
        else
            % use the existing signal
            usersignal = existingSignal;
        end
    else
        usersignal = pointdomains.AddSignal(sigdesc);
    end
    datapoints = pointdomains.Type(sigdesc.DomainType).datapoints;
    % handle complex data
    if (sigdesc.Complex == 1)
        odd = bitand(0:2*size(y,2)-1, 1) > 0;
        data = zeros(1,2*size(y,2));
    end
    if (point == 0)
        from = 1;
        to = size(y,1);
    else
        from = point;
        to = point;
    end
    for i = from:to
        datapoint = get(datapoints, 'item', i);
        if (sigdesc.Complex == 1)
            data(~odd) = real(y(i,:));
            data(odd) = imag(y(i,:));
            datapoint.SetData(usersignal, frame, single(data));
        else
            datapoint.SetData(usersignal, frame, single(y(i,:)));
        end
    end
    file.Save();
    file.Close();
    delete(sigdesc);
    delete(file);
catch
    if file.IsOpen == 1
        file.Close();
    end
    delete(file);
    rethrow(lasterror);
end

