% [freq, y] = GetBandData(filename, domainname, channelname, signalname, displayname,
%   band)
% 
% Gets original or user defined band data from a polytec file.
%
% filename is the path of the .svd file
% domainname is the name of the domain, e.g. 'FFT' or 'RMS'
% channelname is the name of the channel, e.g. 'Vib' or 'Ref1' or 'Vib &
%   Ref1' or 'Vib X' or 'Vib Y' or 'Vib Z'
% signalname is the name of the signal, e.g. 'Velocity' or 'Displacement'
% displayname is the name of the display, e.g. 'Real' or 'Magnitude' or
%   'Real & Imag.'
% band is the (1-based) index of the band to get data from. If band is
%   0 the data of all bands will be returned. y will contain the data of
%   band i at row index i.
% frame is the frame number of the data. for data acquired in MultiFrame
%   mode, 0 is the averaged frame and 1-n are the other frames. For user
%   defined datasets the frame number is in the range 1-n where n is the
%   number of frames in the user defined dataset. For all other data,
%   use frame number 0.
%
% returns 
%   freq: frequency or vector of frequencies.
%     For FFT and RMS bands the peak frequency is returned,
%     for 3rd octave bands this is the geometric mean of the upper and lower band limits.
%   y: the data.
%     columns correspond to the scan point index, rows to the band index.
%
function [freq,y] = GetBandData(filename, domainname, channelname, signalname, displayname, band, frame)
%
if (nargin == 6)
    % use frame number 0 for original data if parameter is not given
    frame = 0;
end
file = actxserver('PolyFile.PolyFile');
try
    invoke(file, 'Open', filename);
    ptcBuildBandDataXYZ = 592703;
    banddomains = file.GetBandDomains(ptcBuildBandDataXYZ);
    banddomain = banddomains.Item(domainname);
    channel = banddomain.Channels.Item(channelname);
    signal = channel.Signals.Item(signalname);
    display = signal.Displays.Item(displayname);
    %
    databands = banddomain.GetDataBands(signal);
    if (band == 0)
        % get data of all bands
        % note: as Item() takes a long or a string, we have to cast explicitly
        % to long here
        databand = get(databands, 'Item', int32(1));
        y = double(databand.GetData(display, frame));        
        y = zeros(databands.count, size(y,2));
        freq=zeros(databands.count,1);
        for i=1:databands.count
            databand = databands.Item(int32(i));
            freq(i)=databand.peak;
            y(i,:) = double(databand.GetData(display, frame));        
        end
    else
        databand = databands.Item(int32(band));
        freq=databand.peak;
        y = double(databand.GetData(display, frame));
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