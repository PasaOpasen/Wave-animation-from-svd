// CplxPointAvgDlg.h : header file
//

#if !defined(AFX_CPLXPOINTAVGDLG_H__E685ECC9_01FD_4898_B273_0BAC6CDCC164__INCLUDED_)
#define AFX_CPLXPOINTAVGDLG_H__E685ECC9_01FD_4898_B273_0BAC6CDCC164__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

/////////////////////////////////////////////////////////////////////////////
// CCplxPointAvgDlg dialog

class CCplxPointAvgDlg : public CDialog
{
// Construction
public:
	CCplxPointAvgDlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	//{{AFX_DATA(CCplxPointAvgDlg)
	enum { IDD = IDD_CPLXPOINTAVG_DIALOG };
		// NOTE: the ClassWizard will add data members here
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CCplxPointAvgDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	//{{AFX_MSG(CCplxPointAvgDlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	afx_msg void OnSelectFile();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
private:
	void CalcComplexAverage(IPolyFile11Ptr& spIPolyFile, std::vector<float>& vec_fAvgReal, std::vector<float>& vec_fAvgImag, IDisplay2Ptr& spIDisplayReal, IDisplay2Ptr& spIDisplayImag, IXAxisPtr& spIXAxis);
	void SaveToAscii(IPolyFile11Ptr& spIPolyFile, CString strFileName, std::vector<float>& vec_fAvgReal, std::vector<float>& vec_fAvgImag, IDisplay2Ptr& spIDisplayReal, IDisplay2Ptr& spIDisplayImag, IXAxisPtr& spIXAxis);
	void AddUp(const std::vector<float>& vec_fPoint, std::vector<float>& vec_fAvg);
	void Normalize(std::vector<float>& vec_fAvg, long lNorm);
	template<class T> HRESULT CopySafeArrayToVector(SAFEARRAY* saData, std::vector<T>& vecData, long lStart=0, long lCount=-1)
	{
		if (saData==NULL) return E_POINTER;

		long lLBound=0, lUBound=0;
		HRESULT hr=SafeArrayGetLBound(saData, 1, &lLBound);
		if (FAILED(hr)) return hr;
		hr=SafeArrayGetUBound(saData, 1, &lUBound);
		if (FAILED(hr)) return hr;

		long lDataSize =  (lUBound - lLBound + 1);
		if (lStart > lDataSize || lStart < 0)
			return E_INVALIDARG;
		if (lCount > -1)
		{
			if (lStart + lCount > lDataSize)
				return E_INVALIDARG;
			lDataSize = lCount;
		}

		if (lDataSize > 0)
		{
			vecData.resize(lDataSize);

			T*	pValues;
			hr=SafeArrayAccessData(saData, (void **)&pValues);
			if (FAILED(hr)) return hr;
			std::vector<T>::iterator it = vecData.begin();
			for (long l = lStart; l < lStart + lDataSize; l++, it++)
				*it = pValues[l];
			hr=SafeArrayUnaccessData(saData);
			if (FAILED(hr)) return hr;
		}
		else 
			vecData.clear();

		return S_OK;
	}
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_CPLXPOINTAVGDLG_H__E685ECC9_01FD_4898_B273_0BAC6CDCC164__INCLUDED_)
