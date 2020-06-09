% imageData = GetVideoImage(filename)
% 
% Gets the video image of a .svd file.
% You can use image(imageData); to display the image.
%
% filename is the path of the .svd file
%
% returns the image data
function imageData = GetVideoImage(filename)

file = actxserver('PolyFile.PolyFile');
try
    file.Open(filename);
    width = 0;
    height = 0;
    imageArray = file.Infos.VideoBitmap.Image('ptcGraphicFormatJPEG', width, height);
    
    % write the image array to a binary file so that we can read it in with
    % imread
    tempImageFileName = tempname;
    fid = fopen(tempImageFileName, 'wb');
    fwrite(fid, imageArray, 'uint8');
    fclose(fid);
 
    imageData = imread(tempImageFileName, 'jpg');
    
    delete(tempImageFileName);
 
    file.Close();
    delete(file);
catch
    if file.IsOpen == 1
        file.Close();
    end
    delete(file);
    rethrow(lasterror);
end