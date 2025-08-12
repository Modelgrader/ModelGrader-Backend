from ..models import *
from .auth_service import verifyToken
from .permission_service import canManageTopic
from ..utility import generate_random_string, check_pdf
from .service_result import ServiceResult
from django.forms.models import model_to_dict
from ..errors.common import *
from ..serializers2.topic_serializer import GetTopicSerializer

def get_topic_item_list(topic_id, token):

    if not Topic.objects.filter(topic_id=topic_id).exists():
        raise ItemNotFoundError()

    if not verifyToken(token):
        raise InvalidTokenError()

    topic = Topic.objects.get(topic_id=topic_id)

    collections = []
    for tc in TopicCollection.objects.filter(topic=topic).order_by('order'):
        problems = CollectionProblem.objects.filter(collection=tc.collection).order_by('order')
        problems_data = []
        for cp in problems:
            problems_data.append({
                'problem_id': cp.problem.problem_id,
                'title': cp.problem.title,
            })
        collections.append({
            'collection_id': tc.collection.collection_id,
            'name': tc.collection.name,
            'problems': problems_data
        })
    
    return {
        'name': topic.name,
        'collections': collections
    }