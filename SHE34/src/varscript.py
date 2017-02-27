from HE3.models import Project
from merg import recommend as rec

project = Project.objects.all()
p1 = project.get(name ='p1')
p2 = project.get(name ='p2')

p1eval = p1.evaluation_for_project.all()
p2eval = p2.evaluation_for_project.all()



rec.updateAllSearchModels()
rec.placebase(p1eval[0])
rec.placebase(p1eval[2])

rec.projectbase(p1eval[0])
rec.projectbase(p1eval[2])
rec.projectbase(p1eval[1])
rec.projectbase(p1eval[3])