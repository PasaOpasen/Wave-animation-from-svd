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

            toolStrip1.Hide();
            toolStripLabel1.Text = "Выберите нужные директории";

            new ScrollForm(@"D:\svd_to_animation\Results\Scan_time_10-30_area_hann7_143kHz").Show();
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


            this.Hide();

            StartProcess(Path.Combine(newFolder, "create.py"), () => {

                System.Media.SoundPlayer player = new System.Media.SoundPlayer(Properties.Resources.end);
                player.Play();
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
    }
}
