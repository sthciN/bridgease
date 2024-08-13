# Bridgease

## Bridgease Backend

Bridgease is a Flask-based backend application designed to help users navigate immigration options. The app collects various user details through forms, processes the data, and recommends the top 5 visa programs that best match each user's profile.

The application leverages a Large Language Model (LLM) from OpenAI to identify the most relevant visa programs for users. By analyzing the user's information, the LLM generates personalized content explaining why specific visa programs are suitable for them.

Each user is allotted a certain number of credits, which they can purchase. One credit is deducted each time a user inquires about visa programs.

## Features

- **User Profiles**: Users can create profiles containing basic information, education, work experience, skills, language abilities, climate preferences, preferred living costs, marital status, health status, country of origin, and more.

- **Visa Program Recommendations**: The application generates a list of the top 5 visa programs tailored to the user based on their provided information. Each recommendation includes the program title, a link, a description, and a personalized explanation of why it is a good fit.

## Tech Stack

- **Flask**: A lightweight WSGI web framework used to build the backend of the application.
- **SQLAlchemy**: A Python SQL toolkit and Object-Relational Mapping (ORM) library used for database management.

## Setup

To run this project locally, install the required dependencies and start the application with:

```bash
$ flask run
```

or

```bash
$ python main.py
```

## Routes

The Bridgease backend provides various API endpoints for managing user authentication, profiles, visa processes, credits, and other functionalities. Below is a list of available routes organized by their respective categories:

### User

#### Authentication
- **Register**: `POST /register`  
  Register a new user.

- **Login**: `POST /login`  
  Authenticate a user and generate a token.

- **Logout**: `POST /logout`  
  Log out the authenticated user.

- **Update Password**: `PUT /update_password`  
  Update the user's password.

- **Refresh Token**: `GET /user/refresh-token`  
  Refresh the user's authentication token.

#### Profile Management
- **Language Preference**: `GET /user/language`  
  Get or update the user's language preference.

- **User Profile**: `GET /user-profile`  
  Retrieve the user's profile.

- **Profile Information**: `GET /user-personal-info`  
  Retrieve the user's personal information.

#### Forms
- **Basic Information**: `GET PUT /client-basic-information`  
  Get, Submit or update basic user information.

- **Family Information**: `GET PUT /client-family-information`  
  Get, Submit or update user family information.

- **Business Information**: `GET PUT /user-business-information`  
  Get, Submit or update business-related user information.

- **Preference Information**: `GET PUT /user-preference-information`  
  Get, Submit or update user preferences.

### Visa

- **Create Timeline Assistant**: `GET /user/create_timeline_assistant`  
  Create a timeline assistant for the visa process.

- **Reprocess Visa Card**: `GET /user/reprocess-visa-card`  
  Reprocess the user's visa card.

- **Process Visa Card**: `GET /user/process-visa-card`  
  Process the user's visa card.

- **Visa Card**: `GET /user/visa-card`  
  Retrieve the user's visa card.

- **Process Timeline**: `GET /user/process-timeline/<string:id>`  
  Process the timeline for the visa with a specific ID.

- **Timeline**: `GET /user/timeline/<string:id>`  
  Retrieve the timeline for the visa with a specific ID.

- **Visa Program**: `GET /user/visa-program/<string:id>`  
  Retrieve information about a specific visa program.

### Credit

- **Buy Plan**: `POST /user/<int:id>/buy_plan`  
  Purchase a credit plan for the user with a specific ID.

- **Add Credit**: `POST /user/<int:id>/add_credits`  
  Add credits to the user's account with a specific ID.

- **Stripe Webhook**: `POST /webhook`  
  Handle Stripe payment webhook events.

### Miscellaneous

- **Countries**: `GET /countries`  
  Retrieve a list of supported countries.



#### Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

License
This project is licensed under the MIT License.

