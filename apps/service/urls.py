from django.urls import path
from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from service.views import LoonFlowAPIView
from service.views import LoonFlowInitStateViewSet
from service.views import LoonFlowCreateTicketViewSet
from service.views import LoonFlowTicketViewSet
from service.views import LoonFlowStepViewSet
from service.views import LoonFlowTransitionViewSet
from service.views import LoonFlowTranActionViewSet
from service.views import LoonFlowTicketOpViewSet
from service.views import ueditor_index
from service.views import ueditor_uploadfile
from service.views import ueditor_uploadimage

router = DefaultRouter()
router.register('init_state', LoonFlowInitStateViewSet, 'init_state')
router.register('create_ticket', LoonFlowCreateTicketViewSet, 'create_ticket')
router.register('tickets', LoonFlowTicketViewSet, 'tickets')
# router.register('operation_ticket', LoonFlowTicketOpViewSet, 'operation_ticket')
router.register('steps', LoonFlowStepViewSet, 'steps')
router.register('logs', LoonFlowTransitionViewSet, 'logs')
router.register('actions', LoonFlowTranActionViewSet, 'actions')

urlpatterns = [
    path('workflows/', LoonFlowAPIView.as_view()),
    path('ueditor/', ueditor_index),
    path('ueditor_fileup', ueditor_uploadfile),
    path('ueditor_imgup', ueditor_uploadimage),
    url(r'operation_ticket/(?P<pk>\d+)/$', LoonFlowTicketOpViewSet.as_view())
]

urlpatterns += router.urls
