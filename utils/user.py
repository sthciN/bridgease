from models.models import UserProfile, Client, Country, IndustryType, LanguageType
from db.database import db
from datetime import date

def get_user_info(id):
    data = {}
    user = db.session.query(UserProfile).filter(UserProfile.id == id).first()
    client = db.session.query(Client).filter(Client.user_profile_id == id).first()
    
    if user.born_date is not None:
        today = date.today()
        age = today.year - user.born_date.year - ((today.month, today.day) < (user.born_date.month, user.born_date.day))
        data['age'] = age
    
    if client.citizenship_country is not None:
        citizenship = db.session.query(Country).filter(Country.id == client.citizenship_country).first().title
        data['citizenship'] = citizenship
    
    if client.current_country_of_residence is not None:
        residence = db.session.query(Country).filter(Country.id == client.current_country_of_residence).first().title
        data['residence'] = residence
    
    if client.education_type is not None:
        education = client.education_type
        data['education'] = education
    
    if client.education_level is not None:
        level = client.education_level
        data['level'] = level
    
    if client.years_of_work_experience is not None:
        experience = client.years_of_work_experience
        data['experience'] = experience
    
    if client.work_industry_id is not None:
        industry = db.session.query(IndustryType).filter(IndustryType.id == client.work_industry_id).first().title
        data['industry'] = industry
    
    if client.preferred_language is not None:
        language = db.session.query(LanguageType).filter(LanguageType.id in client.preferred_language).all()
        data['language'] = 'and'.join([l.title for l in language])
    
    return data