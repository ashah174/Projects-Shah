/*
 * Template JAVA User Interface
 * =============================
 *
 * Database Management Systems
 * Department of Computer Science  &  Engineering
 * University of California - Riverside
 *
 * Target DBMS: 'Postgres'
 *
 */


import java.sql.DriverManager;
import java.sql.Connection;
import java.sql.Statement;
import java.sql.ResultSet;
import java.sql.ResultSetMetaData;
import java.sql.SQLException;
import java.io.File;
import java.io.FileReader;
import java.io.BufferedReader;
import java.io.InputStreamReader;

/**
 * This class defines a simple embedded SQL utility class that is designed to
 * work with PostgreSQL JDBC drivers.
 *
 */
public class DBProject {

   // reference to physical database connection.
   private Connection _connection = null;

   // handling the keyboard inputs through a BufferedReader
   // This variable can be global for convenience.
   static BufferedReader in = new BufferedReader(
                                new InputStreamReader(System.in));

   /**
    * Creates a new instance of DBProject
    *
    * @param hostname the MySQL or PostgreSQL server hostname
    * @param database the name of the database
    * @param username the user name used to login to the database
    * @param password the user login password
    * @throws java.sql.SQLException when failed to make a connection.
    */
   public DBProject (String dbname, String dbport, String user, String passwd) throws SQLException {

      System.out.print("Connecting to database...");
      try{
         // constructs the connection URL
         String url = "jdbc:postgresql://localhost:" + dbport + "/" + dbname;
         System.out.println ("Connection URL: " + url + "\n");

         // obtain a physical connection
         this._connection = DriverManager.getConnection(url, user, passwd);
         System.out.println("Done");
      }catch (Exception e){
         System.err.println("Error - Unable to Connect to Database: " + e.getMessage() );
         System.out.println("Make sure you started postgres on this machine");
         System.exit(-1);
      }//end catch
   }//end DBProject

   /**
    * Method to execute an update SQL statement.  Update SQL instructions
    * includes CREATE, INSERT, UPDATE, DELETE, and DROP.
    *
    * @param sql the input SQL string
    * @throws java.sql.SQLException when update failed
    */
   public void executeUpdate (String sql) throws SQLException {
      // creates a statement object
      Statement stmt = this._connection.createStatement ();

      // issues the update instruction
      stmt.executeUpdate (sql);

      // close the instruction
      stmt.close ();
   }//end executeUpdate

   /**
    * Method to execute an input query SQL instruction (i.e. SELECT).  This
    * method issues the query to the DBMS and outputs the results to
    * standard out.
    *
    * @param query the input query string
    * @return the number of rows returned
    * @throws java.sql.SQLException when failed to execute the query
    */
   public int executeQuery (String query) throws SQLException {
      // creates a statement object
      Statement stmt = this._connection.createStatement ();

      // issues the query instruction
      ResultSet rs = stmt.executeQuery (query);

      /*
       ** obtains the metadata object for the returned result set.  The metadata
       ** contains row and column info.
       */
      ResultSetMetaData rsmd = rs.getMetaData ();
      int numCol = rsmd.getColumnCount ();
      int rowCount = 0;

      // iterates through the result set and output them to standard out.
      boolean outputHeader = true;
      while (rs.next()){
	 if(outputHeader){
	    for(int i = 1; i <= numCol; i++){
		System.out.printf("%-10s", rsmd.getColumnName(i) + "\t");
	    }
	    System.out.println();
	    outputHeader = false;
	 }
         for (int i=1; i<=numCol; ++i)
            System.out.printf( "%-10s",rs.getString (i) + "\t");
         System.out.println ();
         ++rowCount;
      }//end while
      stmt.close ();
      return rowCount;
   }//end executeQuery

   /**
    * Method to close the physical connection if it is open.
    */
   public void cleanup(){
      try{
         if (this._connection != null){
            this._connection.close ();
         }//end if
      }catch (SQLException e){
         // ignored.
      }//end try
   }//end cleanup

