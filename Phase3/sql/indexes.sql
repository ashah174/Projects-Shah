-- 1. Speed up queries by room + booking date (HotelID, RoomNo, BookingDate)
CREATE INDEX idx_booking_room_date
ON Booking(hotelid, roomno, bookingdate);

-- 2. Speed up price-based searches in Booking (since Room table has no price)
CREATE INDEX idx_booking_price
ON Booking(price);

-- 3. Speed up customer lookup in Booking
CREATE INDEX idx_booking_customer
ON Booking(customer);

-- 4. Speed up queries on Repair by companyID
CREATE INDEX idx_repair_company
ON Repair(companyid);

-- 5. Speed up queries on Repair for room + repair date
CREATE INDEX idx_repair_room_date
ON Repair(hotelid, roomno, repdate);
