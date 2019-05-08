import serpy


class ContextSerializer(serpy.Serializer):

    def __init__(self, instance=None, *args, **kwargs):
        instance = self.process_hook(instance)
        super().__init__(instance=instance, *args, **kwargs)
        self.context = None
        if 'context' in kwargs:
            self.context = kwargs['context']
            self.set_context(self.context)

    def set_context(self, context):
        self.context = context
        for f in self._field_map.items():
            f[1].context = context
            if isinstance(f[1], ContextSerializer):
                f[1].set_context(context)

    def process_hook(self,instance):
        return instance