   /**
    * The main execution method
    *
    * @param args the command line arguments this inclues the <mysql|pgsql> <login file>
    */
   public static void main (String[] args) {
      if (args.length != 3) {
         System.err.println (
            "Usage: " +
            "java [-classpath <classpath>] " +
            DBProject.class.getName () +
            " <dbname> <port> <user>");
         return;
      }//end if
      
      Greeting();
      DBProject esql = null;
      try{
         // use postgres JDBC driver.
         Class.forName ("org.postgresql.Driver").newInstance ();
         // instantiate the DBProject object and creates a physical
         // connection.
         String dbname = args[0];
         String dbport = args[1];
         String user = args[2];
         esql = new DBProject (dbname, dbport, user, "");

         boolean keepon = true;
         while(keepon) {
            // These are sample SQL statements
	    String original = "\u001B[0m";
	    String purple = "\u001B[35m";
				System.out.println(purple +
				"┌──────────────────────────────────────────┐\n" +
				"│               MAIN MENU                  │\n" +
				"└──────────────────────────────────────────┘" + original);
				System.out.println("──────────────────────────────────────────-");
				System.out.println("1. Add New Customer");
				System.out.println("2. Add New Room");
				System.out.println("3. Add New Maintenance Company");
				System.out.println("4. Add New Repair");
				System.out.println("5. Add New Booking"); 
				System.out.println("6. Assign house cleaning staff to a room");
				System.out.println("7. Raise a repair request");
				System.out.println("8. Get number of available rooms");
				System.out.println("9. Get number of booked rooms");
				System.out.println("10. Get hotel bookings for a week");
				System.out.println("11. Get top k rooms with highest price for a date range");
				System.out.println("12. Get top k highest booking price for a customer");
				System.out.println("13. Get customer total cost occurred for a give date range"); 
				System.out.println("14. List the repairs made by maintenance company");
				System.out.println("15. Get top k maintenance companies based on repair count");
				System.out.println("16. Get number of repairs occurred per year for a given hotel room");
				System.out.println("17. < EXIT");

            switch (readChoice()){
				   case 1: addCustomer(esql); break;
				   case 2: addRoom(esql); break;
				   case 3: addMaintenanceCompany(esql); break;
				   case 4: addRepair(esql); break;
				   case 5: bookRoom(esql); break;
				   case 6: assignHouseCleaningToRoom(esql); break;
				   case 7: repairRequest(esql); break;
				   case 8: numberOfAvailableRooms(esql); break;
				   case 9: numberOfBookedRooms(esql); break;
				   case 10: listHotelRoomBookingsForAWeek(esql); break;
				   case 11: topKHighestRoomPriceForADateRange(esql); break;
				   case 12: topKHighestPriceBookingsForACustomer(esql); break;
				   case 13: totalCostForCustomer(esql); break;
				   case 14: listRepairsMade(esql); break;
				   case 15: topKMaintenanceCompany(esql); break;
				   case 16: numberOfRepairsForEachRoomPerYear(esql); break;
				   case 17: keepon = false; break;
				   default : System.out.println("Unrecognized choice!"); break;
            }//end switch
         }//end while
      }catch(Exception e) {
         System.err.println (e.getMessage ());
      }finally{
         // make sure to cleanup the created table and close the connection.
         try{
            if(esql != null) {
               System.out.print("Disconnecting from database...");
               esql.cleanup ();
               System.out.println("Done\n\nBye !");
            }//end if
         }catch (Exception e) {
            // ignored.
         }//end try
      }//end try
   }//end main
   
   public static void Greeting(){
      System.out.println(
         "\n\n*******************************************************\n" +
         "              User Interface      	               \n" +
         "*******************************************************\n");
   }//end Greeting

   /*
    * Reads the users choice given from the keyboard
    * @int
    **/
   public static int readChoice() {
      int input;
      // returns only if a correct value is given.
      do {
         System.out.print("Please make your choice: ");
         try { // read the integer, parse it and break.
            input = Integer.parseInt(in.readLine());
            break;
         }catch (Exception e) {
            System.out.println("Your input is invalid!");
            continue;
         }//end try
      }while (true);
      return input;
   }//end readChoice

