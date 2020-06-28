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

        public ScrollForm(string folder, bool wanna_speed = true)
        {
            InitializeComponent();

            this.folder = folder;

            if(!File.Exists(Path.Combine(folder,"space.txt")))
               button2.Hide();

            get_image = i =>
            {
                if (i % 10 == 0)
                    GC.Collect();

                return new Bitmap(Path.Combine(folder, st[i]));
            };
            if (wanna_speed)
                get_image = i => bitmaps[i];


            GetParams(folder, wanna_speed);


            trackBar1.ValueChanged += (o, e) =>
              {
                  label1.Text = $"time is {vals[trackBar1.Value]}";
                  pictureBox1.BackgroundImage = get_image(trackBar1.Value);
              };
            trackBar2.ValueChanged += (o, e) =>
            {
                if (trackBar2.Value <= trackBar3.Value)
                    trackBar2.Value = trackBar3.Value + 1;

                right = trackBar2.Value;
                label4.Text = $"{vals[trackBar2.Value]}";
            };
            trackBar3.ValueChanged += (o, e) =>
            {
                if (trackBar3.Value >= trackBar2.Value)
                    trackBar3.Value = trackBar2.Value - 1;

                left = trackBar3.Value;
                label3.Text = $"{vals[trackBar3.Value]}";
            };

            trackBar2.Value = right;
            trackBar3.Value = 1; trackBar3.Value = 0;

            timer1.Interval = 40;
            timer1.Tick += (o, e) =>
            {
                int val = trackBar1.Value;
                if (val >= right)
                    trackBar1.Value = left;
                else
                    trackBar1.Value = val + 1;
            };

            numericUpDown1.Value = 30;
            numericUpDown1.Minimum = 10;
            numericUpDown1.Maximum = 700;
            numericUpDown1.Increment = 50;

        }

        private string[] st;
        private double[] vals;
        private Bitmap[] bitmaps;
        private bool shouldRun = false;
        private Func<int, Image> get_image;
        private int left, right;
        private string folder;

        private void GetParams(string folder, bool wanna_speed)
        {
            st = Expendator.GetStringArrayFromFile(Path.Combine(folder, "times.txt"));

            double val(string s) => Path.GetFileNameWithoutExtension(s).Split().Last().ToDouble();

            vals = st.Select(s => val(s)).ToArray();

            trackBar1.Minimum = 0;
            trackBar1.Maximum = st.Length - 1;
            trackBar2.Minimum = 0;
            trackBar2.Maximum = st.Length - 1;
            trackBar3.Minimum = 0;
            trackBar3.Maximum = st.Length - 1;
            left = 0;
            right = st.Length - 1;



            if (wanna_speed)
            {
                bitmaps = new Bitmap[st.Length];
                for (int i = 0; i < st.Length; i++)
                    bitmaps[i] = new Bitmap(Path.Combine(folder, st[i]));

            }

            pictureBox1.BackgroundImage = get_image(0);
        }






        private void ScrollForm_Load(object sender, EventArgs e)
        {

        }

        private void button1_Click(object sender, EventArgs e)
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

        private void button2_Click(object sender, EventArgs e)
        {
            new CutForm(this.folder,this).Show();
        }

        private void numericUpDown1_ValueChanged(object sender, EventArgs e)
        {
            timer1.Interval = numericUpDown1.Value.ToInt32();
        }
    }
}
