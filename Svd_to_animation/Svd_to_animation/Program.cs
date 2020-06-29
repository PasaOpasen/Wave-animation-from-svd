using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Diagnostics;

namespace Svd_to_animation
{
    static class Program
    {
        /// <summary>
        ///  The main entry point for the application.
        /// </summary>
        [STAThread]
        static void Main()
        {
            Application.SetHighDpiMode(HighDpiMode.SystemAware);
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }

        public static void StartProcess(string fileName, Action act, string args="")
        {
            //Process process = new Process();
            //process.StartInfo.FileName = fileName;
            //process.EnableRaisingEvents = true;
            //process.StartInfo.UseShellExecute = true;
            //process.StartInfo.Arguments = $"python.exe";

           // var starinfo = new ProcessStartInfo("python.exe");
            //starinfo.Arguments = $"{fileName} {args}";

            Process process = new Process();
            process.StartInfo.FileName = fileName;
            process.EnableRaisingEvents = true;
            process.StartInfo.UseShellExecute = true;
            process.StartInfo.Arguments = $"{args}";

            process.Exited += (sender, e) => act();
            process.Start();

            //Process.Start(@"cmd.exe ", @$"py.exe {fileName}");

            process.WaitForExit();

        }
    }
}
