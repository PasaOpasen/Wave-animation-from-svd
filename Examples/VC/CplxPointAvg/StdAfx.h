// stdafx.h : include file for standard system include files,
//  or project specific include files that are used frequently, but
//      are changed infrequently
//

#if !defined(AFX_STDAFX_H__0ABE6A97_CF4C_4E3B_A218_A785F0F12DA4__INCLUDED_)
#define AFX_STDAFX_H__0ABE6A97_CF4C_4E3B_A218_A785F0F12DA4__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#define VC_EXTRALEAN		// Exclude rarely-used stuff from Windows headers
#define WINVER	0x601		// Windows 7 as minimum OS

#include <afxwin.h>         // MFC core and standard components
#include <afxext.h>         // MFC extensions
#include <afxdisp.h>        // MFC Automation classes
#include <afxdtctl.h>		// MFC support for Internet Explorer 4 Common Controls
#ifndef _AFX_NO_AFXCMN_SUPPORT
#include <afxcmn.h>			// MFC support for Windows Common Controls
#endif // _AFX_NO_AFXCMN_SUPPORT

// get rid of warning 'cast truncates constant value caused' by the definition of VARIANT_TRUE
#undef VARIANT_TRUE
#define VARIANT_TRUE ((VARIANT_BOOL)-1)

#pragma warning (disable:4100 4786)
#pragma warning (push, 3)
// put all STL includes here to avoid warning messages
#include <vector>
#include <iostream>
#include <fstream>
#pragma warning (pop)

// Imports the type libraries of Polytec File Access
// If these files are not found check the include path in
// Project Settings -> C/C++ -> Preprocessor -> Additional Include Paths.
// It should point to %CommonProgramFiles%\Polytec\COM in 32-bit OS. In
// Vista64, the path should be %CommonProgramFiles(x86)%\Polytec\COM. Please
// check the value of your environment variable %CommonProgramFiles% or
// %CommonProgramFiles(x86)% respectively and substitute it into the include path.
// Do the same for PDX folder.
// The path to the assemblies should point to the GAC.
// For example: C:\Windows\Microsoft.NET\assembly\GAC_MSIL\Polytec.IO.Vibrometer\v4.0_2.7.0.0__e9bf5e9b998cc19f.
// A part of the path ($(WinDir)\Microsoft.NET\assembly\GAC_MSIL) is included in the directory definition already.
#pragma warning (push)
#pragma warning (disable : 4192) // disable warning C4192: automatically excluding 'IStorage' while importing type library 'PolyFile.tlb'
#import <PhysicalUnit.dll> no_namespace
#import <WindowFunction.dll> no_namespace
#import <PolyWaveforms.dll> no_namespace
#import <PolyDigitalFilters.dll> no_namespace
#import <CommInterface.dll> no_namespace
#import <PolyFrontEnd.dll> no_namespace
#import <PolyTask.dll> no_namespace
#import <PolySignalGenerator.dll> no_namespace
#import <PolyDigitalFilterDesign.dll> no_namespace
#import <SignalDescription.dll> no_namespace
#import <PolySignal.dll> no_namespace
#import <PDxLib.dll> no_namespace
#import <PolyCamera.dll> no_namespace
#import <PolyScanHead.dll> no_namespace exclude("IComFunction", "IComScheduler", "PTCComTaskStatus", "IComTask", "IComContinuation")
#import <PolyAlignment.dll> no_namespace
#import <PolyBands.dll> no_namespace
#import <PolyMath.dll> no_namespace
#import <PolyScope.dll> no_namespace
#import <PolyDataVisualizer.dll> no_namespace
#import <mscorlib.tlb> no_registry rename("ReportEvent","MSCorLib_ReportEvent")
#import <Polytec.IO.VibInterfaces\v4.0_2.4.0.0__e9bf5e9b998cc19f\Polytec.IO.VibInterfaces.dll> no_namespace exclude("IFilter")
#import <Polytec.IO.Vibrometer\v4.0_4.1.0.0__e9bf5e9b998cc19f\Polytec.IO.Vibrometer.dll> no_namespace exclude("IFilter")
#import <PolyProperties.dll> no_namespace
#import <PolyFile.dll> no_namespace no_function_mapping

#pragma warning (pop)

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_STDAFX_H__0ABE6A97_CF4C_4E3B_A218_A785F0F12DA4__INCLUDED_)
