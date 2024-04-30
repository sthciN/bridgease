from .models import (
    IndustryType,
    ClimateType,
    Destination,
    LanguageType,
    Users,
    UserProfile,
    Client,
    VisaProgram,
    Country,
    ClientVisaPrograms
)
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import fields

class IndustryTypeSchema(SQLAlchemySchema):
    class Meta:
        model = IndustryType
        include_relationships = True
        load_instance = True

    id = auto_field()
    title = auto_field()

class ClimateTypeSchema(SQLAlchemySchema):
    class Meta:
        model = ClimateType
        include_relationships = True
        load_instance = True

    id = auto_field()
    title = auto_field()

class LanguageTypeSchema(SQLAlchemySchema):
    class Meta:
        model = LanguageType
        include_relationships = True
        load_instance = True

    id = auto_field()
    title = auto_field()

class DestinationSchema(SQLAlchemySchema):
    class Meta:
        model = Destination
        include_relationships = True
        load_instance = True

    id = auto_field()
    name = auto_field()
    country = auto_field()
    state = auto_field()
    currency = auto_field()
    dominant_language = auto_field()
    predominant_religion = auto_field()
    cultural_objective = auto_field()
    tolerance_level = auto_field()
    in_demand_occupations = auto_field()
    labor_law = auto_field()
    business_startup_requirement = auto_field()
    has_tax_incentive = auto_field()
    taxation = auto_field()
    living_cost = auto_field()
    housing_cost_range = auto_field()
    transportation_cost = auto_field()
    affordability = auto_field()
    inflation_rate = auto_field()
    climate_type = auto_field()
    land_use_types = auto_field()
    political_system = auto_field()
    healthcare_quality_ranking = auto_field()
    healthcare_quality = auto_field()
    education_system = auto_field()
    freedom_of_speech = auto_field()
    safety_ranking = auto_field()
    is_lgbtq_friendly = auto_field()
    lgbtq_rights = auto_field()
    timezone = auto_field()
    currency_exchange_rate = auto_field()

class UsersSchema(SQLAlchemySchema):
    class Meta:
        model = Users
        include_relationships = True
        load_instance = True
    
    email = auto_field()
    role = 'user'

class UserProfileSchema(SQLAlchemySchema):
    class Meta:
        model = UserProfile
        include_relationships = True
        load_instance = True
    firstName = fields.String(attribute="first_name")
    lastName = fields.String(attribute="last_name")
    bornDate = fields.Date(attribute="born_date")
    phone = auto_field()
    credits = auto_field()
    language = auto_field()
    
class ClientSchema(SQLAlchemySchema):
    class Meta:
        model = Client
        include_relationships = True
        load_instance = True

    preferred_climate_type = auto_field()
    preferred_language = auto_field()
    current_country_of_residence = auto_field()
    citizenship_country = auto_field()
    education_type = auto_field()
    education_level = auto_field()
    preferred_living_cost_range = auto_field()
    years_of_work_experience = auto_field()
    work_industry = auto_field()
    investment_capital_available_range = auto_field()
    marital_status = auto_field()
    number_of_dependant_accompanying = auto_field()
    is_entrepreneur = auto_field()
    military_service_status = auto_field()
    has_criminal_record = auto_field()
    language_ability = auto_field()
    preferred_industry = auto_field()
    health_status = auto_field()
    
    users = auto_field()

class ClientBasicInformationSchema(SQLAlchemySchema):
    class Meta:
        model = Client
        include_relationships = True
        load_instance = True

    countryOfResidence = fields.String(attribute="current_country_of_residence")
    countryOfCitizenship = fields.String(attribute="citizenship_country")
    fieldOfStudy = fields.String(attribute="education_type")
    educationDegree = fields.String(attribute="education_level")
    yearsOfExperience = fields.String(attribute="years_of_work_experience")
    workingIndustry = fields.String(attribute="work_industry")
    languages = fields.String(attribute="language_ability")

class ClientFamilyInformationSchema(SQLAlchemySchema):
    class Meta:
        model = Client
        include_relationships = True
        load_instance = True

    maritalStatus = fields.String(attribute="marital_status")
    noOfDependentAccompanyingYou = fields.String(attribute="number_of_dependant_accompanying")
    militaryServiceStatus = fields.String(attribute="military_service_status")
    haveCriminalRecord = fields.String(attribute="has_criminal_record")

class ClientBusinessInformationSchema(SQLAlchemySchema):
    class Meta:
        model = Client
        include_relationships = True
        load_instance = True

    investmentCapitalAvailableRange = fields.String(attribute="investment_capital_available_range")
    isEntrepreneuer = fields.String(attribute="is_entrepreneur")

class ClientPreferenceInformationSchema(SQLAlchemySchema):
    class Meta:
        model = Client
        include_relationships = True
        load_instance = True

    preferredClimate = fields.List(fields.String(), attribute="preferred_climate_type")
    preferredLanguage = fields.List(fields.String(), attribute="preferred_language")
    preferredLivingCostRange = fields.String(attribute="preferred_living_cost_range")
    preferredIndustry = fields.String(attribute="preferred_industry")

class VisaProgramSchema(SQLAlchemySchema):
    class Meta:
        model = VisaProgram
        include_relationships = True
        load_instance = True
    
    doc_id = auto_field()
    title = auto_field()
    country = auto_field()
    description = auto_field()

class CountrySchema(SQLAlchemySchema):
    class Meta:
        model = Country
        include_relationships = True
        load_instance = True

    id = fields.Integer(attribute="id")
    title = fields.String(attribute="title")

class ClientVisaProgramsSchema(SQLAlchemySchema):
    class Meta:
        model = ClientVisaPrograms
        include_relationships = True
        load_instance = True

    visaPrograms = fields.String(attribute="visa_programs")

class ClientVisaTimelineSchema(SQLAlchemySchema):
    class Meta:
        model = ClientVisaPrograms
        include_relationships = True
        load_instance = True

    doc_id = fields.Integer(attribute="doc_id")
    timeline = fields.String(attribute="timeline")
