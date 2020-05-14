package Server;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import java.security.*;
import java.security.spec.*;
import java.net.*;
import java.util.concurrent.*;
import java.util.*;

public class User {
	private String username;
	byte[] passwordHash;
	public BlockingQueue<User> friendList;
	private boolean isOnline;
	public int port;
	public InetAddress ip;
	private byte[] salt;
	
	private byte[] hashPassword(String password)
	{
		KeySpec spec = new PBEKeySpec(password.toCharArray(), salt, 65536, 128);
		try
		{
			SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA1");
			return factory.generateSecret(spec).getEncoded();
		}
		catch (NoSuchAlgorithmException e) {return null;}
		catch (InvalidKeySpecException e) {return null;}
	}
	
	public User(String username, String password, InetAddress ip, int port)
	{
		SecureRandom random = new SecureRandom();
		this.salt = new byte[16];
		random.nextBytes(this.salt);
		
		this.username = username;
		this.passwordHash = hashPassword(password);
		this.friendList = new LinkedBlockingDeque<User>();
		this.isOnline = true;	 // a newly created user is online immediately
		this.ip = ip;
		this.port = port;
	}
	
	public boolean isEqual(String username, String password)
	{
		if (this.username.equals(username) && Arrays.equals(this.passwordHash,hashPassword(password)))
			return true;
		return false;
	}
	
	public String getUsername() { return this.username; }
	public boolean getIsOnline() { return this.isOnline; }
	public void setIsOnline(boolean online) { this.isOnline = online; }
}