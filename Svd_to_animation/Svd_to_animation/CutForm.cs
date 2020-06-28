using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using МатКлассы;

namespace Svd_to_animation
{
    public partial class CutForm : Form
    {
        public CutForm(NetOnDouble X, int xi1, int xi2)
        {
            InitializeComponent();
            x = X.Array.Select(t=>Math.Round(t,5)).ToArray();

            trackBar1.Minimum = 0;
            trackBar1.Maximum = x.Length - maxstep;
            trackBar1.Value = xi1 < 0 ? 0 : xi1;

            trackBar2.Minimum = maxstep;
            trackBar2.Maximum = x.Length;
            trackBar2.Value = xi2 < 0 ? x.Length : xi2;

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
        }

        double[] x, y, t;
        int maxstep = 3;
    }
}