    // Error handling: Any empty input
    public static String readNotEmpty(String label) throws Exception{
	    while(true){
		    System.out.print(label);
		    String s = in.readLine().trim();
		    if (!s.isEmpty()) return s;
		    System.out.println("Input can not be empty. Please try again.");
	    }
    }
    public static String readInt(String label) {
        while (true) {
            try {
                System.out.print(label);
                String input = in.readLine().trim();

                // Must be integer (positive or zero)
                if (input.matches("\\d+")) {
                    return input;
                }

                System.out.println("Invalid input. Please enter a number.");
            } catch (Exception e) {
                System.out.println("Error reading input. Please try again.");
            }
        }
    }


   
   public static void addCustomer(DBProject esql){
	  // Given customer details add the customer in the DB 
      try {
	      String id = readInt("Enter customerID: ");
	
	      String fname = readNotEmpty("Enter first name: ");

	      String lname = readNotEmpty("Enter last name: ");
          
	      String address = readNotEmpty("Enter address: ");
          
	      String phone = readInt("Enter phone number: ");
          
	      String dob = readNotEmpty("Enter DOB (YYYY-MM-DD): ");

          String gender = readNotEmpty("Enter gender: ");

	      String query = "INSERT INTO Customer VALUES (" +
                      id + ", '" + fname + "', '" + lname + "', '" + address +
                      "', '" + phone + "', '" + dob + "', '" + gender + "');";
	      esql.executeUpdate(query);
      System.out.println("Customer added successfully.");

      }
      catch (Exception e) {
	      System.err.println(e.getMessage());
      }
   }//end addCustomer

   public static void addRoom(DBProject esql){
	  // Given room details add the room in the DB
      try {
	      String hid = readInt("Enter hotelID: ");
          
	      String roomNo = readInt("Enter room number: ");
          
	      String roomType = readNotEmpty("Enter room type (ex: Single, Double, etc): ");
          
	      String query =
            "INSERT INTO Room(hotelID, roomNo, roomType) " +
            "VALUES (" + hid + ", " + roomNo + ", '" + roomType + "');";

	      esql.executeUpdate(query);
    	      System.out.println("Room added successfully.");
   } catch (Exception e) {
      System.err.println(e.getMessage());
   }
   }//end addRoom

   public static void addMaintenanceCompany(DBProject esql){
      // Given maintenance Company details add the maintenance company in the DB
      try {
      		String cmpID = readInt("Enter company ID: ");
		//String cmpID = in.readLine();

      		String name = readNotEmpty("Enter company name: ");
      		//String name = in.readLine();
		    name = name.replace("'", "''");

      		String address = readNotEmpty("Enter address: ");
      		//String address = in.readLine();
		    address = address.replace("'", "''");

      		System.out.print("Is the company certified? (yes/no): ");
      		String ans = in.readLine();
      		String isCertified = (ans.equalsIgnoreCase("yes") || ans.equalsIgnoreCase("y")) ? "true" : "false";
		
      		String query = "INSERT INTO MaintenanceCompany(cmpID, name, address, isCertified) " +
            "VALUES (" + cmpID + ", '" + name + "', '" + address + "', " + isCertified + ");";

      		esql.executeUpdate(query);
      		System.out.println("Maintenance company added successfully.");
      } catch (Exception e) {
      System.err.println(e.getMessage());
   }
   }//end addMaintenanceCompany

   public static void addRepair(DBProject esql){
	  // Given repair details add repair in the DB
	try {
		String rid = readInt("Enter repair ID: ");
		//String rid = in.readLine();

        String hid = readInt("Enter hotelID: ");
      		//String hid = in.readLine();

        String roomNo = readInt("Enter room number: ");
      		//String roomNo = in.readLine();

        String cmpID = readInt("Enter maintenance company ID: ");
      		//String cmpID = in.readLine();

        String date = readNotEmpty("Enter repair date (MM/DD/YYYY): ");
      		//String date = in.readLine();

      		System.out.print("Enter description: ");
      		String desc = in.readLine();

      		System.out.print("Enter repair type (e.g., ELECTRICAL, PLUMBING): ");
      		String rtype = in.readLine();

     		 String query ="INSERT INTO Repair(rID, hotelID, roomNo, mCompany, repairDate, description, repairType) " +
            "VALUES (" + rid + ", " + hid + ", " + roomNo + ", " + cmpID + ", '" +
                       date + "', '" + desc + "', '" + rtype + "');";

      		esql.executeUpdate(query);
      		System.out.println("Repair added successfully.");
   } catch (Exception e) {
      System.err.println(e.getMessage());
   }
      
   }//end addRepair

