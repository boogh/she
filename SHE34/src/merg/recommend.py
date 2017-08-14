import graphlab as gl
from HE3.models import Project

allprojects = Project.objects.all()
projectsSearchModelsDic = {}
projectsNNmodels ={}

def getEvalSF(project):
    '''
    A method which get a project and return a SFrame of it`s evaluations
    :param project:
    :return: A SFrame of Evaluation in the project
    '''

    evaldic = [e.__dict__ for e in project.evaluation_for_project.all()]

    evalsf = gl.SFrame()
    evalsf['id'] = [str(i['id']) for i in evaldic]
    evalsf['title'] = [i['title'] for i in evaldic]
    evalsf['place'] = [i['place'] for i in evaldic]
    # evalsf['a_place'] = [i['a_place'] for i in evaldic]
    evalsf['description'] = [i['description'] for i in evaldic]
    evalsf['recommendation'] = [i['recommendation'] for i in evaldic]
    evalsf['tags'] = [i['tags'] for i in evaldic]
    # evalsf['heurPrincip_id'] = [str(i['heurPrincip_id']) for i in evaldic]

    return evalsf

def evaltfidf(project):
    '''
    A Method which get a project and add TFIDF column for description, recommendation and tags
    :param project:
    :return:
    '''
    evalsf = getEvalSF(project)
    evalsf['desWordCount'] = gl.text_analytics.count_words(evalsf['description'])
    evalsf['recommendation'] = gl.text_analytics.count_words(evalsf['recommendation'])
    evalsf['tagsWordCount'] = gl.text_analytics.count_words(evalsf['tags'])
    tfidfDes = gl.text_analytics.tf_idf(evalsf['desWordCount'])
    tfidfRec = gl.text_analytics.tf_idf(evalsf['recommendation'])
    tfidfTags = gl.text_analytics.tf_idf(evalsf['tagsWordCount'])
    evalsf['tfidfDes'] = tfidfDes
    evalsf['tfidfRec'] = tfidfRec
    evalsf['tfidfTags'] = tfidfTags

    return evalsf
def getPlaceSF(project):
    '''
    A method which get a project and return a SFrame of it`s evaluations
    :param project:
    :return: A SFrame of Evaluation in the project
    '''

    evaldic = [e.__dict__ for e in project.evaluation_for_project.all()]

    evalsf = gl.SFrame()
    evalsf['id'] = [str(i['id']) for i in evaldic]
    # evalsf['title'] = [i['title'] for i in evaldic]
    evalsf['place'] = [i['place'] for i in evaldic]
    # evalsf['a_place'] = [i['a_place'] for i in evaldic]
    # evalsf['description'] = [i['description'] for i in evaldic]
    # evalsf['recommendation'] = [i['recommendation'] for i in evaldic]
    evalsf['tags'] = [i['tags'] for i in evaldic]
    # evalsf['heurPrincip_id'] = [str(i['heurPrincip_id']) for i in evaldic]

    return evalsf

def placebase(eval):

    project = eval.ofProject
    # updateAllSearchModels()
    # result = projectsSearchModelsDic[project.id]['placeSearchModel'].query(eval.place)
    sf= getPlaceSF(project)
    placeSearchModel = gl.toolkits._internal.search.create(sf , features= ['id','place' ,'tags'])
    result = placeSearchModel.query(eval.place).filter_by(str(eval.id) , 'id' , exclude= True)
    return  list(result['id'])



# def descriptionBase(eval):
#     '''
#     A Method which give similar evaluations to a given evaluatioln
#     :param eval: An evaluation
#     :return: SFrame with similar evalautions
#     '''
#
#     evalsf = evaltfidf(eval.ofProject)
#     evalrow = evalsf[evalsf['id'] == str(eval.id)]
#     # model = projectsNNmodels[eval.ofProject.id]['nnDesModel']
#     model = gl.nearest_neighbors.create(evalsf, features=['tfidfDes'], label='id')
#     result = model.query(evalrow).filter_by(str(eval.id) , 'reference_label' , exclude= True)
#     print(result)
#     result = result[result['distance'] <= 0.6]['reference_label']
#     return list(result)


