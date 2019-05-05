CREATE TABLE Product(
    Product_ID SERIAL PRIMARY KEY,
    Product_Name varchar(255) UNIQUE,
    Category varchar(255),
    Quantity NUMERIC(8) CHECK (Quantity>=0),
    Image_Link varchar(255),
    Company_Name varchar(255),
    Description text,
    Cost Numeric(8,2)
);


CREATE TABLE "User"(
    email varchar(255) Primary KEY,
    firstName varchar(255),
    lastName varchar(255),
    "password" varchar(255),
);


CREATE TABLE Cart(
    email varchar(255) References "User"(email),
    Total_Cost Numeric(8,2),
    cart_id SERIAL PRIMARY KEY
);

CREATE TABLE productandcarts(
  cart_id SERIAL REFERENCES cart(cart_id),
  product_id SERIAL REFERENCES product(product_id)
);

CREATE TABLE Card (
    Card_Number Numeric(16) Primary Key,
    email varchar(255) References "User"(email),
    CCV Numeric(3),
    Experation_Date DATE,
    "Name" varchar(255),
    Zip_Code Numeric(5)
);

CREATE TABLE REVIEWS(
    Review_id SERIAL PRIMARY KEY,
    Product_ID SERIAL References Product(Product_ID),
    Rating Numeric(5),
    email varchar(255) References "User"(email),
    Comment varchar(255)
);

CREATE TABLE admin(
  adminUser varchar(255) PRIMARY KEY,
  password varchar(255)
);

CREATE TABLE Address(
  addressID SERIAL PRIMARY KEY,
  address varchar(255),
  city varchar(255),
  state varchar(2)
);
ALTER TABLE address ADD CONSTRAINT uniqueAddress UNIQUE(address, city, state);

CREATE TABLE addressanduser(
  email varchar(255) REFERENCES "User"(email),
  addressID SERIAL REFERENCES address(addressID)
);
ALTER TABLE addressanduser ADD CONSTRAINT uniqueUserAndAddress UNIQUE(email, addressID);

CREATE TABLE "Order"(
    ORDER_ID SERIAL Primary KEY,
    email varchar(255) References "User"(email),
    Card_Number Numeric(16),
    Order_Date DATE,
    AddressID INTEGER REFERENCES Address(addressID),
    ISORDERDONE BOOLEAN
);

CREATE Table purchasehistory(
    email varchar(255),
    product_id INTEGER references Product(Product_ID),
    order_id INTEGER REFERENCES "Order"(ORDER_ID),
    Cost Numeric(8,2)
);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('Galaxy s10','Phones', 2000, '/galaxys10', 'Samsung', 1000);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('IPhone XS','Phones', 1899, '/iphonexs', 'Apple', 1100);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('Pixel 3','Phones', 465, '/pixel3', 'Google', 870);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('GeForce RTX 2070','Computer Hardware', 100, '/geforcertx2070', 'NVIDIA', 600);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('4770K','Computer Hardware', 3456, '/4770k', 'Intel', 200);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('Commuter Series IPhone XS','Phone Accessories', 676, '/commuterseriesiphonexs', 'Otterbox', 30);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('Macbook Pro 13in','Computer', 321, '/macbookpro13in', 'Apple', 1400);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('XPS 13in','Computer', 974, '/xps13in', 'Dell', 1200);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('C8 65in','TV', 670, '/c865in', 'LG', 2000);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('Red Dead Redemption 2','Video Games', 6746, '/reddeadredemption2', 'Rockstar', 59.99);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('The Division 2','Video Games', 23948, '/thedivision2', 'Ubisoft', 59.99);

INSERT INTO Product (Product_Name, Category, Quantity, Image_Link, Company_Name, Cost)
VALUES ('IPad Pro 11in','Tablets', 30000, '/ipadpro11in', 'Apple', 700);


CREATE OR REPLACE FUNCTION addUserTrigger() RETURNS TRIGGER AS
$BODY$
BEGIN
  INSERT INTO cart(email, total_cost)
  VALUES (new.email, 0);
  RETURN new;
end;
$BODY$ LANGUAGE plpgsql;


CREATE TRIGGER addUserTrigger
  AFTER INSERT ON "User"
  FOR EACH ROW
  EXECUTE PROCEDURE addUserTrigger();

INSERT INTO "User"
VALUES ('hcook@gmail.com', 'Harrison', 'Cook', '5f4dcc3b5aa765d61d8327deb882cf99');

