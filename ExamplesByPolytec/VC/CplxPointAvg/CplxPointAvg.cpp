// CplxPointAvg.cpp : Defines the class behaviors for the application.
//

#include "stdafx.h"
#include "CplxPointAvg.h"
#include "CplxPointAvgDlg.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
#define THIS_FILE __FILE__
#endif

/////////////////////////////////////////////////////////////////////////////
// CCplxPointAvgApp

BEGIN_MESSAGE_MAP(CCplxPointAvgApp, CWinApp)
	//{{AFX_MSG_MAP(CCplxPointAvgApp)
		// NOTE - the ClassWizard will add and remove mapping macros here.
		//    DO NOT EDIT what you see in these blocks of generated code!
	//}}AFX_MSG
	ON_COMMAND(ID_HELP, CWinApp::OnHelp)
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CCplxPointAvgApp construction

CCplxPointAvgApp::CCplxPointAvgApp()
{
	// TODO: add construction code here,
	// Place all significant initialization in InitInstance
}

/////////////////////////////////////////////////////////////////////////////
// The one and only CCplxPointAvgApp object

CCplxPointAvgApp theApp;

/////////////////////////////////////////////////////////////////////////////
// CCplxPointAvgApp initialization

BOOL CCplxPointAvgApp::InitInstance()
{
	AfxEnableControlContainer();

	// Standard initialization
	// If you are not using these features and wish to reduce the size
	//  of your final executable, you should remove from the following
	//  the specific initialization routines you do not need.

	// initialize COM
	VERIFY(SUCCEEDED(CoInitialize(NULL)));

	CCplxPointAvgDlg dlg;
	m_pMainWnd = &dlg;
	int nResponse = dlg.DoModal();
	if (nResponse == IDOK)
	{
		// TODO: Place code here to handle when the dialog is
		//  dismissed with OK
	}
	else if (nResponse == IDCANCEL)
	{
		// TODO: Place code here to handle when the dialog is
		//  dismissed with Cancel
	}

	// Since the dialog has been closed, return FALSE so that we exit the
	//  application, rather than start the application's message pump.
	return FALSE;
} // InitInstance()

int CCplxPointAvgApp::ExitInstance()
{
	// uninitialize COM
	CoUninitialize();

	return CWinApp::ExitInstance();
} // ExitInstance()
