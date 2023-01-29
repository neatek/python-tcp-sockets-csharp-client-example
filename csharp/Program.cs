//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;
using Microsoft.SqlServer.Server;
using System;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;


namespace csharp
{
    public class TcpCustomClient {

        public TcpClient client = new TcpClient();
        NetworkStream stream;

        int port = 1025;
        string ip = "127.0.0.1";
        int receiveBuffer = 256;

        public TcpCustomClient(string ip, int port)
        {
            this.ip = ip;
            this.port = port;
            new Thread(ConnectionTask).Start();
        }

        public void SendMsg(string msg)
        {
            byte[] data = Encoding.Default.GetBytes(msg);
            using (Socket socket = client.Client)
            {
                socket.Send(data);
            }
        }

        void ConnectionTask()
        {
            while(client.Connected == false)
            {
                Console.WriteLine("[client] ConnectionTask");
                client = new TcpClient();
                try
                {
                    client.Connect(ip, port);
                    Console.WriteLine("[client] connected to " + ip + ":" + port);
                }
                catch (Exception ex)
                {
                    Console.WriteLine(ip + ":" + port + " " + ex.Message);
                }
                if (client.Connected)
                {
                    Console.WriteLine("[client] start receive task");
                    new Thread(ReceiveTask).Start();
                    Console.WriteLine("[client] start send task");
                    new Thread(SendTask).Start();
                    return;
                }
            }
        }

        void ReceiveTask()
        {
            Console.WriteLine("[client] start listening data " + ip + ":" + port);
            while(true)
            {
                if (client == null || !client.Connected)
                {
                    new Thread(ConnectionTask).Start();
                    break;
                }

                stream = client.GetStream();
                if (stream.DataAvailable)
                {
                    byte[] bytes = new byte[receiveBuffer];
                    int bytesRead;
                    string data = "";
                    while ((bytesRead = stream.Read(bytes, 0, bytes.Length)) != 0)
                    {
                        data = Encoding.ASCII.GetString(bytes, 0, bytesRead);
                        Console.WriteLine("[client] received data: " + data);
                    }
                }
            }
            
        }

        void SendTask()
        {
            while (true)
            {
                if (!client.Connected) 
                    continue;

                string input = Console.ReadLine();
                byte[] data = Encoding.Default.GetBytes(input);
                stream.Write(data, 0, data.Length);
            }
        }
    }

    internal class Program
    {
        static void Main(string[] args)
        {
            /*Socket s = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);
            try
            {
                s.ConnectAsync(IPAddress.Parse("127.0.0.1"), 1025);
                Console.Write("Enter some text : ");
                string q = Console.ReadLine();
                byte[] data = Encoding.Default.GetBytes(q);
                s.Send(data);
            }
            catch
            {
            }
            s.Close();*/
            TcpCustomClient s = new TcpCustomClient("127.0.0.1", 1025);
        }
    }
}
