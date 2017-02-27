import graphlab as gl
from HE3.models import Project

allprojects = Project.objects.all()
projectsSearchModelsDic = {}

def getEvalSF(project):


    evaldic = [e.__dict__ for e in project.evaluation_for_project.all()]

    evalsf = gl.SFrame()
    evalsf['id'] = [str(i['id']) for i in evaldic]
    evalsf['title'] = [i['title'] for i in evaldic]
    evalsf['place'] = [i['place'] for i in evaldic]
    evalsf['description'] = [i['description'] for i in evaldic]
    evalsf['recommendation'] = [i['recommendation'] for i in evaldic]
    evalsf['tags'] = [i['tags'] for i in evaldic]
    evalsf['heurPrincip_id'] = [str(i['heurPrincip_id']) for i in evaldic]

    return evalsf

def updateSearchModels(project):

    projectSF = getEvalSF(project)
    print('hier')
    placeSearchModel = gl.toolkits._internal.search.create(projectSF , features= ['id','place'])
    # titleSearchModel = gl.toolkits._internal.search.create(projectSF, features=projectSF['title'])
    # descSearchModel = gl.toolkits._internal.search.create(projectSF, features=projectSF['description'])
    # recomSearchModel = gl.toolkits._internal.search.create(projectSF, features=projectSF['recommendation'])
    # tagsSearchModel = gl.toolkits._internal.search.create(projectSF, features=projectSF['tags'])
    projectSearchModel = gl.toolkits._internal.search.create(projectSF , features = projectSF.column_names()[0:-1] )

    models = {'placeSearchModel' : placeSearchModel,
              'projectSearchModel' : projectSearchModel,
              # 'titleSearchModel' : titleSearchModel ,
              # 'descSearchModel'  : descSearchModel  ,
              # 'recomSearchModel' : recomSearchModel ,
              #  'tagsSearchModel' : tagsSearchModel ,
              }

    return  models

def updateAllSearchModels():
    p1 = allprojects.get(name='p1')
    p2 = allprojects.get(name='p2')
    # for p in allprojects:
        # print( '1' + p.name + '  start building searchmodel')
    projectsSearchModelsDic.update({p1.id  :updateSearchModels(p1)})
    projectsSearchModelsDic.update({p2.id : updateSearchModels(p2)})
        # print('4'+ p.name + '  finish building searchmodel')

def placebase(eval):

    project = eval.ofProject
    result = projectsSearchModelsDic[project.id]['placeSearchModel'].query(eval.place)
    return result


def projectbase(eval):

    project = eval.ofProject
    result = projectsSearchModelsDic[project.id]['projectSearchModel'].query(eval.place)
    return result


if __name__ == '__main__':
    print('Running index update script...')
    updateAllSearchModels()