from django.shortcuts import render

from rest_pandas.views import PandasView
from rest_pandas.renderers import PandasCSVRenderer, PandasTextRenderer, PandasJSONRenderer, PandasHTMLRenderer
from .models import MQTTMessage
from .serializers import generate_parsing_serializer_class
from .conf import settings

import re

class MessageView(PandasView):
    """RESTful view to get a set of MQTT messages

    Named URL groups
    ----------------

    * `topic`   : This view will only return messages with a matching topic.

    Query strings
    -------------

    * `format`  : Set the file format to be returned. One of 'txt', 'csv', 'json', 'html'.
    * `limit`   : Limit the number of returned messages.
    * `skip`    : Skip the first N entries.
    * `parse`   : Regular expression to parse the messages' payload.
                  See `MQTTMessage.parse_payload`.

    """

    class HTMLRenderer(PandasHTMLRenderer):
        """Class that renders the messages as a HTML page."""

        template_name = settings.MQTT_LOGGER_TEMPLATE

        def get_template_context(self, data, renderer_context):
            """Add additional variables to the context."""

            view = renderer_context['view']
            request = renderer_context['request']
            kwargs = renderer_context['kwargs']

            # Get context from parent class
            context = PandasHTMLRenderer.get_template_context(self, data, renderer_context)

            # Add usefull variables
            context['topic'] = kwargs.get('topic', '')
            context['format'] = request.GET.get('format', 'html')
            context['limit'] = request.GET.get('limit', 0)
            context['skip'] = request.GET.get('skip', 0)
            context['parse'] = request.GET.get('parse', '')

            return context

    renderer_classes = [HTMLRenderer, PandasCSVRenderer, PandasTextRenderer, PandasJSONRenderer]

    def get_queryset(self):
        """Get the queryset that will be rendered.

        The queryset is filtered by the topic as requested in the URL
        and optionally limited by the query string `limit=<n>`.
        A limit of 0 sets the limit to the maximum value.
        """

        topic = self.kwargs['topic']
        # Replace '+' and '#' with standard regular expression
        topic = topic.replace(r'+', r'[^/]*')
        topic = topic.replace(r'#', r'.*')
        topic = r'^' + topic + r'$'

        default_limit = 100
        max_limit = 1000
        limit = self.request.GET.get('limit', default_limit)
        try:
            limit = int(limit)
        except ValueError:
            limit = default_limit
        if limit < 1 or limit > max_limit:
            limit = max_limit

        skip = self.request.GET.get('skip', 0)
        try:
            skip = int(skip)
        except ValueError:
            skip = 0
        if skip < 0:
            skip = 0

        return MQTTMessage.objects.filter(topic__regex=topic).order_by('-time_recorded')[skip:skip+limit]

    def get_serializer_class(self):
        """Dynamically create a serializer class using the `parse` query string."""

        regex = self.request.GET.get('parse', '')
        try:
            regex = re.compile(regex)
        except:
            regex = re.compile('')

        cls = generate_parsing_serializer_class(regex)
        return self.with_list_serializer(cls)
