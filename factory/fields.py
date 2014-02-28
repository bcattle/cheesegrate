import uuid
import datetime
import random


class FactoryField(object):
    # def __call__(self, obj, model_klass, field, adapter, factory):
    def __call__(self, adapter, model_klass):
        raise NotImplementedError


class RandomGuidField(FactoryField):
    def __call__(self, adapter, model_klass):
        return str(uuid.uuid4())


class DateNowUTCField(FactoryField):
    def __call__(self, adapter, model_klass):
        return datetime.datetime.utcnow().isoformat("T") + "Z"


class RandomBooleanField(FactoryField):
    def __init__(self, prob_true=0.5):
        self.prob_true = prob_true

    def __call__(self, adapter, model_klass):
        return random.random() < self.prob_true


class RandomIntField(FactoryField):
    def __init__(self, min=0, max=100):
        self.min = min
        self.max = max

    def __call__(self, adapter, model_klass):
        return random.randint(self.min, self.max)


class RandomFloatField(FactoryField):
    def __init__(self, min=0.0, max=1.0):
        self.min = min
        self.max = max

    def __call__(self, adapter, model_klass):
        return random.uniform(self.min, self.max)


class ChoiceField(FactoryField):
    def __init__(self, choices):
        self.choices = choices

    def __call__(self, adapter, model_klass):
        return random.choice(self.choices)


class IndexedChoiceField(FactoryField):
    def __init__(self, sequence, seq_index):
        self.sequence = sequence
        self.seq_index = seq_index

    def __call__(self, adapter, model_klass):
        return self.sequence[self.seq_index][self.seq_index]


class ArrayOfModelsField(FactoryField):
    def __init__(self, length=None, length_min=None, length_max=None):
        """
        model_klass can be a string name??
        """
        assert length or (length_min and length_max)
        self.length = length
        self.length_min = length_min
        self.length_max = length_max

        # Find the factory for model_klass of this field
        pass

    def __call__(self, adapter, model_klass):
        # Resolve the type of this field
        # Look on the model for a field of the same name
        model_field = model_klass._fields.get(self._name)
        if model_field is None:
            raise Exception('Unable to find a field called "%s" on model "%s", '
                            'can\'t generate array' % (self._name, model_klass.__name__))
        model_field_type = getattr(model_field, 'type_klass')
        if model_field_type is None:
            raise Exception('Unable to resolve array field type, add a type= attribute ')

        if self.length:
            length = self.length
        else:
            length = random.randint(self.length_min, self.length_max)

        # Return `length` models
        models = []
        for n in range(length):
            models.append(adapter.python_values_for_class(model_field_type))

        return models
