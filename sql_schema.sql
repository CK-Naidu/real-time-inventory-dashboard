-- Drop tables if they exist to avoid conflicts on re-creation
DROP TABLE IF EXISTS InventoryTransactions CASCADE;
DROP TABLE IF EXISTS Stores CASCADE;
DROP TABLE IF EXISTS Products CASCADE;
DROP TABLE IF EXISTS Categories CASCADE;
DROP TABLE IF EXISTS Regions CASCADE;

-- Create tables with primary keys, foreign keys, and unique constraints

CREATE TABLE Regions (
    RegionID SERIAL PRIMARY KEY,
    RegionName VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Stores (
    StoreID VARCHAR(10) PRIMARY KEY,
    RegionID INT REFERENCES Regions(RegionID)
);

CREATE TABLE Categories (
    CategoryID SERIAL PRIMARY KEY,
    CategoryName VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Products (
    ProductID VARCHAR(10) PRIMARY KEY,
    CategoryID INT REFERENCES Categories(CategoryID)
);

CREATE TABLE InventoryTransactions (
    TransactionID SERIAL PRIMARY KEY,
    Date DATE,
    StoreID VARCHAR(10) REFERENCES Stores(StoreID),
    ProductID VARCHAR(10) REFERENCES Products(ProductID),
    InventoryLevel INT,
    UnitsSold INT,
    UnitsOrdered INT,
    DemandForecast DECIMAL(10,2),
    Price DECIMAL(10,2),
    Discount INT,
    WeatherCondition VARCHAR(50),
    HolidayPromotion INT,
    CompetitorPricing DECIMAL(10,2),
    Seasonality VARCHAR(50)
);
