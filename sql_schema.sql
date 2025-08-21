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

-- ETL: Populate Normalized Tables

-- Insert Regions (avoid duplicates)
INSERT INTO Regions (RegionName)
SELECT DISTINCT Region
FROM inventory_forecasting_raw
ON CONFLICT (RegionName) DO NOTHING;

-- Insert Stores with linked RegionID
INSERT INTO Stores (StoreID, RegionID)
SELECT DISTINCT r."Store ID", rg.RegionID
FROM inventory_forecasting_raw r
JOIN Regions rg ON r.Region = rg.RegionName
ON CONFLICT (StoreID) DO NOTHING;

-- Insert Categories
INSERT INTO Categories (CategoryName)
SELECT DISTINCT Category
FROM inventory_forecasting_raw
ON CONFLICT (CategoryName) DO NOTHING;

-- Insert Products with linked CategoryID
INSERT INTO Products (ProductID, CategoryID)
SELECT DISTINCT r."Product ID", c.CategoryID
FROM inventory_forecasting_raw r
JOIN Categories c ON r.Category = c.CategoryName
ON CONFLICT (ProductID) DO NOTHING;

-- Insert InventoryTransactions records
INSERT INTO InventoryTransactions (
    Date, StoreID, ProductID, InventoryLevel, UnitsSold, UnitsOrdered,
    DemandForecast, Price, Discount, WeatherCondition, HolidayPromotion,
    CompetitorPricing, Seasonality
)
SELECT 
    TO_DATE(Date, 'YYYY-MM-DD'),
    "Store ID",
    "Product ID",
    "Inventory Level",
    "Units Sold",
    "Units Ordered",
    "Demand Forecast",
    Price,
    Discount,
    "Weather Condition",
    "Holiday/Promotion",
    "Competitor Pricing",
    Seasonality
FROM inventory_forecasting_raw;
