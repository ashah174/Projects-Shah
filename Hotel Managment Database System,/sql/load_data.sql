\copy Hotel(hotelID, address, manager) FROM 'data/hotel.csv' WITH (FORMAT text, DELIMITER ',', NULL '\N');

\copy MaintenanceCompany(cmpID, name, address, isCertified) FROM 'data/maintenanceCompany.csv' WITH (FORMAT text, DELIMITER ',', NULL '\N');

\copy Staff(SSN, fName, lName, address, role, employerID) FROM 'data/staff.csv' WITH (FORMAT text, DELIMITER ',', NULL '\N');

\copy Room(hotelID, roomNo, roomType) FROM 'data/room.csv' WITH (FORMAT text, DELIMITER ',', NULL '\N');

\copy Customer(customerID, fName, lName, Address, phNo, DOB, gender) FROM 'data/customer.csv' WITH (FORMAT text, DELIMITER ',', NULL '\N');

\copy Booking(bID, customer, hotelID, roomNo, bookingDate, noOfPeople, price) FROM 'data/booking.csv' WITH (FORMAT text, DELIMITER ',', NULL '\N');

\copy Repair(rID, hotelID, roomNo, mCompany, repairDate, description, repairType) FROM 'data/repair.csv' WITH (FORMAT text, DELIMITER ',', NULL '\N');

\copy Request(reqID, managerID, repairID, requestDate, description) FROM 'data/request.csv' WITH (FORMAT text, DELIMITER ',', NULL '\N');

\copy Assigned(asgID, staffID, hotelID, roomNo) FROM 'data/assigned.csv' WITH (FORMAT text, DELIMITER ',', NULL '\N');
