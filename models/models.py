from sqlalchemy import Column, Integer, String, Boolean, ARRAY, Float, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db.database import db

Base = declarative_base()

class IndustryType(db.Model):
    __tablename__ = "industry_type"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)

class ClimateType(db.Model):
    __tablename__ = "climate_type"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)

class Destination(db.Model):
    __tablename__ = "destination"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    country = Column(Integer, nullable=False)
    state = Column(String(100))
    currency = Column(Integer)
    dominant_language = Column(ARRAY(String(100)))
    predominant_religion = Column(String(200))
    cultural_objective = Column(String(1000))
    tolerance_level = Column(String(100))
    in_demand_occupations = Column(ARRAY(String(100)))
    labor_law = Column(String(1000))
    business_startup_requirement = Column(String(1000))
    has_tax_incentive = Column(Boolean)
    taxation = Column(String)
    living_cost = Column(ARRAY(Float))
    housing_cost_range = Column(ARRAY(Float))
    transportation_cost = Column(Float)
    affordability = Column(String(100))
    inflation_rate = Column(Float)
    climate_type_id = Column(Integer, ForeignKey('climate_type.id'))
    land_use_types = Column(ARRAY(String(100)))
    political_system = Column(String(100))
    healthcare_quality_ranking = Column(Integer)
    healthcare_quality = Column(String(1000))
    education_system = Column(String(1000))
    freedom_of_speech = Column(Boolean)
    safety_ranking = Column(Integer)
    is_lgbtq_friendly = Column(Boolean)
    lgbtq_rights = Column(String(1000))
    timezone = Column(String(20))
    currency_exchange_rate = Column(Float)

    climate_type = relationship(ClimateType, foreign_keys=[climate_type_id])

class LanguageType(db.Model):
    __tablename__ = "language_type"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)

class Users(db.Model):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = db.Column(db.Text)
    roles = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, server_default="true")
    
    @property
    def identity(self):
        return self.id

    @property
    def rolenames(self):
        try:
            return self.roles.split(",")
        except Exception:
            return []

    @property
    def password(self):
        return self.hashed_password
    
    @classmethod
    def lookup(cls, email):
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def identify(cls, id):
        return cls.query.get(id)

    def is_valid(self):
        return self.is_active


class UserProfile(db.Model):
    __tablename__ = "user_profile"
    
    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(250), nullable=False)
    born_date = Column(Date)
    phone = Column(String(100))
    credits = db.Column(db.Integer, default=0)
    language = db.Column(db.Text)
    
    users = relationship(Users, foreign_keys=[users_id])


class Client(db.Model):
    __tablename__ = "client"

    id = Column(Integer, primary_key=True)
    users_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    preferred_climate_type = Column(ARRAY(String(100)))
    preferred_language = Column(ARRAY(String(100)))
    current_country_of_residence = Column(Integer)
    citizenship_country = Column(Integer, nullable=False)
    education_type = Column(String(100))
    education_level = Column(String(250))
    preferred_living_cost_range = Column(ARRAY(Float))
    years_of_work_experience = Column(Integer)
    work_industry_id = Column(Integer, ForeignKey('industry_type.id'))
    investment_capital_available_range = Column(ARRAY(Float))
    marital_status = Column(String(100))
    number_of_dependant_accompanying = Column(Integer)
    is_entrepreneur = Column(Boolean)
    military_service_status = Column(String(100))
    has_criminal_record = Column(Boolean)
    language_ability = Column(ARRAY(String(100)))
    preferred_industry_id = Column(Integer, ForeignKey('industry_type.id'))
    health_status = Column(String(1000))

    work_industry = relationship(IndustryType, foreign_keys=[work_industry_id])
    preferred_industry = relationship(IndustryType, foreign_keys=[preferred_industry_id])
    users = relationship(Users, foreign_keys=[users_id])

class VisaProgram(db.Model):
    __tablename__ = "visa_program"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(String(3000))
    destination_id = Column(Integer, ForeignKey('destination.id'))

class Country(db.Model):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
