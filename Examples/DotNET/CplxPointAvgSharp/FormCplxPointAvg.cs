using System;
using System.Drawing;
using System.Collections;
using System.ComponentModel;
using System.Windows.Forms;
using System.Data;
using System.Runtime.InteropServices; // needed for System Menu
using Polytec.Interop.PolyFile;
using Polytec.Interop.PolySignal;
using Polytec.Interop.PolyProperties;

namespace CplxPointAvgSharp
{
	/// <summary>
	/// Summary description for Form1.
	/// </summary>
	public class FormCplxPointAvg : System.Windows.Forms.Form
	{
		private System.Windows.Forms.Button SelectFile;
		private System.Windows.Forms.Button End;
		private System.Windows.Forms.Label labelExplain;
		/// <summary>
		/// Required designer variable.
		/// </summary>
		private System.ComponentModel.Container components = null;

		public FormCplxPointAvg()
		{
			//
			// Required for Windows Form Designer support
			//
			InitializeComponent();

			//
			// New System Menu
			//
			this.SetupSystemMenu();
		}

		/// <summary>
		/// Clean up any resources being used.
		/// </summary>
		protected override void Dispose(bool disposing)
		{
			if (disposing)
			{
				if (components != null)
				{
					components.Dispose();
				}
			}
			base.Dispose(disposing);
		}

		#region Windows Form Designer generated code
		/// <summary>
		/// Required method for Designer support - do not modify
		/// the contents of this method with the code editor.
		/// </summary>
		private void InitializeComponent()
		{
			System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(FormCplxPointAvg));
			this.labelExplain = new System.Windows.Forms.Label();
			this.End = new System.Windows.Forms.Button();
			this.SelectFile = new System.Windows.Forms.Button();
			this.SuspendLayout();
			//
			// labelExplain
			//
			this.labelExplain.Location = new System.Drawing.Point(32, 32);
			this.labelExplain.Name = "labelExplain";
			this.labelExplain.Size = new System.Drawing.Size(320, 56);
			this.labelExplain.TabIndex = 1;
			this.labelExplain.Text = "This application shows how to use Polytec File Access to perform a complex averag" +
	"ing over the FFT spectra of all measurements points of a PSV Scan File.";
			//
			// End
			//
			this.End.Location = new System.Drawing.Point(296, 160);
			this.End.Name = "End";
			this.End.Size = new System.Drawing.Size(72, 24);
			this.End.TabIndex = 2;
			this.End.Text = "Close";
			this.End.Click += new System.EventHandler(this.End_Click);
			//
			// SelectFile
			//
			this.SelectFile.Location = new System.Drawing.Point(32, 96);
			this.SelectFile.Name = "SelectFile";
			this.SelectFile.Size = new System.Drawing.Size(200, 56);
			this.SelectFile.TabIndex = 3;
			this.SelectFile.Text = "Select PSV Scan File...";
			this.SelectFile.Click += new System.EventHandler(this.SelectFile_Click);
			//
			// FormCplxPointAvg
			//
			this.AutoScaleBaseSize = new System.Drawing.Size(5, 13);
			this.ClientSize = new System.Drawing.Size(384, 196);
			this.Controls.Add(this.SelectFile);
			this.Controls.Add(this.End);
			this.Controls.Add(this.labelExplain);
			this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
			this.MaximizeBox = false;
			this.MinimizeBox = false;
			this.Name = "FormCplxPointAvg";
			this.Text = "Complex Point Average - Polytec File Access DEMO";
			this.ResumeLayout(false);

		}
		#endregion

		[DllImport("user32.dll")]
		private static extern int GetSystemMenu(int hwnd, int bRevert);

		[DllImport("user32.dll")]
		private static extern int AppendMenu(
			int hMenu, int Flagsw, int IDNewItem, string lpNewItem);

		private enum SystemMenuIDs
		{
			About = 1234,
		}

		private enum MenuFlags
		{
			Separator = 0xa00
		}