INSERT INTO "User"
VALUES ('snlguy@gmail.com', 'Alec', 'Baldwin', '21232f297a57a5a743894a0e4a801fc3');

INSERT INTO "User"
VALUES ('john@gmail.com', 'John', 'James', '527bd5b5d689e2c32ae974c6229ff785');

INSERT INTO "User"
VALUES ('carl@gmail.com', 'Carl', 'Hardees', 'a0df931e7a7f9b608c165504bde9b620');

INSERT INTO "User"
VALUES ('alex@gmail.com', 'Alex', 'Smith', '534b44a19bf18d20b71ecc4eb77c572f');

INSERT INTO "User"
VALUES ('bob@gmail.com', 'Bob', 'Jones', '9f9d51bc70ef21ca5c14f307980a29d8');

INSERT INTO "User"
VALUES ('sam@gmail.com', 'Sam', 'Wilson', '332532dcfaa1cbf61e2a266bd723612c');

INSERT INTO "User"
VALUES ('tom@gmail.com', 'Tom', 'Brady', '34b7da764b21d298ef307d04d8152dc5');

INSERT INTO Address(address, city, state) VALUES ('1538 West Broad St. Apt 230', 'Richmond', 'VA');
INSERT INTO addressanduser VALUES ('hcook@gmail.com', (SELECT addressid FROM address WHERE address.address='1538 West Broad St. Apt 230' AND address.city='Richmond' AND address.state='VA'));

INSERT INTO Address(address, city, state) VALUES ('123 Maple St.', 'Alexandria', 'VA');
INSERT INTO addressanduser VALUES ('snlguy@gmail.com', (SELECT addressid FROM address WHERE address.address='123 Maple St.' AND address.city='Alexandria' AND address.state='VA'));

INSERT INTO addressanduser VALUES ('john@gmail.com', (SELECT addressid FROM address WHERE address.address='1538 West Broad St. Apt 230' AND address.city='Richmond' AND address.state='VA'));

INSERT INTO Address(address, city, state) VALUES ('1960 Hardees Ln.', 'Rocky Mount', 'NC');
INSERT INTO addressanduser VALUES ('carl@gmail.com', (SELECT addressid FROM address WHERE address.address='1960 Hardees Ln.' AND address.city='Rocky Mount' AND address.state='NC'));

INSERT INTO Address(address, city, state) VALUES ('1902 Target Rd.', 'Minneapolis', 'MN');
INSERT INTO addressanduser VALUES ('alex@gmail.com', (SELECT addressid FROM address WHERE address.address='1902 Target Rd.' AND address.city='Minneapolis' AND address.state='MN'));

INSERT INTO Address(address, city, state) VALUES ('1700 Wade Hampton Blvd', 'Greenville', 'SC');
INSERT INTO addressanduser VALUES ('bob@gmail.com', (SELECT addressid FROM address WHERE address.address='1700 Wade Hampton Blvd' AND address.city='Greenville' AND address.state='SC'));

INSERT INTO Address(address, city, state) VALUES ('1 Hacker Ln.', 'San Jose', 'CA');
INSERT INTO addressanduser VALUES ('sam@gmail.com', (SELECT addressid FROM address WHERE address.address='1 Hacker Ln.' AND address.city='San Jose' AND address.state='CA'));

INSERT INTO addressanduser
VALUES ('tom@gmail.com', (SELECT addressid FROM address WHERE address.address='1 Hacker Ln.' AND address.city='San Jose' AND address.state='CA'));

CREATE OR REPLACE FUNCTION searchForProduct(searchTerm varchar(255)) RETURNS SETOF product
AS
$BODY$
  SELECT *
  FROM product
  WHERE (UPPER(company_name) LIKE ('%' || UPPER(searchTerm) || '%')) OR (UPPER(product_name) LIKE ('%' || UPPER(searchTerm) || '%'));
$BODY$ LANGUAGE sql;

CREATE OR REPLACE FUNCTION updateCartPrice() RETURNS TRIGGER AS
$BODY$
BEGIN
UPDATE cart
SET total_cost = total_cost+(SELECT "cost" FROM product WHERE product_id=new.product_id)
WHERE cart_id=new.cart_id;
RETURN new;
END;
$BODY$ LANGUAGE plpgsql;

