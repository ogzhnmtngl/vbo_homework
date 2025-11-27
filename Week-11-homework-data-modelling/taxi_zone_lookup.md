Dimensional Data Modeling(NYC Taxi Data Warehouse)

## 1. Entities
Fact_Taxi_Trips: The central entity representing a single completed taxi journey. It contains quantitative data (measures) such as fare amount, trip distance, passenger count, and keys to associated dimensions.

Dim_Date: Represents the temporal aspect of the trips. It provides detailed attributes for dates (Day name, Month, Year, Weekend flag) to facilitate time-based analysis.

Dim_Location: Represents the geospatial data defined by the NYC Taxi & Limousine Commission. It contains details about Boroughs, Zones, and Service Zones.

Dim_Vendor: Represents the TPEP (Technology Provider) that provided the record for the trip (e.g., Creative Mobile Technologies, VeriFone Inc.).

Dim_RateCode: Represents the final rate category applied to the trip (e.g., Standard rate, JFK, Newark, Negotiated fare).

Dim_Payment: Represents the method used by the passenger to pay for the trip (e.g., Credit Card, Cash, No Charge).

## 2. Relationships
Dim_Date - Fact_Taxi_Trips: One-to-Many (A single date, e.g., "2023-01-01", is associated with many taxi trips occurring on that day).

Dim_Vendor - Fact_Taxi_Trips: One-to-Many (A single vendor provider records many trips over time).

Dim_RateCode - Fact_Taxi_Trips: One-to-Many (A specific rate code, e.g., "Standard Rate", is applied to many different trips).

Dim_Payment - Fact_Taxi_Trips: One-to-Many (A specific payment type, e.g., "Credit Card", is used in many trips).

Dim_Location - Fact_Taxi_Trips (Pickup): One-to-Many (A specific location, e.g., "JFK Airport", can be the starting point (pickup) for many trips).

Dim_Location - Fact_Taxi_Trips (Dropoff): One-to-Many (The same specific location can also be the destination (dropoff) for many trips). Note: This represents a Role-Playing Dimension relationship.

## 3. Visual Representation

![Logical Plan](Logical-Plan.png)

# Physical Plan

```
CREATE TABLE public.Dim_Date (
    Date_Key integer NOT NULL,
    Full_Date date NOT NULL,
    Day_Name varchar(20),
    Is_Weekend boolean,
    Month_Name varchar(20),
    Year integer,
    CONSTRAINT Dim_Date_pk PRIMARY KEY (Date_Key)
);

CREATE TABLE public.Dim_Location (
    Location_Key serial NOT NULL,
    LocationID integer NOT NULL,
    Borough varchar(100),
    Zone varchar(100),
    Service_Zone varchar(100),
    CONSTRAINT Dim_Location_pk PRIMARY KEY (Location_Key)
);

CREATE TABLE public.Dim_Vendor (
    Vendor_Key serial NOT NULL,
    VendorID integer,
    Vendor_Name varchar(100),
    CONSTRAINT Dim_Vendor_pk PRIMARY KEY (Vendor_Key)
);

CREATE TABLE public.Dim_RateCode (
    RateCode_Key serial NOT NULL,
    RateCodeID integer,
    Rate_Description varchar(100),
    CONSTRAINT Dim_RateCode_pk PRIMARY KEY (RateCode_Key)
);

CREATE TABLE public.Dim_Payment (
    Payment_Key serial NOT NULL,
    Payment_Type_ID integer,
    Payment_Name varchar(50),
    CONSTRAINT Dim_Payment_pk PRIMARY KEY (Payment_Key)
);

CREATE TABLE public.Fact_Taxi_Trips (
    Trip_ID bigserial NOT NULL,
    Date_Key integer,
    Vendor_Key integer,
    PU_Location_Key integer,
    DO_Location_Key integer,
    RateCode_Key integer,
    Payment_Key integer, 
    Store_and_fwd_flag varchar(3), 
    Passenger_Count integer,
    Trip_Distance numeric(10,2),
    Fare_Amount numeric(10,2),
    Extra numeric(10,2),
    MTA_Tax numeric(10,2),
    Tip_Amount numeric(10,2),
    Tolls_Amount numeric(10,2),
    Improvement_Surcharge numeric(10,2),
    Total_Amount numeric(10,2),
    Congestion_Surcharge numeric(10,2),
    
    CONSTRAINT Fact_Taxi_Trips_pk PRIMARY KEY (Trip_ID)
);

ALTER TABLE public.Fact_Taxi_Trips ADD CONSTRAINT Date_FK FOREIGN KEY (Date_Key)
REFERENCES public.Dim_Date (Date_Key);

ALTER TABLE public.Fact_Taxi_Trips ADD CONSTRAINT Vendor_FK FOREIGN KEY (Vendor_Key)
REFERENCES public.Dim_Vendor (Vendor_Key);

ALTER TABLE public.Fact_Taxi_Trips ADD CONSTRAINT PU_Location_FK FOREIGN KEY (PU_Location_Key)
REFERENCES public.Dim_Location (Location_Key);

ALTER TABLE public.Fact_Taxi_Trips ADD CONSTRAINT DO_Location_FK FOREIGN KEY (DO_Location_Key)
REFERENCES public.Dim_Location (Location_Key);

ALTER TABLE public.Fact_Taxi_Trips ADD CONSTRAINT Rate_FK FOREIGN KEY (RateCode_Key)
REFERENCES public.Dim_RateCode (RateCode_Key);

ALTER TABLE public.Fact_Taxi_Trips ADD CONSTRAINT Payment_FK FOREIGN KEY (Payment_Key)
REFERENCES public.Dim_Payment (Payment_Key);

```