% fft = GetFFTAcqProps(filename)
% 
% Gets the FFT acquisition properties as a struct.
%
% This demonstrates how to access acquisition settings.
%
% filename is the path of the .svd, .pvd or .set file
%
% returns the struct of the FFT acquisition properties
function fft = GetFFTAcqProps(filename)

file = actxserver('PolyFile.PolyFile');
try
    file.Open(filename);
    acqProps = file.Infos.Acquisition.ActiveProperties;
    fft = struct(acqProps.Fft);
 
    file.Close();
    delete(file);
catch
    if file.IsOpen == 1
        file.Close();
    end
    delete(file);
    rethrow(lasterror);
end