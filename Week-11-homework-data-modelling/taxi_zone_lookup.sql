CREATE SCHEMA IF NOT EXISTS taxi_zone_lookup;

CREATE TABLE taxi_zone_lookup.Dim_Date (
    Date_Key integer NOT NULL,
    Full_Date date NOT NULL,
    Day_Name varchar(20),
    Is_Weekend boolean,
    Month_Name varchar(20),
    Year integer,
    CONSTRAINT Dim_Date_pk PRIMARY KEY (Date_Key)
);

CREATE TABLE taxi_zone_lookup.Dim_Location (
    Location_Key serial NOT NULL,
    LocationID integer NOT NULL,
    Borough varchar(100),
    Zone varchar(100),
    Service_Zone varchar(100),
    CONSTRAINT Dim_Location_pk PRIMARY KEY (Location_Key)
);

CREATE TABLE taxi_zone_lookup.Dim_Vendor (
    Vendor_Key serial NOT NULL,
    VendorID integer,
    Vendor_Name varchar(100),
    CONSTRAINT Dim_Vendor_pk PRIMARY KEY (Vendor_Key)
);

CREATE TABLE taxi_zone_lookup.Dim_RateCode (
    RateCode_Key serial NOT NULL,
    RateCodeID integer,
    Rate_Description varchar(100),
    CONSTRAINT Dim_RateCode_pk PRIMARY KEY (RateCode_Key)
);

CREATE TABLE taxi_zone_lookup.Dim_Payment (
    Payment_Key serial NOT NULL,
    Payment_Type_ID integer,
    Payment_Name varchar(50),
    CONSTRAINT Dim_Payment_pk PRIMARY KEY (Payment_Key)
);

CREATE TABLE taxi_zone_lookup.Fact_Taxi_Trips (
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


ALTER TABLE taxi_zone_lookup.Fact_Taxi_Trips ADD CONSTRAINT Date_FK FOREIGN KEY (Date_Key)
REFERENCES taxi_zone_lookup.Dim_Date (Date_Key);

ALTER TABLE taxi_zone_lookup.Fact_Taxi_Trips ADD CONSTRAINT Vendor_FK FOREIGN KEY (Vendor_Key)
REFERENCES taxi_zone_lookup.Dim_Vendor (Vendor_Key);

ALTER TABLE taxi_zone_lookup.Fact_Taxi_Trips ADD CONSTRAINT PU_Location_FK FOREIGN KEY (PU_Location_Key)
REFERENCES taxi_zone_lookup.Dim_Location (Location_Key);

ALTER TABLE taxi_zone_lookup.Fact_Taxi_Trips ADD CONSTRAINT DO_Location_FK FOREIGN KEY (DO_Location_Key)
REFERENCES taxi_zone_lookup.Dim_Location (Location_Key);

ALTER TABLE taxi_zone_lookup.Fact_Taxi_Trips ADD CONSTRAINT Rate_FK FOREIGN KEY (RateCode_Key)
REFERENCES taxi_zone_lookup.Dim_RateCode (RateCode_Key);

ALTER TABLE taxi_zone_lookup.Fact_Taxi_Trips ADD CONSTRAINT Payment_FK FOREIGN KEY (Payment_Key)
REFERENCES taxi_zone_lookup.Dim_Payment (Payment_Key);