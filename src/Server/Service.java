package Server;
import java.net.*;
import java.io.*;
import java.util.concurrent.*;
import java.util.*;

public class Service implements Runnable
{
	private Socket serviceSocket;
	private User user;
	private BlockingQueue<String> messageQueue;
	private Queue<String> pendingUserList;
	
	public Service(Socket serviceSocket) throws SocketException
	{
		this.serviceSocket = serviceSocket;
		this.serviceSocket.setSoTimeout(1000);
		messageQueue = new LinkedBlockingDeque<String>();
		pendingUserList = new LinkedList<String>();
	}
	
	public void sendMsg(OutputStream output, String data) throws IOException 
	{
		output.write(data.getBytes());
	}
	// readUntil delimiter (exclusively)
	public String readUntil(InputStream input, char delimiter, String result, boolean notBlock) throws IOException
	{
		try {
			while(true)
			{
				char tmp = new String(input.readNBytes(1)).charAt(0);
				if (tmp == delimiter)
					break;
				result += tmp;
			}
			return result;
		}
		catch (SocketTimeoutException e)
		{
			if(notBlock)
			{
				if (!result.equals(""))
					return readUntil(input,delimiter,result,notBlock);
				else
					return result;
			}
			else
				return readUntil(input,delimiter,result,notBlock);
		}
	}
	
	private boolean login(String username, String password, InetAddress ip, int port)
	{
		for (User user: Server.userList)
		{
			if (user.isEqual(username, password))
			{
				this.user = user;
				user.setIsOnline(true);
				user.ip = ip;
				user.port = port;
				return true;
			}
		}
		return false;
	}
	
	private boolean register(String username, String password, InetAddress ip, int port)
	{
		for (User user: Server.userList)
		{
			if (user.isEqual(username, password))
				return false;
		}
		User newUser = new User(username,password, ip, port);
		Server.userList.add(newUser);
		this.user = newUser;
		return true;
	}
	
	private void addFriend(String sender, String recipient)
	{
		for (Service service: Server.serviceList)
		{
			if (service.user.getUsername().equals(recipient))
			{
				service.messageQueue.add("FRIEND REQUEST\n" + sender + "\n");
				break;
			}
		} 
	}
	
	private void chatRequest(String sender, String recipient)
	{
		for (Service service: Server.serviceList)
		{
			if (service.user.getUsername().equals(recipient))
			{
				service.messageQueue.add("CHAT REQUEST\n" + sender + "\n");
				break;
			}
		} 
	}
	
	@Override
	public void run()
	{
		try 
		{
			InputStream input = this.serviceSocket.getInputStream();
			OutputStream output = this.serviceSocket.getOutputStream();
			InetAddress ip = this.serviceSocket.getInetAddress();
			int port = this.serviceSocket.getPort();
			while(true)
			{
				String msg;
				try 
				{
					msg = this.messageQueue.poll(100,TimeUnit.MILLISECONDS);
				}
				catch (InterruptedException e) { msg = null; }
				
				if (msg != null)
				{
					String sender = msg.split("\n")[1];
					this.pendingUserList.add(sender);
					sendMsg(output, msg);
				}
				
				String header = readUntil(input,'\n',new String(""),true);
				String username, password;
				switch(header)
				{
				case "":
					break;
				case "LOGIN":
					username = readUntil(input,'\n',new String(""),false);
					password = readUntil(input,'\n',new String(""),false);
					System.out.println("[DEBUG] Login " + username + " " + password);
					if (login(username,password,ip,port))
						sendMsg(output, "LOGIN SUCESSFUL\n");
					else 
						sendMsg(output, "LOGIN FAILED\n");
					break;
				case "REGISTER":
					username = readUntil(input,'\n',new String(""),false);
					password = readUntil(input,'\n',new String(""),false);
					System.out.println("[DEBUG] Register " + username + " " + password);
					if (register(username,password,ip,port))
						sendMsg(output, "REGISTER SUCESSFUL\n");
					else 
						sendMsg(output, "REGISTER FAILED\n");
					break;
				case "SHOW FRIEND":
					String response = "FRIEND STATUS\n" + user.friendList.size() + "\n";
					for (User friend: user.friendList)
					{
						if (friend.getIsOnline())
							response += friend.getUsername() + ": online\n";
						else
							response += friend.getUsername() + ": offline\n";
					}
					sendMsg(output, response);
					break;
				case "ADD FRIEND":
					username = readUntil(input, '\n',new String(""),false);
					System.out.println("[DEBUG] Add friend " + username);
					for (User user: Server.userList)
					{
						if (user.getUsername().equals(username) && !user.getUsername().contentEquals(this.user.getUsername()))
						{
							if (!user.getIsOnline())
								break;
							addFriend(this.user.getUsername(),username);
							break;
						}
					}
					break;
				case "FRIEND REQUEST ACCEPTED":
					username = pendingUserList.remove();
					for (User user: Server.userList)
					{
						if (username.equals(user.getUsername()))			
						{
							user.friendList.add(this.user);
							this.user.friendList.add(user);
							break;
						}
					}
				case "FRIEND REQUEST REJECTED":
					break;
				case "CHAT":
					username = readUntil(input, '\n',new String(""),false);
					int port_;
					try 
					{
						port_ = Integer.parseInt(readUntil(input, '\n',new String(""),false));
						this.user.port = port_;
					}
					catch (NumberFormatException e)
					{
						System.out.println("[CRITICAL] Malicious client message");
						break;
					}
					System.out.println("[DEBUG] Chat " + username + " " + port_);
					boolean find = false;
					for (User user: this.user.friendList)
					{
						if (username.equals(user.getUsername()) && !username.equals(this.user.getUsername()))
						{
							if (!user.getIsOnline())
							{
								sendMsg(output, "CHAT NOT AVAILABLE\n");
								break;
							}
							chatRequest(this.user.getUsername(),username);
							find = true;
							break;
						}
					}
					if (!find)
						sendMsg(output, "CHAT NOT AVAILABLE\n");
					break;
				case "CHAT REQUEST REJECTED":
					username = pendingUserList.remove();
					for (Service service: Server.serviceList)
					{
						if (username.equals(service.user.getUsername()))
						{
							service.messageQueue.add("CHAT REJECTED\n");
							break;
						}
					}
					break;
				case "CHAT REQUEST ACCEPTED":
					username = pendingUserList.remove();	
					for (Service service: Server.serviceList)
					{
						if (username.equals(service.user.getUsername()))
						{
							service.messageQueue.add("CHAT INFO\n" + this.user.ip.toString().split("/")[1] + ":" + this.user.port + ":1\n");
							sendMsg(output,"CHAT INFO\n" + service.user.ip.toString().split("/")[1] + ":" + service.user.port + ":0\n");
							break;
						}
					}
					break;
				default:
					System.out.println("[INFO] Invalid message from" + this.serviceSocket.getInetAddress() + " " + header);
				}
			}
		}
		catch (IOException e)
		{
			System.out.println("[INFO] Connection closed " + this.serviceSocket.getInetAddress());
			try 
			{
				this.serviceSocket.close();
			}
			catch (IOException ex) {}
		}
		catch (NoSuchElementException e)
		{
			System.out.println("[CRITICAL] Malicious client message from " + this.serviceSocket.getInetAddress());
			try 
			{
				this.serviceSocket.close();
			}
			catch (IOException ex) {}
		}
		this.user.setIsOnline(false);
		Server.serviceList.remove(this);
	}
}