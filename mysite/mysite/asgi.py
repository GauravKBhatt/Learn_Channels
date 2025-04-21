
import os

from channels.auth import AuthMiddlewareStack
# AuthMiddlewareStack populates the websocket connection's scope with the currently authenticated user.
# Similar to AuthenticationMiddleware that populates the request onject of a view function with the currently authenticated user.
from channels.routing import ProtocolTypeRouter, URLRouter
# URLrouter examines the path of the connection to route it to particular consumer.
from channels.security.websocket import AllowedHostOriginValidator
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
# when you run an ASGI app, Django needs to know about your models before you use them, thus you need to instantialize the app before importin any code that would need ORM
django_asgi_app=get_asgi_application()
# protocoltyperouter determines whether the incoming request is http or websocket and forwards it likewise. 
from chat.routing import websocket_urlpatterns
application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket":AllowedHostOriginValidator(
            AuthMiddlewareStack(
                URLRouter(
                    websocket_urlpatterns
                )
            )
        )
    }
)
