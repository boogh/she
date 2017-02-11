import django_tables2 as tables
from .models import Evaluation

class EvaluationsTables(tables.Table):
    class Meta:
        model = Evaluation
        attrs = {'class': 'paleblue'}
        exclude=('id', 'evaluator' , 'ofProject')
        sequence=('heurPrincip','place','description' ,'recommendation','positivity','severity','frequency')
