from models.models import UserProfile, Client, Country, IndustryType, LanguageType, ClimateType
from db.database import db
from datetime import date
from sqlalchemy import select, text, func
from sqlalchemy.sql.expression import join


def get_user_info(id, app):
    data = {}
    with app.app_context():
        # in join with climatetype, but the preferred climate in the Client table is a JSON field
        # so we need to convert it to text to join with the ClimateType table
        query = select(Client, UserProfile, Country, IndustryType).where(Client.users_id == id)\
            .join(UserProfile, Client.users_id == UserProfile.users_id)\
            .join(Country, Client.citizenship_country == Country.name)\
            .join(IndustryType, Client.work_industry == IndustryType.name)  
            
            # .join(ClimateType, ClimateType.name.in_(func.json_array_agg(Client.preferred_climate_type).cast(text('text'))))
            # .join(ClimateType, Client.preferred_climate_type == ClimateType.name)
        
        result = db.session.execute(query).fetchone()
        if not result:
            return None
        
        client = result[0]
        user_profile = result[1]
        country = result[2]
        industry = result[3]

        if user_profile.born_date is not None:
            today = date.today()
            age = today.year - user_profile.born_date.year - ((today.month, today.day) < (user_profile.born_date.month, user_profile.born_date.day))
            data['age'] = age
        
        if country.title is not None:
            data['citizenship'] = country.title

        if client.marital_status is not None:
            data['marital_status'] = client.marital_status

        if client.number_of_dependant_accompanying is not None:
            data['number_of_dependant_accompanying'] = client.number_of_dependant_accompanying

        if client.is_entrepreneur is not None:
            data['is_entrepreneur'] = client.is_entrepreneur

        if client.military_service_status is not None:
            data['military_service_status'] = client.military_service_status

        if client.has_criminal_record is not None:
            data['has_criminal_record'] = client.has_criminal_record
        
        if client.education_type is not None:
            data['education_in_home_country'] = client.education_type
        
        if client.education_level is not None:
            data['education_level_in_home_country'] = client.education_level
        
        if client.preferred_living_cost_range is not None:
            data['preferred_living_cost_range'] = client.preferred_living_cost_range
        
        if client.investment_capital_available_range is not None:
            data['investment_capital_available_range'] = client.investment_capital_available_range
        
        if client.years_of_work_experience is not None:
            data['years_of_work_experience_in_home_country'] = client.years_of_work_experience
        
        if client.preferred_climate_type is not None:
            data['preferred_climate'] = client.preferred_climate_type
        
        if industry.title is not None:
            data['working_industry_in_home_country'] = industry.title
        
        # if client.preferred_industry_alias is not None:
        #     data['preferred_industry'] = client.preferred_industry_alias
        
        if client.language_ability is not None:
            data['language_ability'] = client.language_ability

        if client.preferred_language is not None:
            data['preferred_language'] = client.preferred_language

        if client.health_status is not None:
            data['health_status'] = client.health_status

        return data
