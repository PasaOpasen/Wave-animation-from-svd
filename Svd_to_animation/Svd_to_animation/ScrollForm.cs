using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using System.Windows.Forms;
using МатКлассы;

namespace Svd_to_animation
{
    public partial class ScrollForm : Form
    {
        public ScrollForm(string folder)
        {
            InitializeComponent();
            GetParams(folder);

            trackBar1.ValueChanged += (o, e) =>
              {
                  label1.Text = $"time is {vals[trackBar1.Value]}";
                  pictureBox1.BackgroundImage = bitmaps[trackBar1.Value];
              };

            timer1.Interval = 40;
            timer1.Tick += (o, e) =>
            {
                int val = trackBar1.Value;
                if (val == trackBar1.Maximum)
                    trackBar1.Value = trackBar1.Minimum;
                else
                    trackBar1.Value = val + 1;
            };
        }

        private string[] st;
        private double[] vals;
        private Bitmap[] bitmaps;
        private bool shouldRun = false;

        private void GetParams(string folder)
        {
            st = Expendator.GetStringArrayFromFile(Path.Combine(folder, "times.txt"));

            double val(string s) => Path.GetFileNameWithoutExtension(s).Split().Last().ToDouble();

            vals = st.Select(s => val(s)).ToArray();

            trackBar1.Minimum = 0;
            trackBar1.Maximum = st.Length - 1;

            bitmaps = new Bitmap[st.Length];
            for (int i = 0; i < st.Length; i++)
                bitmaps[i] = new Bitmap(Path.Combine(folder, st[i]));

            pictureBox1.BackgroundImage = bitmaps[0];
        }






        private void ScrollForm_Load(object sender, EventArgs e)
        {

        }

        private  void button1_Click(object sender, EventArgs e)
        {
            shouldRun = !shouldRun;
            if (shouldRun)
            {
                timer1.Start();
                button1.Text = "Stop";
            }
            else
            {
                button1.Text = "Auto Run";
                timer1.Stop();
            }
        
        }

        private void numericUpDown1_ValueChanged(object sender, EventArgs e)
        {
            timer1.Interval = numericUpDown1.Value.ToInt32();
        }
    }
}
