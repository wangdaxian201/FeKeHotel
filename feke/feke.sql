-- 房间类型表
CREATE TABLE room_type (
  room_type_id INT NOT NULL AUTO_INCREMENT,
  room_type_name VARCHAR(50) NOT NULL,
  room_type_desc VARCHAR(200),
  room_type_price DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (room_type_id)
);
-- 房间表
CREATE TABLE room (
  room_id INT NOT NULL AUTO_INCREMENT,
  room_type_id INT NOT NULL,
  room_number VARCHAR(20) NOT NULL,
  room_floor INT NOT NULL,
  room_area DECIMAL(10,2),
  room_description VARCHAR(200),
  PRIMARY KEY (room_id),
  FOREIGN KEY (room_type_id) REFERENCES room_type (room_type_id) ON DELETE CASCADE
);

-- 客户表
CREATE TABLE customer (
  customer_id INT NOT NULL AUTO_INCREMENT,
  customer_name VARCHAR(50) NOT NULL,
  customer_phone VARCHAR(20),
  PRIMARY KEY (customer_id)
);

-- 订单表
CREATE TABLE orders (
  order_id INT NOT NULL AUTO_INCREMENT, 
  room_id INT NOT NULL,
  customer_id INT NOT NULL,
  order_date DATE NOT NULL,
  order_start_time DATETIME NOT NULL,
  order_end_time DATETIME NOT NULL,
  order_source VARCHAR(50) NOT NULL,
  return_rate DECIMAL(5,2),
  order_price DECIMAL(10,2),
  PRIMARY KEY (order_id),
  FOREIGN KEY (room_id) REFERENCES room (room_id) ON DELETE CASCADE,
  FOREIGN KEY (customer_id) REFERENCES customer (customer_id) ON DELETE CASCADE
);
