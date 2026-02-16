
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from config import Config

# Create engine
engine = create_engine(Config.DATABASE_URL)

# Create session
Session = sessionmaker(bind=engine)

# Base class
Base = declarative_base()


class JobCard(Base):
    __tablename__ = "job_cards"

    id = Column(Integer, primary_key=True)

    Registration_No = Column(String)
    odometer_reading = Column(String)
    avg_kms_perday = Column(String)
    VIN = Column(String)
    Engine_No = Column(String)

    Make = Column(String)
    model = Column(String)
    year = Column(String)
    variant = Column(String)
    fuel_type = Column(String)
    vehicle_color = Column(String)

    service_type = Column(String)
    service_advisor_name = Column(String)
    Source = Column(String)
    Advisor = Column(String)
    Technician = Column(String)
    Estimated_Delivery_Date = Column(String)

    customer_name = Column(String)
    mobile_number = Column(String)
    Alternative_Contact_Number = Column(String)
    Email_ID = Column(String)

    Contact_Name_OR_Driver_Name = Column(String)
    Flat_House_No = Column(String)
    Colony_Street_Location = Column(String)
    Town_city = Column(String)
    state = Column(String)
    pincode = Column(String)


# Create tables automatically
Base.metadata.create_all(engine)
