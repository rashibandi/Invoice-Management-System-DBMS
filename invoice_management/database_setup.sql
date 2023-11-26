SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

Create database invoiceManagement;
use invoiceManagement;

-- ------CUSTOMER TABLE ------

CREATE TABLE `customers` (
  `id` int(11) NOT NULL,
  `invoice` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `house_no` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `country` varchar(255) NOT NULL,
  `postcode` varchar(255) NOT NULL,
  `phone` varchar(100) NOT NULL,
  `address` varchar(255)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

DELIMITER //
CREATE TRIGGER create_address BEFORE INSERT ON customers 
FOR EACH ROW 
BEGIN
	SET NEW.address = concat_ws(' ', new.house_no, new.city, new.country, new.postcode);
END;
//
DELIMITER ;

INSERT INTO `customers` (`id`, `invoice`, `name`, `email`, `house_no`, `city`, `country`, `postcode`, `phone`) VALUES
(43, '3', 'Anne B Ruch', 'anner@mail.com', '4039', 'Indianapolis', 'US', '46225', '1478500000'),
(44, '4', 'Albert M Dunford', 'albd@mail.com', '1143', 'Norcross', 'US', '30092', '8520000010'),
(45, '5', 'Anne B Ruch', 'anner@mail.com', '4039', 'Indianapolis', 'US', '46225', '1478500000'),
(46, '6', 'Wendy Reilly', 'wendy@mail.com', '3605 ', 'Wharton', 'US', '77488', '3214444444'),
(47, '7', 'Test Customer', 'testc@mail.com', '110', 'Mumbai', 'India', '00225', '7777777770'),
(48, '8', 'Demo User', 'demouser@mail.com', '115', 'Mumbai', 'India', '00020', '7777777777'),
(49, '9', 'Wendy Reilly', 'wendy@mail.com', '3605', 'Wharton', 'US', '77488', '3214444444'),
(50, '10', 'Rose Thompson', 'thompsonr@mail.com', '2374', 'Northampton', 'US', '01010', '7410000020');

-- ------INVOICE TABLE ------

CREATE TABLE `invoices` (
  `id` int(11) NOT NULL,
  `invoice` varchar(255) NOT NULL,
  `custom_email` text NOT NULL,
  `invoice_date` varchar(255) NOT NULL,
  `invoice_due_date` varchar(255) NOT NULL,
  `total` decimal(10,0) NOT NULL
  `status` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;


INSERT INTO `invoices` (`id`, `invoice`, `custom_email`, `invoice_date`, `invoice_due_date`, `total`, `status`) VALUES
(42, '1', '', '12/11/2021', '14/11/2021', '523', 'paid'),
(44, '2', '', '12/11/2021', '13/11/2021', '395', 'paid'),
(47, '3', '', '13/11/2021', '15/11/2021', '132', 'paid'),
(46, '4', '', '13/11/2021', '17/11/2021', '270', 'open'),
(48, '5', '', '13/11/2021', '17/11/2021', '405', 'open'),
(49, '6', '', '13/11/2021', '18/11/2021', '534','open'),
(51, '7', '', '13/11/2021', '16/11/2021', '600','paid'),
(52, '8', '', '13/11/2021', '15/11/2021', '153','open'),
(53, '9', '', '15/11/2021', '17/11/2021', '115','open'),
(54, '10', '', '15/11/2021', '16/11/2021', '154','open');

-- -----INVOICE ITEMS ------

CREATE TABLE `invoice_items` (
  `id` int(11) NOT NULL,
  `invoice` varchar(255) NOT NULL,
  `product` text NOT NULL,
  `qty` int(11) NOT NULL,
  `price` varchar(255) NOT NULL,
  `total` varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=latin1;



INSERT INTO `invoice_items` (`id`, `invoice`, `product`, `qty`, `price`, `total`) VALUES
(90, '5', 'Product One', 12, '34','405.00'),status
(89, '4', 'Product Two', 21, '13', '270.00'),
(91, '6', 'Product Four', 5, '5', '23.00'),
(92, '6', 'Product Five', 6, '86','511.00'),
(95, '8', 'Product Seven', 5, '23','115.00'),
(96, '8', 'Product Four', 8, '5', '38.00'),
(97, '9', 'Product Seven', 5, '23','115.00'),
(98, '10', 'Product Six', 13, '12', '154.00');

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

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `username`, `email`, `phone`, `password`) VALUES
(1, 'admin', 'admin', 'admin@dbmsproject.com', '1234567890', 'password');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `invoices`
--
ALTER TABLE `invoices`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `invoice_items`
--
ALTER TABLE `invoice_items`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`product_id`);

--
-- Indexes for table `store_customers`
--

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
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
-- AUTO_INCREMENT for table `invoice_items`
--
ALTER TABLE `invoice_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;
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