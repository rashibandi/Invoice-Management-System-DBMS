
SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

CREATE DATABASE IF NOT EXISTS invoiceManagement;
USE invoiceManagement;

-- CUSTOMER TABLE --
CREATE TABLE `customers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `invoice` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `house_no` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `postcode` varchar(255) NOT NULL,
  `phone` varchar(20) NOT NULL, -- Changed from int(20) to varchar(20)
  `address` varchar(255), 
  `due_invoices` INT DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DELIMITER //

CREATE TRIGGER create_address BEFORE INSERT ON customers 
FOR EACH ROW 
BEGIN
    SET NEW.address = CONCAT_WS(' ', NEW.house_no, NEW.city, NEW.country, NEW.postcode);
END;
//
DELIMITER ;

INSERT INTO `customers` (`id`, `invoice`, `name`, `email`, `house_no`, `city`, `country`, `postcode`, `phone`) VALUES
(43, '3', 'Anne B Ruch', 'anner@mail.com', '4039', 'Indianapolis', 'US', '46225', '1478500000'),
(44, '4', 'Albert M Dunford', 'albd@mail.com', '1143', 'Norcross', 'US', '30092', '8520000010'),
(46, '6', 'Wendy Reilly', 'wendy@mail.com', '3605 ', 'Wharton', 'US', '77488', '3214444444'),
(47, '7', 'Test Customer', 'testc@mail.com', '110', 'Mumbai', 'India', '00225', '7777777770'),
(48, '8', 'Demo User', 'demouser@mail.com', '115', 'Mumbai', 'India', '00020', '7777777777'),
(50, '10', 'Rose Thompson', 'thompsonr@mail.com', '2374', 'Northampton', 'US', '01010', '7410000020');

-- INVOICE TABLE 
-- CREATE TABLE `invoices` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `invoice` varchar(255) NOT NULL UNIQUE,
--   `custom_email` varchar(255) NOT NULL, -- Changed from text to varchar(255)
--   `invoice_date` date NOT NULL,
--   `invoice_due_date` date NOT NULL,
--   `total` decimal(10,0) NOT NULL,
--   `status` varchar(255) NOT NULL default 'open',
--   FOREIGN KEY (`custom_email`) REFERENCES `customers` (`email`),
--   PRIMARY KEY (`id`)
-- ) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE `invoices` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `invoice` varchar(255) NOT NULL UNIQUE,
  `custom_email` varchar(255) NOT NULL,
  `invoice_date` date NOT NULL,
  `invoice_due_date` date NOT NULL,
  `total` decimal(10,0) NOT NULL,
  `status` varchar(255) NOT NULL default 'open',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


INSERT INTO `invoices` (`id`, `invoice`, `custom_email`, `invoice_date`, `invoice_due_date`, `total`, `status`) VALUES
(47, '3', 'anner@mail.com', '2021-11-13', '2012-11-15', '132', 'paid'),
(46, '4', 'albd@mail.com', '2021-11-13', '2021-11-17', '270', 'open'),
(49, '6', 'wendy@mail.com', '2021-11-13', '2021-11-18', '534','open'),
(51, '7', 'testc@mail.com', '2021-11-13', '2021-11-16', '600','paid'),
(52, '8', 'demouser@mail.com', '2021-11-13', '2021-11-18', '153','open'),
(54, '10', 'thompsonr@mail.com', '2021-11-15', '2021-11-16', '154','open');

DELIMITER //
CREATE PROCEDURE update_due_invoices(IN customer_email VARCHAR(255))
BEGIN
    DECLARE num_due_invoices INT;
    
    SELECT COUNT(*) INTO num_due_invoices
    FROM invoices
    WHERE custom_email = customer_email AND status = 'open';
    
    UPDATE customers
    SET due_invoices = num_due_invoices
    WHERE email = customer_email;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_due_invoices_on_status_change
AFTER UPDATE ON invoices
FOR EACH ROW
BEGIN
    IF NEW.status <> OLD.status THEN
        CALL update_due_invoices(NEW.custom_email);
    END IF;
END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER update_due_invoices_on_insert
AFTER INSERT ON invoices
FOR EACH ROW
BEGIN
    IF NEW.status = 'open' THEN
        CALL update_due_invoices(NEW.custom_email);
    END IF;
END//
DELIMITER ;



 -- ------PRODUCT -------

CREATE TABLE `products` (
  `product_id` int(11) NOT NULL,
  `product_name` text NOT NULL,
  `product_price` varchar(255) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


INSERT INTO `products` (`product_id`, `product_name`, `product_price`) VALUES
(979, 'Product One', '34'),
(980, 'Product Two', '13'),
(981, 'Product Three', '68'),
(982, 'Product Four', '5'),
(983, 'Product Five', '86'),
(984, 'Product Six', '12'),
(985, 'Product Seven', '23'),
(986, 'Product Eight', '19');


-- -------- USERS -------

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `username` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `password` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;



CREATE TABLE `invoice_items`(
    `invoice` varchar(255) NOT NULL, 
    `product_id` int(11) NOT NULL, 
    `product_name` varchar(255) NOT NULL,
    `qty` int NOT NULL,
    `purchaseDate` date
);
--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `username`, `email`, `phone`, `password`) VALUES
(1, 'admin', 'admin', 'admin@dbmsproject.com', '1234567890', 'password');

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);
  
ALTER TABLE `invoice_items` 
	ADD foreign key (product_id) references products(product_id);

-- AUTO_INCREMENT for table `customers`
--
ALTER TABLE `customers`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=51;
--
-- AUTO_INCREMENT for table `invoices`
--
ALTER TABLE `invoices`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;
--
--
--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `product_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=987;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

