package Server;
import java.net.*;
import java.io.*;
import java.util.concurrent.*;
import java.util.ArrayList;

public class Server {
	private static int port = 6969;
	private static int numThreads = 10;
	private static ServerSocket serverSocket = null;
	private static ArrayList<Service> serviceList = new ArrayList<Service>();
	
	
	public static void main(String[] argv){
		System.out.println("[SERVER] Start");
		ExecutorService pool = Executors.newFixedThreadPool(Server.numThreads);
		try{
			serverSocket = new ServerSocket(Server.port);
			while(true){
				 Socket clientSocket = serverSocket.accept();
				 System.out.println("[SERVER] New client " + clientSocket.getInetAddress());
				 Service service = new Service(clientSocket);
				 serviceList.add(service);
				 pool.submit(service);
			}
		}
		catch (IOException e){
			if (serverSocket != null) {
				try {
					serverSocket.close();
				}
				catch (IOException ex) {}
			}
		}
	}
}