CREATE TRIGGER watchProductAdded
AFTER INSERT ON productandcarts
FOR EACH ROW
EXECUTE PROCEDURE updateCartPrice();

CREATE OR REPLACE FUNCTION lowerPrice() RETURNS TRIGGER AS
$BODY$
BEGIN
UPDATE cart
SET total_cost = total_cost-(SELECT "cost" FROM product WHERE product_id=old.product_id)
WHERE cart_id=old.cart_id AND total_cost>=(SELECT "cost" FROM product WHERE product_id=old.product_id);
UPDATE product
SET quantity=quantity+1
WHERE product_id=old.product_id;
RETURN new;
END;
$BODY$ LANGUAGE plpgsql;


CREATE TRIGGER watchProductRemoved
AFTER DELETE ON productandcarts
FOR EACH ROW
EXECUTE PROCEDURE lowerPrice();


CREATE FUNCTION addMoreProduct(product_id_given INTEGER, amount INTEGER)
RETURNS VOID AS
$BODY$
BEGIN
    UPDATE product
    SET quantity=quantity+amount
    WHERE product_id=product_id_given;
end;
$BODY$ LANGUAGE plpgsql;

CREATE FUNCTION productInCheckOut() RETURNS TRIGGER AS
$BODY$
BEGIN
    UPDATE product
    SET quantity=quantity-1
    WHERE product_id=new.product_id;
    RETURN NEW;
end;
$BODY$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION onordercreated() RETURNS TRIGGER AS
$BODY$
DECLARE
  tempRow RECORD;
