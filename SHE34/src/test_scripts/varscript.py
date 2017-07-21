from src.HE3.models import Project
from src.merg import recommend as rec

def script() :

    project = Project.objects.all()
    p1 = project.get(name ='p1')
    p2 = project.get(name ='p2')

    p1eval = p1.evaluation_for_project.all()
    p2eval = p2.evaluation_for_project.all()



    # rec.updateAllSearchModels()


    # print(rec.placebase(p1eval[0]))
    # print('----------------')
    # print(rec.placebase(p1eval[2]))
    # print('------------------')
    #
    # # rec.projectbase(p1eval[0])
    # # rec.projectbase(p1eval[2])
    # # rec.projectbase(p1eval[1])
    # print(rec.projectbase(p1eval[3]))


    sf = rec.getEvalSF(p1)
    tf = rec.evaltfidf(sf)
    tf