'#Reference {3D148768-F913-49D8-BBF4-F3CE03A601CB}#1.0#0#C:\Program Files\Common Files\Polytec\COM\PolyDataVisualizer.dll#Polytec PolyDataVisualizer Type Library
'#Reference {E44752C9-2D41-48A6-9B74-66D5B7505325}#1.0#0#C:\Program Files\Common Files\Polytec\COM\PolyProperties.dll#Polytec PolyProperties Type Library
'#Reference {E68EA160-8AD4-11D3-8F08-00104BB924B2}#1.0#0#C:\Program Files\Common Files\Polytec\COM\SignalDescription.dll#Polytec SignalDescription Type Library
'#Reference {CE68D434-5052-431F-BE75-F3C23458127A}#1.0#0#C:\Program Files\Common Files\Polytec\COM\PolySignal.dll#Polytec PolySignal Type Library
'#Reference {F08ACE20-C7AD-46CA-8001-D5158D9B0224}#1.0#0#C:\Program Files\Common Files\Polytec\COM\PolyMath.dll#Polytec PolyMath Type Library
'#Reference {A65C100F-C1FE-4C3B-9C43-46F4FB4C3BC3}#1.0#0#C:\Program Files\Common Files\Polytec\COM\PolyFile.dll#Polytec PolyFile Type Library
' POLYTEC MACRO DEMO
' ----------------------------------------------------------------------
'
' This macro calculates the complex average of the vibrometer velocity
' signal over all scan points and saves the result as user defined dataset
' in the average domain of the given scan file.
'
' When running the macro you are asked to navigate to a PSV scan file.
' This file has to meet the following conditions:
'
' - you have to have exclusive write access to the file. We strongly recommend to
'   use a backup copy of your original file with this macro. The macro
'   will fail if the file is open in PSV.
' - the measurement has to be done in FFT mode and the vibrometer
'   channel has to offer a complex velocity signal
'
' To display the calculated data in PSV do the following:
' - start PSV and open the scan file
' - select Presentation/View/Average Spectrum
' - in analyzer window toolbar select Channel/Usr
' - in analyzer window toolbar select Signal/Complex Average Spectrum
'
' References
' - Polytec PhysicalUnit Type Library
' - Polytec PolyAlignment Type Library
' - Polytec PolyDataVisualizer Type Library
' - Polytec PolyDigitalFilters Type Library
' - Polytec PolyFile Type Library
' - Polytec PolyFrontEnd Type Library
' - Polytec PolyGenerators Type Library
' - Polytec PolyInplane Type Library
' - Polytec PolyMath Type Library
' - Polytec PolyProperties Type Library
' - Polytec PolyScanHead Type Library
' - Polytec PolyScope Type Library
' - Polytec PolySignal Type Library
' - Polytec PolyWaveforms Type Library
' - Polytec Vibrometer Type Library
' - Polytec WindowFunction Type Library
' - Polytec SignalDescription Type Library
' ----------------------------------------------------------------------

Option Explicit

Const c_strFileFilter As String = "Scan File (*.svd)|*.svd|All Files (*.*)|*.*||"
Const c_strFileExt As String = "svd"

