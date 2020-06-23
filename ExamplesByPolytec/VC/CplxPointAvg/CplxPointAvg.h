// CplxPointAvg.h : main header file for the CPLXPOINTAVG application
//

#if !defined(AFX_CPLXPOINTAVG_H__8AB22419_4652_4DD5_97A5_B93F8C494DA9__INCLUDED_)
#define AFX_CPLXPOINTAVG_H__8AB22419_4652_4DD5_97A5_B93F8C494DA9__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"		// main symbols

/////////////////////////////////////////////////////////////////////////////
// CCplxPointAvgApp:
// See CplxPointAvg.cpp for the implementation of this class
//

class CCplxPointAvgApp : public CWinApp
{
public:
	CCplxPointAvgApp();

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CCplxPointAvgApp)
	public:
	virtual BOOL InitInstance();
	virtual int ExitInstance();
	//}}AFX_VIRTUAL

// Implementation

	//{{AFX_MSG(CCplxPointAvgApp)
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_CPLXPOINTAVG_H__8AB22419_4652_4DD5_97A5_B93F8C494DA9__INCLUDED_)