  public static void bookRoom(DBProject esql) {
    // Given hotelID, roomNo and customer ID, create a booking in the DB
    try {
        // Booking ID
        String bid = readInt("Enter booking ID: ");

        // Customer ID
        String cid = readInt("Enter customer ID: ");

        // Hotel ID
        String hid = readInt("Enter hotelID: ");

        // Room number
        System.out.print("Enter room number: ");
        String roomNo = in.readLine();

        // Booking date
        System.out.print("Enter booking date (YYYY-MM-DD): ");
        String date = in.readLine();

        // Number of people
        String noOfPeople = readInt("Enter number of people: ");

        // Price
        System.out.print("Enter price (numeric, e.g., 199.99): ");
        String price = in.readLine();

        // Check for existing booking
        String check = "SELECT * FROM Booking " +
                       "WHERE hotelID = " + hid +
                       " AND roomNo = " + roomNo +
                       " AND bookingDate = '" + date + "';";

        int checkDuplicate = esql.executeQuery(check);

        if (checkDuplicate > 0) {
            System.out.println("This room has already been booked on that date. Please pick another time.");
            return;
        }

        // Insert booking
        String query = "INSERT INTO Booking(bID, customer, hotelID, roomNo, bookingDate, noOfPeople, price) " +
                       "VALUES (" + bid + ", " + cid + ", " + hid + ", " + roomNo +
                       ", '" + date + "', " + noOfPeople + ", " + price + ");";

        esql.executeUpdate(query);
        System.out.println("Booking created successfully.");

    } catch (Exception e) {
        System.err.println(e.getMessage());
    }
}

   public static void assignHouseCleaningToRoom(DBProject esql){
	  // Given Staff SSN, HotelID, roomNo Assign the staff to the room 
	try {
		System.out.print("Enter assignment ID: ");
		String asgID = in.readLine();

		System.out.print("Enter staff SSN: ");
		String ssn = in.readLine();

		System.out.print("Enter hotelID: ");
		String hid = in.readLine();
		
		System.out.print("Enter room number: ");
		String roomNo = in.readLine();

		String query = "INSERT INTO Assigned(asgID, staffID, hotelID, roomNo) " +
         "VALUES (" + asgID + ", '" + ssn + "', " + hid + ", " + roomNo + ")";

		esql.executeUpdate(query);
      System.out.println("Staff assigned.");
   } catch (Exception e) 
	{ System.err.println(e.getMessage()); }

 }//end assignHouseCleaningToRoom
   
   public static void repairRequest(DBProject esql){
	  // Given a hotelID, Staff SSN, roomNo, repairID , date create a repair request in the DB
      try {

	      System.out.print("Enter request ID: ");
	      String req = in.readLine();

	      System.out.print("Enter manager SSN: ");
	      String mid = in.readLine();

	      System.out.print("Enter repair ID: ");
	      String rid = in.readLine();

	      System.out.print("Enter request date (YYYY-MM-DD): ");
	      String date = in.readLine();

	      System.out.print("Enter description: ");
	      String desc = in.readLine();

	      String query = "INSERT INTO Request(reqID, managerID, repairID, requestDate, description) "+         "VALUES (" + req + ", " + mid + ", " + rid + ", '" + date + "', '" + desc + "')";

	      esql.executeUpdate(query);
      System.out.println("Repair request created.");
   } catch (Exception e) 
      { System.err.println(e.getMessage()); }
   }//end repairRequest
   
   public static void numberOfAvailableRooms(DBProject esql){
	  // Given a hotelID, get the count of rooms available 
      // Your code goes here.
      // ...
      // ...
      //
      //
      try {  
      String query = "SELECT count(*) FROM Room WHERE hotelID = ";
         System.out.print("\tEnter hotelID: $");
         String input = in.readLine();
         query += input;

          esql.executeQuery(query);
         System.out.println ("Above is the number of rooms for hotel " + input);
      }catch(Exception e){
         System.err.println (e.getMessage());
      
    }



   }//end numberOfAvailableRooms
   
   public static void numberOfBookedRooms(DBProject esql){
	  // Given a hotelID, get the count of rooms booked
      try {
	      System.out.print("Enter hotelID: ");
	      String hid = in.readLine();

	      System.out.print("Enter date (MM/DD/YYYY): ");
	      String date = in.readLine();

	      String query = "SELECT COUNT(*) FROM Booking " +
         "WHERE hotelID = " + hid + " AND bookingDate = '" + date + "'";

      esql.executeQuery(query);
   } catch(Exception e)
      { System.err.println(e.getMessage()); }

   }//end numberOfBookedRooms
   
