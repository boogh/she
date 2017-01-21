import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SHE34.settings.base')

import django
django.setup()

from authtools.models import User
from HE2.models import Project

def populate():
    user_items=[{'email': 'user1@user1.com', 'password': 'user1', 'name': 'user1'},
                {'email': 'user2@user2.com', 'password': 'user2', 'name': 'user2'},
                {'email': 'user3@user3.com', 'password': 'user3', 'name': 'user3'},
                {'email': 'user4@user4.com', 'password': 'user4', 'name': 'user4'},
                {'email': 'user5@user5.com', 'password': 'user5', 'name': 'user5'},
                {'email': 'user6@user6.com', 'password': 'user6', 'name': 'user6'},
                {'email': 'user7@user7.com', 'password': 'user7', 'name': 'user7'},
                {'email': 'user8@user8.com', 'password': 'user8', 'name': 'user8'},]
    project_items = [{'name':'p1', 'description' : ' This is project 1', 'manager':'user1',
                    'evaluator' :['user2','user3','user4','user5' ] },
                   {'name': 'p2', 'description': ' This is project 2', 'manager': 'user2',
                    'evaluator': ['user1', 'user3', 'user4', 'user5']},
                   {'name': 'p3', 'description': ' This is project 3', 'manager': 'user3',
                    'evaluator': ['user1', 'user2', 'user4', 'user5']},
                   {'name': 'p4', 'description': ' This is project 4', 'manager': 'user4',
                    'evaluator': ['user1', 'user2', 'user3', 'user5']},
                   {'name': 'p5', 'description': ' This is project 5', 'manager': 'user1',
                    'evaluator': ['user2', 'user3', 'user4', 'user5']},
                   {'name': 'p6', 'description': ' This is project 6', 'manager': 'user2',
                    'evaluator': ['user1', 'user3', 'user4', 'user5']},
                   {'name': 'p7', 'description': ' This is project 7', 'manager': 'user1',
                    'evaluator': ['user2', 'user3', 'user4', 'user5']},
                   ]
    for user in user_items:
        addUser(user)

    for project in project_items:
        addProject(project)

def addUser(userdata):
    user = User.objects.get_or_create(email=userdata['email'] , password=userdata['password'] , name=userdata['name'])[0]
    user.save()
    print("Added User")

def addProject(projectData):
    project,create = Project.objects.get_or_create(name=projectData['name'], description = projectData['description'],
                                            manager=User.objects.get(name=projectData['manager']))
    project.save()
    for evaluator in projectData['evaluator']:
        project.evaluators.add(User.objects.get(name=evaluator))
    project.save()
    print('Added a Project')

if __name__ == '__main__':
    print('Running population script...')
    populate()