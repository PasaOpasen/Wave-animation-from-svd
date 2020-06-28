using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using МатКлассы;
using System.Diagnostics;

namespace Svd_to_animation
{
    public partial class Form1 : Form
    {
        public Form1()
        {
            InitializeComponent();
            InitFolder();

            button3.Hide();
            radioButton1.Hide();
            radioButton2.Hide();

            toolStrip1.Hide();
            toolStripLabel1.Text = "Выберите нужные директории";

            //new ScrollForm(@"D:\svd_to_animation\Results\Scan_time_10-30_area_hann7_143kHz",false).Show();
            new CutForm(new NetOnDouble(0.1, 0.5, 60), 12, 56, new NetOnDouble(-0.5,0.5,100),10,90,new NetOnDouble(0,999,1000),100,-1).Show();
        }

        public string storageDirectoryFile = "StorageDirectory.txt";
        
        public void InitFolder()
        {

            if (File.Exists(storageDirectoryFile))
            {
                var dir = Expendator.GetWordFromFile(storageDirectoryFile);

                if (Directory.Exists(dir))
                    textBox1.Text = dir;
                else
                {
                    MessageBox.Show($"Директория {dir} из файла {storageDirectoryFile} не существует. Используется базовая директория", "Нет указанной директории", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                    textBox1.Text = Environment.CurrentDirectory;
                }
            }
            else
            {
                textBox1.Text = Environment.CurrentDirectory;
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            using (FolderBrowserDialog folderDlg = new FolderBrowserDialog())
            {
                folderDlg.ShowNewFolderButton = true;
                DialogResult result = folderDlg.ShowDialog();

                if (result == DialogResult.OK)
                {
                    textBox1.Text = folderDlg.SelectedPath;
                    Expendator.WriteStringInFile(Path.Combine(Environment.CurrentDirectory, storageDirectoryFile), textBox1.Text);
                }
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            string init = "c:\\";
            if(textBox2.Text != "")
            {
                init = Path.GetDirectoryName(textBox2.Text);
            }

            using (OpenFileDialog openFileDialog = new OpenFileDialog())
            {
                openFileDialog.InitialDirectory = init;
                openFileDialog.Filter = "svd files (*.svd)|*.svd";
                openFileDialog.FilterIndex = 2;
                openFileDialog.RestoreDirectory = true;

                if (openFileDialog.ShowDialog() == DialogResult.OK)
                {
                    //Get the path of specified file
                    textBox2.Text = openFileDialog.FileName;
                    button3.Show();
                    radioButton1.Show();
                    radioButton2.Show();
                }
            }

            toolStripLabel1.Text = "Теперь можно запускать процесс";
        }



        private void CopyResourses(string to)
        {
            string[] pyfiles = { "create.py", "heatmap.py", "get_data_from_file.py" };

            foreach (var f in pyfiles)
                File.Copy(f, Path.Combine(to, f), true);
        }

        private void button3_Click(object sender, EventArgs e)
        {
            if (!Directory.Exists(textBox1.Text))
            {
                try
                {
                    Directory.CreateDirectory(textBox1.Text);
                }
                catch
                {
                    MessageBox.Show("Не получилось создать указанную папку! Выберите другую", "Ошибка с папкой", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    return;
                }
                Expendator.WriteStringInFile(Path.Combine(Environment.CurrentDirectory, storageDirectoryFile), textBox1.Text);
            }

            string newFolder = Path.Combine(textBox1.Text, Path.GetFileNameWithoutExtension(textBox2.Text));
            if(!Directory.Exists(newFolder))
                Directory.CreateDirectory(newFolder);
            CopyResourses(newFolder);

            Expendator.WriteStringInFile(Path.Combine(newFolder, "path.txt"), textBox2.Text);

            if (File.Exists(Path.Combine(newFolder, "times.txt")))
            {
                var res = MessageBox.Show("В целевой папке обнаружены файлы с рисунками. Открыть их или запустить вычисления для создания новых файлов? ДА значит ОТКРЫТЬ", "Выполнять вычисления?", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
                if(res == DialogResult.Yes)
                {
                    new ScrollForm(newFolder, radioButton1.Checked).Show();
                    this.WindowState = FormWindowState.Minimized;
                    return;
                }
            }

            this.Hide();

            StartProcess(Path.Combine(newFolder, "create.py"), () => {

                System.Media.SoundPlayer player = new System.Media.SoundPlayer(Properties.Resources.end);
                player.Play();
               

                new ScrollForm(newFolder, radioButton1.Checked).Show();

                this.WindowState = FormWindowState.Minimized;
                this.Show();
            });
        }
         
        private void StartProcess(string fileName, Action act)
        {
            Process process = new Process();
            process.StartInfo.FileName = fileName;
            process.EnableRaisingEvents = true;
            process.StartInfo.UseShellExecute = true;
            process.StartInfo.Arguments = "py.exe";

            process.Exited += (sender, e) => act();
            process.Start();

            //Process.Start(@"cmd.exe ", @$"py.exe {fileName}");

            process.WaitForExit();

        }






        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void label1_Click(object sender, EventArgs e)
        {
            //System.Diagnostics.Process.Start("https://github.com/PasaOpasen/Wave-animation-from-svd");
            System.Diagnostics.Process.Start("cmd", "/C start https://github.com/PasaOpasen/Wave-animation-from-svd");
        }
    }
}