   public static void listHotelRoomBookingsForAWeek(DBProject esql){
	  // Given a hotelID, date - list all the rooms booked for a week(including the input date) 
     try {
	     System.out.print("Enter hotelID: ");
	     String hid = in.readLine();

	     System.out.print("Enter start date (MM/DD/YYYY): ");
	     String date = in.readLine();

	     String query = "SELECT * FROM Booking " +
         "WHERE hotelID = " + hid + " " +
         "AND bookingDate BETWEEN '" + date + "' AND (DATE '" + date + "' + INTERVAL '7 days')";

      esql.executeQuery(query);
   } catch(Exception e)
     { System.err.println(e.getMessage()); }

   }//end listHotelRoomBookingsForAWeek
   
   public static void topKHighestRoomPriceForADateRange(DBProject esql){
	  // List Top K Rooms with the highest price for a given date range
      try {
	      System.out.print("Enter start date: ");
	      String s = in.readLine();

	      System.out.print("Enter end date: ");
	      String e = in.readLine();

	      System.out.print("Enter K: ");
	      String k = in.readLine();

	      String query = "SELECT roomNo, price FROM Booking " +
         "WHERE bookingDate BETWEEN '" + s + "' AND '" + e + "' " +
         "ORDER BY price DESC LIMIT " + k;

      esql.executeQuery(query);
   } catch(Exception ex)
      { System.err.println(ex.getMessage()); }
   }//end topKHighestRoomPriceForADateRange
   
   public static void topKHighestPriceBookingsForACustomer(DBProject esql){
	  // Given a customer Name, List Top K highest booking price for a customer 
     try {
	     System.out.print("Enter customer ID: ");
	     String cid = in.readLine();

	     System.out.print("Enter K: ");
	     String k = in.readLine();

	     String query = "SELECT * FROM Booking " +
         "WHERE customer = " + cid + " " +
         "ORDER BY price DESC LIMIT " + k;

      esql.executeQuery(query);
   } catch(Exception e)
     { System.err.println(e.getMessage()); }
   }//end topKHighestPriceBookingsForACustomer
   
   public static void totalCostForCustomer(DBProject esql){
	  // Given a hotelID, customer Name and date range get the total cost incurred by the customer
      try {
	      System.out.print("Enter customer ID: ");
	      String cid = in.readLine();

	      System.out.print("Enter start date: ");
	      String s = in.readLine();

	      System.out.print("Enter end date: ");
	      String e = in.readLine();

	      String query = "SELECT SUM(price) FROM Booking " +
         "WHERE customer = " + cid + " " +
         "AND bookingDate BETWEEN '" + s + "' AND '" + e + "'";



      esql.executeQuery(query);
   } catch(Exception ex)
      { System.err.println(ex.getMessage()); }
   }//end totalCostForCustomer
   
   public static void listRepairsMade(DBProject esql){
	  // Given a Maintenance company name list all the repairs along with repairType, hotelID and roomNo
      try {
	      System.out.print("Enter maintenance company ID: ");
	      String cid = in.readLine();

	      String query = "SELECT rID, hotelID, roomNo, repairDate, repairType, description " +
         "FROM Repair " +
         "WHERE mCompany = " + cid;

      esql.executeQuery(query);
   } catch(Exception e)
      { System.err.println(e.getMessage()); }
   }//end listRepairsMade
   
   public static void topKMaintenanceCompany(DBProject esql){
	  // List Top K Maintenance Company Names based on total repair count (descending order)
      try {
	      System.out.print("Enter K: ");
	      String k = in.readLine();

	      String query = "SELECT M.cmpID, M.name, COUNT(R.rID) AS repairCount " +
         "FROM MaintenanceCompany M " +
         "LEFT JOIN Repair R ON M.cmpID = R.mCompany " +
         "GROUP BY M.cmpID, M.name " +
         "ORDER BY repairCount DESC " +
         "LIMIT " + k;

      esql.executeQuery(query);
   } catch(Exception e)
      { System.err.println(e.getMessage()); }
   }//end topKMaintenanceCompany
   
   public static void numberOfRepairsForEachRoomPerYear(DBProject esql){
	  // Given a hotelID, roomNo, get the count of repairs per year
      try {
	      System.out.print("Enter hotelID: ");
	      String hid = in.readLine();

	      System.out.print("Enter roomNo: ");
	      String roomNo = in.readLine();

	      String query = "SELECT EXTRACT(YEAR FROM repairDate) AS year, COUNT(*) " +
         "FROM Repair " +
         "WHERE hotelID = " + hid + " AND roomNo = " + roomNo + " " +
         "GROUP BY year ORDER BY year";

      esql.executeQuery(query);
   } catch(Exception e)
      { System.err.println(e.getMessage()); }
   }//end listRepairsMade

}//end DBProject