Sub Main
' -------------------------------------------------------------------------------
'	Main procedure.
' -------------------------------------------------------------------------------
	Dim oFile  As PolyFile

	' get filename and path
	Dim strFileName As String
	strFileName = FileOpenDialog()

	If (strFileName = "") Then
		MsgBox("No filename has been specified, macro exits now.", vbOkOnly)
		Exit Sub
	End If

	If (MsgBox("This macro will modify the file '" + strFileName + _
		"'. We strongly recommend to work with a backup copy of original data only. " + _
		"Do you want to continue?", vbYesNo) = vbNo) Then
		Exit Sub
	End If

	' we have to open the file for read/write, otherwise we cannot save our
	' user defined dataset to the file
	If Not OpenFile(oFile, strFileName) Then
		Exit Sub
	End If

    ' provide access to the acquisition properties
    Dim oAcqInfoModes As AcquisitionInfoModes
    Set oAcqInfoModes = oFile.Infos.AcquisitionInfoModes

    ' check the acquisition mode - should be FFT
    Dim AcqMode As PTCAcqMode
    AcqMode = oAcqInfoModes.ActiveMode
    If (AcqMode <> ptcAcqModeFft) Then
        MsgBox("Please select a file with acquisition mode FFT", vbExclamation)
    	oFile.Close()
        Exit Sub
    End If

    Dim oAcqProps As AcquisitionPropertiesContainer
	Set oAcqProps = oAcqInfoModes.ActiveProperties

    Dim oChannelsAcqProps As ChannelsAcqPropertiesContainer
    Set oChannelsAcqProps = oAcqProps.ChannelsProperties

    ' set source for data to channel and signal
	Dim oPointDomain As PointDomain
	Set oPointDomain = oFile.GetPointDomains(ptcBuildPointData3d).type(ptcDomainSpectrum)

	Dim bRe As Boolean
	bRe = CheckComplexSignal(oPointDomain)
	If bRe = False Then
		MsgBox("No file with complex signal has been specified, macro exits now.", vbOkOnly)
    	oFile.Close()
		Exit Sub
	End If

	Dim oSignal As Signal
	Dim oDomain As Domain
	Set oDomain = oPointDomain
	Set oSignal = oDomain.Channels("Vib").Signals("Velocity")

    ' hold average data in single array for real and imaginary part
    Dim asglComplex() As Single
    Call CalculateComplexAverage(oPointDomain, asglComplex)

	' create the new signal in the point average domain
	Dim oAverageDomains As PointAverageDomains
	Set oAverageDomains = oFile.GetPointAverageDomains(ptcBuildPointData3d)

	' now add the signal and data
	Call AddUserSignal(oAverageDomains, oSignal, asglComplex)

    oFile.Save()
    oFile.Close()

	MsgBox("Macro has finished.", vbOkOnly)
End Sub

Function CheckComplexSignal(oPointDomain As PointDomain) As Boolean
' -------------------------------------------------------------------------------
' Check file properties.
' -------------------------------------------------------------------------------
	Dim bRe As Boolean
	bRe = True

	' to make cast
	Dim oDomain As Domain
	Set oDomain = oPointDomain

	Dim oChannels As Channels
	Dim oChannel As Channel
	Set oChannels = oDomain.Channels
	If (oChannels.Exists("Vib")) Then
		Set oChannel = oChannels.Item("Vib")

		Dim oSignals As Signals
		Dim oSignal  As Signal

		Set oSignals = oChannel.Signals
		If (oSignals.Exists("Velocity")) Then
			Set oSignal = oSignals("Velocity")
			If (oSignal.Description.Complex = False) Then
				bRe = False
			End If
		Else
			bRe = False
		End If

	Else
		bRe = False
	End If

	CheckComplexSignal = bRe
End Function

Sub CalculateComplexAverage(oPointDomain As PointDomain, asglComplex() As Single)
' -------------------------------------------------------------------------------
' Calculate the complex average.
' -------------------------------------------------------------------------------
	' to make cast
	Dim oDomain As Domain
	Set oDomain = oPointDomain

	Dim oChannels As Channels
	Dim oChannel As Channel
	Set oChannels = oDomain.Channels
	If (oChannels.Exists("Vib")) Then
		Set oChannel = oChannels.Item("Vib")
	Else
		Exit Sub
	End If

	Dim oSignals As Signals
	Dim oSignal  As Signal
	Set oSignals = oChannel.Signals
	If (oSignals.Exists("Velocity")) Then
		Set oSignal = oSignals("Velocity")
	Else
		Exit Sub
	End If

	If (oSignal.Description.Complex = False) Then
		Exit Sub
	End If


    ' construct display objects for interleaved real and imaginary part
    Dim oDisplay As Display
	Set oDisplay = oSignal.Displays(ptcDisplayRealImag)

	Dim oStat As New Statistics

    Dim bValid As Boolean

    ' loop over all measurement points
    Dim oDataPoint As DataPoint
    For Each oDataPoint In oDomain.DataPoints
        ' check if measurement point is valid
        ' test the valid flag of the point status
        bValid = (oDataPoint.GetScanStatus(oDisplay) And ptcScanStatusValid) <> 0
        If (bValid) Then
            ' measurement point is valid
        	oStat.Add(oDataPoint.GetData(oDisplay, 0))
        End If
    Next oDataPoint

	asglComplex = oStat.Mean