def nearestN(eval):
    '''
    A Method which give similar evaluations to a given evaluatioln based on NN algorithm
    :param eval: An evaluation
    :return: SFrame with similar evalautions
    '''

    evalsf = evaltfidf(eval.ofProject)
    evalrow = evalsf[evalsf['id'] == str(eval.id)]
    # model = projectsNNmodels[eval.ofProject.id]['nnDesModel']
    modelDes = gl.nearest_neighbors.create(evalsf, features=['tfidfDes'], label='id')
    modelRec = gl.nearest_neighbors.create(evalsf, features=['tfidfRec'], label='id')
    modelTags = gl.nearest_neighbors.create(evalsf, features=['tfidfTags'], label='id')
    resultDes = modelDes.query(evalrow).filter_by(str(eval.id) , 'reference_label' , exclude= True)
    resultRec = modelRec.query(evalrow).filter_by(str(eval.id) , 'reference_label' , exclude= True)
    resultTags = modelTags.query(evalrow).filter_by(str(eval.id) , 'reference_label' , exclude= True)
    resultDes = resultDes[resultDes['distance'] <= 0.85]['reference_label']
    resultRec = resultRec[resultRec['distance'] <= 0.85]['reference_label']
    resultTags = resultTags[resultTags['distance'] <= 0.85]['reference_label']

    result = {'resultDes' : resultDes ,
              'resultRec' : resultRec ,
              'resultTags': resultTags,}

    return result

# def updateSearchModels(project):
#
#     projectSF = getEvalSF(project)
#     print('hier')
#     placeSearchModel = gl.toolkits._internal.search.create(projectSF , features= ['id','place'])
#     # titleSearchModel = gl.toolkits._internal.search.create(projectSF, features=projectSF['title'])
#     # descSearchModel = gl.toolkits._internal.search.create(projectSF, features=projectSF['description'])
#     # recomSearchModel = gl.toolkits._internal.search.create(projectSF, features=projectSF['recommendation'])
#     # tagsSearchModel = gl.toolkits._internal.search.create(projectSF, features=projectSF['tags'])
#     projectSearchModel = gl.toolkits._internal.search.create(projectSF , features = projectSF.column_names()[0:-1] )
#
#     models = {'placeSearchModel' : placeSearchModel,
#               'projectSearchModel' : projectSearchModel,
#               # 'titleSearchModel' : titleSearchModel ,
#               # 'descSearchModel'  : descSearchModel  ,
#               # 'recomSearchModel' : recomSearchModel ,
#               #  'tagsSearchModel' : tagsSearchModel ,
#               }
#
#     return  models

# def updateAllSearchModels():
#     p1 = allprojects.get(name='p1')
#     p2 = allprojects.get(name='p2')
#     # for p in allprojects:
#     # print( '1' + p.name + '  start building searchmodel')
#     projectsSearchModelsDic.update({p1.id  :updateSearchModels(p1)})
#     projectsSearchModelsDic.update({p2.id : updateSearchModels(p2)})
#     # print('4'+ p.name + '  finish building searchmodel')



# def projectbase( project , query):
#
#     project = eval.ofProject
#     # result = projectsSearchModelsDic[project.id]['projectSearchModel'].query(eval.place)
#     # result = updateSearchModels(project)
#     sf = getEvalSF(project)
#     projectSearchModel = gl.toolkits._internal.search.create(sf , features = sf.column_names()[0:-1] )
#     return projectSearchModel.query(s)


# def updateNNmodels(project):
#     sf = evaltfidf(project)
#     nnRec = gl.nearest_neighbors.create(sf, features=['tfidfRec'], label='id')
#     nnDes = gl.nearest_neighbors.create(sf, features=['tfidfDes'], label='id')
#     nnTags = gl.nearest_neighbors.create(sf, features=['tfidfTags'], label='id')
#
#     modeldic = {'nnRecModel' : nnRec ,
#                 'nnDesModel' : nnDes ,
#                 'nnTagsModel': nnTags}
#     return modeldic

# def updataAllNNmodels():
#     # for p in allprojects:
#     p1 = allprojects.get(name='p1')
#     p2 = allprojects.get(name='p2')
#     projectsNNmodels.update({ p1.id : updateNNmodels(p1)})
#     projectsNNmodels.update({ p2.id : updateNNmodels(p2)})



# if __name__ == '__main__':
#     print('Running index update script...')
#     updateAllSearchModels()
#     updataAllNNmodels()
#
#
#
