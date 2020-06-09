% CalculateFFT(filename)
%
% calculates an FFT from time data of the velocity signal of the vibrometer channel and
% adds the result as user defined data set to the original data.
%
% Note: you should run this algorithm only on a backup copy of the original
% data. The original data has to contain time data. No window function is
% applied before the FFT is calculated.
%
function CalculateFFT(filename)
%
% read in the original time data of the vibrometer channel
[x,y,usd] = GetPointData(filename, 'Time', 'Vib', 'Velocity', 'Samples', 0, 0);
% calculate the FFT. we have to transpose the read in data because the
% FFT is calculated column-wise whereas the data of the different
% measurement points is stored in rows.
Y = fft(y')';
% the number of FFT lines is half of the number of time samples
nLines = size(y,2) / 2;
% we do not use the DC fft line
Y = Y(:,2:nLines+1);
% normalize the FFT
Y = Y/nLines;
% update the user signal description
samplefreq = (usd.XCount - 1) / (usd.XMax - usd.XMin);
resolution = 0.5*samplefreq/nLines;
usd.Name = 'Matlab FFT';
usd.Complex = 1;
usd.DomainType = 'ptcDomainSpectrum';
usd.FunctionType = 'ptcFunctionSpectrumType';
usd.XName = 'Frequency';
usd.XUnit = 'Hz';
usd.XMin = resolution;
usd.XMax = resolution * nLines;
usd.XCount = nLines;
% add the data as user defined datasets to the FFT domain
SetPointData(filename, 'FFT', usd, 1, 0, 1, Y);
