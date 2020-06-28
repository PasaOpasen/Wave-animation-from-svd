using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using System.IO;
using МатКлассы;

namespace Svd_to_animation
{
    public partial class CutForm : Form
    {
        public CutForm(string folder, ScrollForm f)
        {
            InitializeComponent();

            var arr = Expendator.GetWordFromFile(Path.Combine(folder, "space.txt")).Replace('.', ',').ToDoubleMas();

            x = new NetOnDouble(arr[0],arr[1],(int)arr[2]).Array.Select(tc=>Math.Round(tc,5)).ToArray();
            y = new NetOnDouble(arr[3], arr[4], (int)arr[5]).Array.Select(tc => Math.Round(tc, 5)).ToArray();
            t = new NetOnDouble(arr[6], arr[7], (int)arr[8]).Array.Select(tc => Math.Round(tc, 5)).ToArray();

            this.par = Path.Combine(folder, "params.txt");
            this.folder = folder;

            if (File.Exists(par))
            {
                arr = Expendator.GetWordFromFile(par).Replace('.',',').ToDoubleMas();
                FillTracks(arr[0].ToInt(), arr[1].ToInt(), arr[2].ToInt(), arr[3].ToInt(), arr[4].ToInt(), arr[5].ToInt());
            }
            else
            FillTracks();

            
        }

        double[] x, y, t;
        int maxstep = 3;
        string folder, par;
        ScrollForm f;

        private void FillTracks(int xi1=-1, int xi2=-1, int yi1=-1, int yi2=-1, int ti1=-1, int ti2=2)
        {

            trackBar1.ValueChanged += (o, e) =>
            {
                if (trackBar1.Value + maxstep > trackBar2.Value)
                    trackBar1.Value = trackBar2.Value - maxstep;

                label1.Text = $"xmin = {x[trackBar1.Value]}";
                groupBox1.Text = $"X-axis (total: {trackBar2.Value - trackBar1.Value + 1})";
            };
            trackBar2.ValueChanged += (o, e) =>
            {
                if (trackBar2.Value - maxstep < trackBar1.Value)
                    trackBar2.Value = trackBar1.Value + maxstep;

                label2.Text = $"xmax = {x[trackBar2.Value]}";
                groupBox1.Text = $"X-axis (total: {trackBar2.Value - trackBar1.Value + 1})";
            };

            trackBar1.Minimum = 0;
            trackBar1.Maximum = x.Length - maxstep;
            trackBar1.Value = xi1 < 0 ? 0 : xi1;

            trackBar2.Minimum = maxstep;
            trackBar2.Maximum = x.Length-1;
            trackBar2.Value = xi2 < 0 ? x.Length : xi2;


 trackBar3.ValueChanged += (o, e) =>
            {
                if (trackBar3.Value + maxstep > trackBar4.Value)
                    trackBar3.Value = trackBar4.Value - maxstep;

                label3.Text = $"ymin = {y[trackBar3.Value]}";
                groupBox2.Text = $"Y-axis (total: {trackBar4.Value - trackBar3.Value + 1})";
            };
            trackBar4.ValueChanged += (o, e) =>
            {
                if (trackBar4.Value - maxstep < trackBar3.Value)
                    trackBar4.Value = trackBar3.Value + maxstep;

                label4.Text = $"ymax = {y[trackBar4.Value]}";
                groupBox2.Text = $"Y-axis (total: {trackBar4.Value - trackBar3.Value + 1})";
            };


            trackBar3.Minimum = 0;
            trackBar3.Maximum = y.Length - maxstep;
            trackBar3.Value = yi1 < 0 ? 0 : yi1;

            trackBar4.Minimum = maxstep;
            trackBar4.Maximum = y.Length-1;
            trackBar4.Value = yi2 < 0 ? y.Length : yi2;

           


trackBar5.ValueChanged += (o, e) =>
            {
                if (trackBar5.Value + maxstep > trackBar6.Value)
                    trackBar5.Value = trackBar6.Value - maxstep;

                label5.Text = $"tmin = {t[trackBar5.Value]}";
                groupBox3.Text = $"Time-axis (total: {trackBar6.Value - trackBar5.Value + 1})";
            };
            trackBar6.ValueChanged += (o, e) =>
            {
                if (trackBar6.Value - maxstep < trackBar5.Value)
                    trackBar6.Value = trackBar5.Value + maxstep;

                label6.Text = $"tmax = {t[trackBar6.Value]}";
                groupBox3.Text = $"Time-axis (total: {trackBar6.Value - trackBar5.Value + 1})";
            };

            trackBar5.Minimum = 0;
            trackBar5.Maximum = t.Length - maxstep;
            trackBar5.Value = ti1 < 0 ? 0 : ti1;

            trackBar6.Minimum = maxstep;
            trackBar6.Maximum = t.Length-1;
            trackBar6.Value = ti2 < 0 ? t.Length : ti2;

            
        }
    }
}