		/// <summary>
		/// adds an About item to the Windows System Menu
		/// </summary>
		private void SetupSystemMenu()
		{
			// get handle to system menu
			int menu = GetSystemMenu(this.Handle.ToInt32(), 0);
			// add a separator
			AppendMenu(menu, (int)MenuFlags.Separator, 0, null);
			// add an item with a unique ID
			AppendMenu(menu, 0, (int)SystemMenuIDs.About, "About CplxPointAvg...");
		}

		protected override void WndProc(ref Message m)
		{
			base.WndProc(ref m);
			const int WM_SYSCOMMAND = 0x112;
			if (m.Msg == WM_SYSCOMMAND)
			{
				// check for my new menu item ID
				if (m.WParam.ToInt32() == (int)SystemMenuIDs.About)
				{
					// show About box here...
					About aboutDlg = new About();
					aboutDlg.ShowDialog();
				}
			}
		}

		/// <summary>
		/// The main entry point for the application.
		/// </summary>
		[STAThread]
		static void Main()
		{
			Application.Run(new FormCplxPointAvg());
		}

		/// <summary>
		/// This function is called when the 'Select PSV File...' Button is pressed on the dialog.
		/// Asks for a PSV filename, instantiates a PolyFile object, does the average calculations,
		/// asks for a save file name and saves the average data to an Ascii file.
		/// </summary>
		/// <param name="sender">unused</param>
		/// <param name="eventArgs">unused</param>
		private void SelectFile_Click(object sender, System.EventArgs eventArgs)
		{
			OpenFileDialog openFileDialog = new OpenFileDialog();
			openFileDialog.Filter = "ScanFiles (*.svd)|*.svd|Single Point Files (*.pvd)|*.pvd|PSV Files (*.svd; *.pvd)|*.svd; *.pvd|All files (*.*)|*.*";
			openFileDialog.FilterIndex = 1;
			openFileDialog.RestoreDirectory = true;

			if (openFileDialog.ShowDialog() == DialogResult.Cancel)
				return;

			// from here on catch all COM-errors that are generated by PolyFile
			PolyFileClass file = null;
			try
			{
				// create instance of PolyFile COM object
				file = new PolyFileClass();

				file.Open(openFileDialog.FileName);
				// get and check file type - we accept VibSoft and PSV files
				// VibSoft files have only a single point so the averaging has demonstration purposes only.
				PTCFileID fileID = file.Version.FileID;
				switch (fileID)
				{
					case PTCFileID.ptcFileIDCombinedFile:
					case PTCFileID.ptcFileIDPSVFile:
					case PTCFileID.ptcFileIDVibSoftFile:
						break;
					default:
						string msg = openFileDialog.FileName + (" is not an VibSoft or PSV file");
						MessageBox.Show(msg, "File Error", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
						return;
				}

				// provide access to the acquisition properties
				AcquisitionInfoModes acqInfoModes = file.Infos.AcquisitionInfoModes;

				// check the acquisition mode - should be FFT
				PTCAcqMode ptcAcqMode = acqInfoModes.ActiveMode;
				if (ptcAcqMode != PTCAcqMode.ptcAcqModeFft)
				{
					MessageBox.Show("Please select a file with acquisition mode FFT", "Wrong Acquisition Mode", MessageBoxButtons.OK, MessageBoxIcon.Exclamation);
					return;
				}

				// hold average data in array for real and imaginary part
				float[] avgReal;
				float[] avgImag;

				// display used will be returned by CalcComplexAverage
				Display displayReal;
				Display displayImag;
				XAxis xaxis;

				CalcComplexAverage(file, out avgReal, out avgImag, out displayReal, out displayImag, out xaxis);

				// select a filename for saving the data
				SaveFileDialog saveFileDialog = new SaveFileDialog();
				saveFileDialog.Filter = "Microsoft Excel (*.xls)|*.xls|Ascii Files (*.txt)|*.txt|All files (*.*)|*.*";
				saveFileDialog.FilterIndex = 2;
				saveFileDialog.RestoreDirectory = true;

				if (saveFileDialog.ShowDialog() == DialogResult.Cancel)
					return;

				SaveToAscii(file, saveFileDialog.FileName, avgReal, avgImag, displayReal, displayImag, xaxis);

				MessageBox.Show("Complex Point Average data has been saved successfully", "Save data", MessageBoxButtons.OK, MessageBoxIcon.Information);
			}
			catch (ArgumentException e)
			{
				MessageBox.Show(e.Message);
			}
			catch (Exception e)
			{
				MessageBox.Show(e.ToString());
			}
			finally
			{
				if (file != null && file.IsOpen)
				{
					try
					{
						file.Close();
					}
					catch (Exception e)
					{
						MessageBox.Show(e.ToString());
					}
				}
			}

		}


		/// <summary>
		/// Calculates the average of the complex data of all measure points.
		/// </summary>
		/// <param name="file">PolyFile Object</param>
		/// <param name="avgReal">averaged data, real part</param>
		/// <param name="avgImag">averaged data, imaginary part</param>
		/// <param name="displayReal">display object for real part</param>
		/// <param name="displayImag">display object for imaginary part</param>
		private void CalcComplexAverage(PolyFileClass file, out float[] avgReal, out float[] avgImag, out Display displayReal, out Display displayImag, out XAxis xaxis)
		{
			this.Cursor = Cursors.WaitCursor;

			avgReal = null;
			avgImag = null;
			displayReal = null;
			displayImag = null;

			try
			{
				PointDomains pointDomains = file.GetPointDomains(PTCSignalBuildFlags.ptcBuildPointDataXYZ);

				// select FFT domain
				PointDomain domain;
				if (!pointDomains.get_Exists(PTCDomainType.ptcDomainSpectrum))
					throw new ArgumentException("The file does not contain a point data domain \"FFT\".");

				domain = pointDomains.get_Type(PTCDomainType.ptcDomainSpectrum);

				string channel;
				if (domain.Channels.get_Exists("Vib"))
					channel = "Vib";
				else if (domain.Channels.get_Exists("Vib X"))
					channel = "Vib X";
				else
					throw new ArgumentException("The file does not contain a channel \"Vib\" or \"Vib X\".");

				if (!domain.Channels[channel].Signals.get_Exists("Velocity"))
					throw new ArgumentException("The file does not contain a signal \"Velocity\".");
				Signal signal = domain.Channels[channel].Signals["Velocity"];
				if (!(signal.Displays.get_Exists("Real") && signal.Displays.get_Exists("Imaginary")))
					throw new ArgumentException("The vibrometer channel of the file does not contain complex data.");

				// construct display objects for real and imaginary part
				displayReal = signal.Displays["Real"];
				displayImag = signal.Displays["Imaginary"];

				xaxis = domain.GetXAxis(displayReal);
				// mark first point because we can use its data directly
				bool firstPoint = true;
				long validPoints = 0;

				// loop over all measurement points
				DataPoint dataPoint;
				DataPoints dataPoints = domain.DataPoints;
				long pointCount = dataPoints.Count;

				for (int point = 1; point <= pointCount; ++point)
				{
					dataPoint = dataPoints[point];
					// check if measurement point is valid - in VibSoft we can't do that because there
					// are no measurement points available for single point files
					bool pointIsValid = true;
					if (PTCFileID.ptcFileIDPSVFile == file.Version.FileID)
					{
						// test valid flag of the point status
						pointIsValid = (PTCScanStatus.ptcScanStatusValid & dataPoint.MeasPoint.ScanStatus) != 0;
					}
					if (!pointIsValid) continue;

					// get the data
					float[] dataReal = (float[])dataPoint.GetData(displayReal, 0);
					float[] dataImag = (float[])dataPoint.GetData(displayImag, 0);

					if (firstPoint)
					{
						avgReal = dataReal;
						avgImag = dataImag;
						firstPoint = false;
					}
					else
					{
						AddUp(dataReal, avgReal);
						AddUp(dataImag, avgImag);
					}

					validPoints++;
				}

				// normalize average to the number of valid points
				if (validPoints > 1)
				{
					Normalize(avgReal, validPoints);
					Normalize(avgImag, validPoints);
				}
			}
			finally
			{
				this.Cursor = Cursors.Default;
			}
		}


		/// <summary>
		/// adds point values to the averaged values
		/// </summary>
		/// <param name="point">point data</param>
		/// <param name="avg">averaged data</param>
		private void AddUp(float[] point, float[] avg)
		{
			if (point.Length != avg.Length)
				throw new ArgumentException("Arrays point and avg must have same length");
			for (int i = 0; i < avg.Length; ++i)
				avg[i] += point[i];
		} // AddUp()


		/// <summary>
		/// normalizes the averaged data
		/// </summary>
		/// <param name="avg">averaged data</param>
		/// <param name="norm">normalization factor</param>
		private void Normalize(float[] avg, long norm)
		{
			for (int i = 0; i < avg.Length; ++i)
			{
				avg[i] /= norm;
			}
		} // Normalize()

		/// <summary>
		/// Writes averaged data to ascii file
		/// </summary>
		/// <param name="file">PolyFile object</param>
		/// <param name="fileName">file path of the ascii file</param>
		/// <param name="avgReal">averaged data, real part</param>
		/// <param name="avgImag">averaged data, imaginary part</param>
		/// <param name="displayReal">display object for real part</param>
		/// <param name="displayImag">display object for imaginary part</param>
		private void SaveToAscii(PolyFileClass file, string fileName, float[] avgReal, float[] avgImag, Display displayReal, Display displayImag, XAxis xaxis)
		{
			this.Cursor = Cursors.WaitCursor;

			// get info for x-axis (frequency axis)
			AcquisitionInfoModes acqInfoModes = file.Infos.AcquisitionInfoModes;
			IAcquisitionProperties acqProps = acqInfoModes.ActiveProperties;

			System.IO.StreamWriter sw = new System.IO.StreamWriter(fileName, false, System.Text.Encoding.Default);

			// write description of signals
			string bstrSignal = displayReal.Signal.Name;
			string bstrChannel = displayReal.Signal.Channel.Name;
			string bstrDomain = displayReal.Signal.Channel.Domain.Name;

			sw.WriteLine("Complex Average over all valid measurement points - Polytec File Access DEMO");
			sw.WriteLine();
			sw.Write("Signal: ");
			sw.Write(bstrDomain);
			sw.Write(" / ");
			sw.Write(bstrChannel);
			sw.Write(" / ");
			sw.WriteLine(bstrSignal);
			sw.WriteLine();
			sw.Write("\t");
			sw.Write(displayReal.Name);
			sw.Write("\t");
			sw.WriteLine(displayImag.Name);

			// write units
			string bstrRealUnit = displayReal.Signal.Description.YAxis.Unit;
			string bstrImagUnit = displayImag.Signal.Description.YAxis.Unit;

			sw.Write("[Hz]\t[");
			sw.Write(bstrRealUnit);
			sw.Write("]\t[");
			sw.Write(bstrImagUnit);
			sw.WriteLine("]");

			// we want to output our floating point numbers in a culture invariant (english) format
			IFormatProvider formatProvider = System.Globalization.CultureInfo.InvariantCulture;

			// write data
			for (int i = 0; i < avgReal.Length; i++)
			{
				double dFreq = xaxis.GetMidX(i);
				sw.Write(dFreq.ToString(formatProvider));
				sw.Write("\t");
				sw.Write(avgReal[i].ToString(formatProvider));
				sw.Write("\t");
				sw.WriteLine(avgImag[i].ToString(formatProvider));
			}

			sw.Close();

			this.Cursor = Cursors.Default;
		}

		private void End_Click(object sender, System.EventArgs e)
		{
			Application.Exit();
		}

	}
}