BEGIN
  FOR tempRow in (SELECT * FROM productandcarts WHERE cart_id=(SELECT cart_id FROM Cart WHERE email=new.email)
  LOOP
    INSERT INTO purchasehistory
    VALUES (new.email, tempRow.product_id , new.order_id, (SELECT Cost From product WHERE product.product_id=tempRow.product_id));
  END LOOP;
  DELETE FROM productandcarts
  WHERE cart_id=(SELECT cart_id FROM Cart WHERE email=new.email);
  RETURN new;
end;
$BODY$ LANGUAGE plpgsql;


CREATE TRIGGER watchordercreated
AFTER INSERT ON "Order"
FOR EACH ROW
EXECUTE PROCEDURE onordercreated();


INSERT INTO productandcarts
VALUES (1,1);

INSERT INTO productandcarts
VALUES (1,12);

INSERT INTO productandcarts
VALUES (3,4);

INSERT INTO productandcarts
VALUES (3,5);

INSERT INTO productandcarts
VALUES (6,9);

INSERT INTO productandcarts
VALUES (8,11);

INSERT INTO productandcarts
VALUES (8,10);

INSERT INTO productandcarts
VALUES (5,3);

INSERT INTO productandcarts
VALUES (2,7);

INSERT INTO productandcarts
VALUES (4,8);

INSERT INTO Card
VALUES (123456, 'hcook@gmail.com', 202, (select date '2023-04-01' + interval '1 month -1 day'), 'Harrison Cook', 22466);

INSERT INTO Card
VALUES (098765, 'hcook@gmail.com', 938, (select date '2020-10-01' + interval '1 month -1 day'), 'Harrison Cook', 22466);

INSERT INTO Card
VALUES (423283, 'sam@gmail.com', 423, (select date '2022-01-01' + interval '1 month -1 day'), 'Sam Wilson', 56478);

INSERT INTO Card
VALUES (478943, 'john@gmail.com', 347, (select date '2024-02-01' + interval '1 month -1 day'), 'John James', 58403);

INSERT INTO Card
VALUES (064899, 'carl@gmail.com', 987, (select date '2020-04-01' + interval '1 month -1 day'), 'Carl Hardees', 37842);

INSERT INTO Card
VALUES (897897, 'alex@gmail.com', 237, (select date '2019-12-01' + interval '1 month -1 day'), 'Alex Smith', 47392);

INSERT INTO Card
VALUES (473899, 'bob@gmail.com', 340, (select date '2020-03-01' + interval '1 month -1 day'), 'Bob Jones', 08923);

INSERT INTO Card
VALUES (789123, 'tom@gmail.com', 908, (select date '2021-06-01' + interval '1 month -1 day'), 'Tom Miller', 89238);

INSERT INTO "Order"(email, card_number, order_date, isorderdone, addressID)
VALUES ('hcook@gmail.com', 123456, date '2018-06-21', TRUE, 1);

INSERT INTO "Order"(email, card_number, order_date, isorderdone, addressID)
VALUES ('bob@gmail.com', 473899, date '2019-02-01',TRUE,5);

INSERT INTO "Order"(email, card_number, order_date, isorderdone, addressID)
VALUES ('alex@gmail.com', 897897, date '2019-03-12',TRUE,4);

INSERT INTO "Order"(email, card_number, order_date, isorderdone, addressID)
VALUES ('tom@gmail.com', 789123, date '2018-12-7',TRUE, (SELECT addressid FROM address WHERE address.address='1 Hacker Ln.' AND address.city='San Jose' AND address.state='CA'));

INSERT INTO "Order"(email, card_number, order_date, isorderdone, addressID)
VALUES ('carl@gmail.com', 64899, date '2019-04-17', FALSE, 3);

INSERT INTO "Order"(email, card_number, order_date, isorderdone, addressID)
VALUES ('hcook@gmail.com', 123456, date '2019-01-21',TRUE, 1);

INSERT INTO "Order"(email, card_number, order_date, isorderdone, addressID)
VALUES ('hcook@gmail.com', 123456, date '2019-04-19' , FALSE, (SELECT addressid FROM address WHERE address.address='1538 West Broad St. Apt 230' AND address.city='Richmond' AND address.state='VA'));


INSERT INTO reviews(Product_ID, Rating, email, Comment)
VALUES (7,5,'hcook@gmail.com','Great laptop!');

INSERT INTO reviews(Product_ID, Rating, email, Comment)
VALUES (8,4,'snlguy@gmail.com','Good product from dell.');

INSERT INTO reviews(Product_ID, Rating, email, Comment)
VALUES (9,5,'tom@gmail.com','Best tv ever!');

INSERT INTO reviews(Product_ID, Rating, email, Comment)
VALUES (11,4,'hcook@gmail.com','Much better than the last game.');

INSERT INTO reviews(Product_ID, Rating, email, Comment)
VALUES (12,4,'carl@gmail.com','I use my ipad for work its a great product.');

INSERT INTO reviews(Product_ID, Rating, email, Comment)
VALUES (7, 4,'bob@gmail.com','Pretty good product.');


CREATE OR REPLACE FUNCTION removeUser(emailGiven varchar(255)) RETURNS VOID AS
$BODY$
BEGIN
  DELETE FROM productandcarts
  WHERE cart_id=(SELECT cart_id FROM cart WHERE emailGiven=email);
  DELETE FROM cart
  WHERE email=emailGiven;
  DELETE FROM "User"
  WHERE emailGiven = email;
end;
$BODY$ LANGUAGE plpgsql;

UPDATE product
SET description='The 10th generation of Samsung Galaxy lets you do more and do it better. The new Samsung Galaxy S10 has more screen with an all-new nearly bezel-less 6.1-inch QHD+ Cinematic Infinity Display. With a total of 4 cameras, its premium performance utilizes the Pro-grade Cameras with optical zoom for effortless capture and an ultra-wide lens that sees the world like you do. The in-display Ultrasonic Fingerprint ID gives the next generation in security, unlocking with a tap of the screen. Best of all, the Wireless PowerShare feature lets you wirelessly charge your Galaxy Buds, Galaxy Watch, or even a friend''s Qi wireless charging capable phone right from your device!'
WHERE product_name='Galaxy S10';

UPDATE product
SET description='iPhone XS Max has Apple''s largest display on an iPhone ever. It features a Dual-camera system. Wireless charging. Gigabit-class LTE connectivity. Augmented Reality. Advanced Neural Engine. 4K HD video. And a TrueDepth camera.'
WHERE product_name='IPhone XS';

UPDATE product
SET description='Introducing the revolutionary Pixel 3. The phone that reimagines the camera. And in doing so reimagines everything you can do, too.'
WHERE product_name='Pixel 3';

UPDATE product
SET description='Intel Core i7-4770K Haswell Quad-Core 3.5 GHz LGA 1150 84W'
WHERE product_name='4770K';

UPDATE product
SET description='You don’t have time to precision pack your briefcase. So pack along Commuter Series — the slim, sleek case that fits into any pocket, purse or bag. Featuring two tough layers — an internal slipcover and exterior shell — Commuter Series keeps your smartphone safe from drops, bumps, dust and life on the go.'
WHERE product_name='Commuter Series IPhone XS';

UPDATE product
SET description='Brilliant Retina display with True Tone technology
Touch Bar and Touch ID
Intel Iris Plus Graphics 655
Ultrafast SSD
Four Thunderbolt 3 (USB-C) ports
Up to 10 hours of battery life
802. 11ac Wi-Fi
Force Touch trackpad
macOS Mojave, inspired by pros but designed for everyone, with Dark Mode, Stacks, easier screenshots, new built-in apps, and more'
WHERE product_name='Macbook Pro 13in';

UPDATE product
SET description='1. 13.3" touch screen:3840 x 2160 native resolution. Natural finger-touch navigation makes the most of Windows 10. 3. Thunderbolt 3 port:This compact port connects to USB, DisplayPort, PCI Express, and Thunderbolt devices, and offers four times the data and twice the video bandwidth of any other cable.'
WHERE product_name='XPS 13in';

UPDATE product
SET description='The sleek C8 is designed to elevate a room’s aesthetics while complementing any decor. This new LG OLED TV with AI (Artificial Intelligence) ThinQ becomes the hub for the smart home: Using Intelligent Voice control, speak into the LG Magic Remote to pull up family photos, control light settings, check the weather and more. Movies, sports and games come to thrilling new life, more immersive with the perfect black and intense color made possible by LG OLED display technology. The new α9 (Alpha9) Intelligent Processor makes the most of the self-illuminating pixels, providing true-to-life images with rich colors, superior sharpness and enhanced depth. The C8 features comprehensive support of major 4K high dynamic range formats including premium Dolby Vision, as well as HDR10 and HLG.'
WHERE product_name='C8 65in';

UPDATE product
SET description='With the gameplay of Red Dead Redemption 2 as its foundation, Red Dead Online transforms the vast and deeply detailed landscapes, cities, towns and habitats of Red Dead Redemption 2 into a new, living online world ready to be shared by multiple players. Create and customize your character, tailor your abilities to suit your play style and head out into a new frontier full of things to experience.'
WHERE product_name='Red Dead Redemption 2';

UPDATE product
SET description='The fate of the free world is on the line in Tom Clancy The Division 2. Lead a team of elite agents into a post-pandemic Washington, DC, to restore order and prevent the collapse of the city.'
WHERE product_name='The Division 2';

UPDATE product
SET product_name='IPad Pro 10.5in'
WHERE product_name='IPad Pro 11in';

UPDATE product
SET description='From the manufacturer Style:XC  |  Size:Real Boost Clock: 1710 MHz The EVGA GeForce RTX 20-Series Graphics Cards are powered by the all-new NVIDIA Turing architecture to give you incredible new levels of gaming realism, speed, power efficiency, and immersion. With the EVGA GeForce RTX 20-Series gaming cards you get the best gaming experience with next generation graphics performance, ice cold cooling, and advanced overclocking features with the all new EVGA Precision X1software. The new NVIDIA GeForce RTX GPUs have reinvented graphics and set a new bar for performance. Powered by the new NVIDIA Turing GPU architecture and the revolutionary NVIDIA RTX platform, the new graphics cards bring together real-time ray tracing, artificial intelligence, and programmable shading. This is not only a whole new way to experience games - this is the ultimate PC gaming experience.'
WHERE product_name='GeForce RTX 2070';

INSERT INTO admin
VALUES ('bobby', 'a9c4cef5735770e657b7c25b9dcb807b');

INSERT INTO admin
VALUES ('ron', '45798f269709550d6f6e1d2cf4b7d485');

CREATE OR REPLACE FUNCTION deleteUser(emailG varchar(255))
RETURNS VOID AS
$BODY$
  BEGIN
    DELETE FROM reviews
    WHERE email=emailG;
    DELETE FROM "Order"
    WHERE email=emailG;
    DELETE FROM Card
    WHERE email=emailG;
    DELETE FROM cart
    WHERE email=emailG;
    DELETE FROM "User"
    WHERE email=emailG;
  end;
$BODY$ language plpgsql;


CREATE OR REPLACE FUNCTION deleteOrder(orderID integer)
RETURNS VOID AS
$BODY$
BEGIN
  DELETE FROM purchasehistory
  WHERE order_id=orderID;
  DELETE FROM "Order"
  WHERE order_id=orderID;
end;
$BODY$ LANGUAGE plpgsql;