End Sub

Function AddUserSignal(oAverageDomains As PointAverageDomains, oSignal As Signal, asglComplex() As Single)
' -------------------------------------------------------------------------------
' Set user signal description, add signal, add data.
' -------------------------------------------------------------------------------
	' to make cast

	' set the properties of the user defined signal
	Dim oUsrSigDesc As SignalDescription
	Set oUsrSigDesc = oSignal.Description.Clone()

	With oUsrSigDesc
		.DataType = ptcDataAverage
		.Name = "Complex Average Spectrum"
		.Complex = True

		.XAxis.MaxCount = (UBound(asglComplex) - LBound(asglComplex) + 1) / 2
	End With

	Dim oUsrSignal As Signal
	Set oUsrSignal = oAverageDomains.FindSignal(oUsrSigDesc, True)

	' check if a signal with the same name exits already
	If (oUsrSignal Is Nothing) Then
		' now add the signal
		Set oUsrSignal = oAverageDomains.AddSignal(oUsrSigDesc)
	Else
		If (MsgBox("A user defined signal with the name '" + oUsrSigDesc.Name + "' exists already. Do you want to replace it?", vbYesNo) = vbNo) Then
			Exit Function
		End If

		' exchange the signal
		oUsrSignal.Channel.Signals.Update(oUsrSignal.Name, oUsrSigDesc)
	End If

	' now add the data
	oAverageDomains.type(oUsrSigDesc.DomainType).SetData(oUsrSignal, 1, asglComplex)
End Function

' *******************************************************************************
' * Helper functions and subroutines
' *******************************************************************************
Const c_OFN_HIDEREADONLY As Long = 4

Private Function FileOpenDialog() As String
' -------------------------------------------------------------------------------
' Select file.
' -------------------------------------------------------------------------------
	On Error GoTo MCreateError
	Dim fod As Object
	Set fod = CreateObject("MSComDlg.CommonDialog")
	fod.Filter = c_strFileFilter
	fod.Flags = c_OFN_HIDEREADONLY
	fod.CancelError = True
	On Error GoTo MCancelError
	fod.ShowOpen
	FileOpenDialog = fod.FileName
	GoTo MEnd
MCancelError:
	FileOpenDialog = ""
	GoTo MEnd
MCreateError:
	FileOpenDialog = GetFilePath(, c_strFileExt, CurDir(), "Select a file", 0)
MEnd:
End Function

Private Function OpenFile(oFile  As PolyFile, strFileName As String) As Boolean
' -------------------------------------------------------------------------------
' Instantiate PolyFile object, open the File.
' -------------------------------------------------------------------------------
	On Error GoTo MErrorHandler
	Dim bRe As Boolean
	bRe = True

	Set oFile = New PolyFile
	If oFile.ReadOnly Then
		oFile.ReadOnly = False
	End If

	On Error Resume Next
	oFile.Open (strFileName)

	On Error GoTo 0
	If Not oFile.IsOpen Then
		MsgBox("Can not open the file."& vbCrLf & _
		"Check the file attribute is not read only!", vbExclamation)
		bRe = False
	End If
MErrorHandler:
	Select Case Err
	Case 0
		OpenFile = bRe
	Case Else
		bRe = False
		Resume MErrorHandler
	End Select
End Function
