import json
from . import create_app
from .extensions import db
from .models import User, ROLES, Course, Page, Setting



def generate_users():
    admin = User(email='admin@site.com', 
            password='admin',
            username='admin', 
            full_name='Administrator',
            confirmed=True,
            role=ROLES['developer'])
    db.session.add(admin)
    db.session.commit()
    print('Users Added')

def generate_courses():
    #courses = [{'name': 'Tailoring', 'body': 'lorem ipsum', 'description': 'about tailoring', 'lead': 'something about this course'}]

    for k in courses:
        course = Course(name=k['name'], body=k['body'], description=k['description'], lead=k['lead'])
        db.session.add(course)
    db.session.commit()
    print('Courses added')

def generate_pages():
    #pages = [{'name': 'About us', 'body': 'About Us', 'lead': 'Some adertising text'}]

    for k in pages:
        page = Page(name=k['name'], body=k['body'], lead=k['lead'])
        db.session.add(page)
    db.session.commit()
    print('Pages added')

def generate_settings():

    for k in settings:
        setting = Setting(name=k['name'], value=k['value'])
        db.session.add(setting)
    db.session.commit()
    print('Settings added')

def setup_db():
    db.drop_all()
    db.create_all()
    generate_users()
    generate_courses()
    generate_pages()
    generate_settings()
    print('DB setup')

pages = [
	{
		"name": "About Us",
		"body": """Innovation in technology influences how we live as much as any other aspect of modern life. Computers perform increasingly complex tasks that have the potential to improve our lives in ways we could have never imagined. Read on to learn about five employment areas where you can turn a love of computers into a career. 		

Computer scientists are highly trained professionals who create new technologies. These advances might be in hardware functionality or other computing improvements. Discoveries are also sought in robotics, virtual reality and other relatively new technological areas that are only now being fully explored. 

Computer scientists often perform research on computing processes and work to make them more efficient or innovative. These professionals may work with others, including mechanical and electrical engineers, to solve technological dilemmas. 

""",
		"lead": "Why choose us, some marketing text"
	},
	{
		"name": "Apply",
		"body": "recognised for its delivery of industry-relevant programmes. It cultivates strong partnerships with the world’s top brands in order to maintain a dynamic industry-relevant curriculum focussing on the development of skills and experiences that prepares students to face real world expectations. Our global graduates are ensured of a smooth transition into new and exciting high-income careers anywhere in the world.i recognised for its delivery of industry-relevant programmes. It cultivates strong partnerships with the world’s top brands in order to maintain a dynamic industry-relevant curriculum focussing on the development of skills and experiences that prepares students to face real world expectations. Our global graduates are ensured of a smooth transition into new and exciting high-income careers anywhere in the world.",
		"lead": "Apply today to start your dream job"
	}
		
]

courses = [
	{
            "name":"Refrigiration & Air Conditioning", 
            "body": """Air conditioning professionals are often tasked with installing, maintaining and repairing heating, ventilation and air conditioning (HVAC) systems in residential or commercial buildings. They can receive training through certificate a program.



Although some heating, ventilation and air conditioning (HVAC) professionals receive their training on the job or through 3- to 5-year apprenticeships, many learn their trade through 6-month to 2-year HVAC certificate or associate's degree programs. These programs include air conditioning courses and are usually offered at 2-year technical colleges or trade schools. 

Here are common concepts found in air conditioning classes: 

* Diagnostics Technology 
* Building systems 
* Basic electricity Industrial controls 
* Customer service Communication 

HVAC students can go on to become HVAC installers, technicians or project coordinators. Some employers look specifically for industry-certified HVAC professionals and some states require licensing, though specific requirements vary. Those technicians who handle refrigerants - like those found in air conditioners - must be certified by by passing  the certification exams. 

""",
            "description": """Although some heating, ventilation and air conditioning (HVAC) professionals receive their training on the job or through 3- to 5-year apprenticeships, many learn their trade through 6-month to 2-year HVAC certificate or associate's degree programs. These programs include air conditioning courses and are usually offered at 2-year technical colleges or trade schools. 
""",
            "lead": "Start a business in air Conditioning & Refrigiration today"
	},
	{
            "name":"Electrical Fitting & Installation",
            "body": "fill me in",
            "description": "fill me in",
            "lead": "fill me in"
	},
	{
            "name":"Welding & Fabrication",
            "body": """Vocational schools and community colleges offer welding programs leading to diplomas, certificates or associate's degrees. Not as common, but available are bachelor's degree programs in welding. Most welding classes allow students to practice the skills they've acquired in the classroom in a supervised shop environment. 

Programs could offer majors in areas such as welding technology, basic welding, pipe welding, flux core welding and gas metal arc welding. The diploma and certificate programs feature core welding classes, while degree programs include general education, core welding and elective topics. Some schools offer day and evening programs to accommodate students' schedules. 

Here are some common concepts taught in welding courses: 

* Electric shock Fumes 
* STICK welding 
* Joint preparation 
* Electrode selection 
* Technical drawing 
* Architectural drafting 

""",
            "description": """We offer welding technology, basic welding, pipe welding, flux core welding and gas metal arc welding. The diploma and certificate programs feature core welding classes, while degree programs include general education, core welding and elective topics. Some schools offer day and evening programs to accommodate students' schedules.""",
            "lead": "Learn by doing, and from the best in the industry"
	},
	{
            "name":"Moto Vehicle Repair & Maintanance",
            "body": "fill me in",
            "description": "fill me in",
            "lead": "fill me in"
	},
	{
            "name":"Carpentry & Wood Joinery",
			"body": "fill me in",
			"description": "fill me in",
			"lead": "fill me in"
	},
	{"name":"Computer Repair & Maintanance",
			"body": """Innovation in technology influences how we live as much as any other aspect of modern life. Computers perform increasingly complex tasks that have the potential to improve our lives in ways we could have never imagined. Read on to learn about five employment areas where you can turn a love of computers into a career. 		

Computer scientists are highly trained professionals who create new technologies. These advances might be in hardware functionality or other computing improvements. Discoveries are also sought in robotics, virtual reality and other relatively new technological areas that are only now being fully explored. 

Computer scientists often perform research on computing processes and work to make them more efficient or innovative. These professionals may work with others, including mechanical and electrical engineers, to solve technological dilemmas. 

""",
                        "description": """Computer scientists often perform research on computing processes and work to make them more efficient or innovative. These professionals may work with others, including mechanical and electrical engineers, to solve technological dilemma""",
			"lead": "fill me in"
	},
	{"name":"Brick Laying & Construction",
			"body": "fill me in",
			"description": "fill me in",
			"lead": "fill me in"
	},
	{"name":"Hair dressing",
			"body": "fill me in",
			"description": "fill me in",
			"lead": "fill me in"
	},
	{"name":"Tailoring", 
			"body": "fill me in",
			"description": "fill me in",
			"lead": "fill me in"
	}
]

settings = [
	{"name": "app_name", "value": "Equip youth Africa"},
        {"name": "navigation", "value": ""},
	{"name": "widget_hero", "value":"" },
        {"name": "widget_intro", "value": ""},
	{"name": "widget_features", "value": ""},
	{"name": "widget_teaser", "value": ""},
	{"name": "contacts", "value": ""}	
]
