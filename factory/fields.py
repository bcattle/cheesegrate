import uuid
import datetime
import random
import collections


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


class ConsecutiveIntField(FactoryField):
    # static variable
    counters = collections.defaultdict(lambda: 0)

    def __init__(self, min=0, count_down=False):
        self.min = min
        self.counts_down = count_down

    def __call__(self, adapter, model_klass):
        # We key the counter on name, adapter, model_klass
        key = (self._name, adapter, model_klass)
        if self.counts_down:
            ConsecutiveIntField.counters[key] -= 1
        else:
            ConsecutiveIntField.counters[key] += 1
        return ConsecutiveIntField.counters[key] + self.min


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
        If the model field has a hard-coded length,
         doesn't make sense to use the length parans here

        Should we just ignore them?
        """
        assert length or (length_min and length_max) \
            or not (length or length_min or length_max)
        self.length = length
        self.length_min = length_min
        self.length_max = length_max

    def __call__(self, adapter, model_klass):
        # Resolve the type of this field
        # Look on the model for a field of the same name
        model_field = model_klass._fields.get(self._name)
        if model_field is None:
            raise Exception('Unable to find a field called "%s" '
                            'on model "%s", can\'t generate array'
                            % (self._name, model_klass.__name__))
        model_field_type = getattr(model_field, 'type_klass')
        if model_field_type is None:
            raise Exception('Unable to resolve array field type, '
                            'add a type= attribute ')

        # If the field has a length, and this factory field
        # has one as well, it's an error
        if model_field.length is not None and \
                self.length or self.length_min or self.length_max:
            raise Exception('The field "%s.%s" has a defined length '
                            'and the factory is trying to override it'
                            % (model_klass.__name__, model_field._name))

        if model_field.length:
            length = model_field.length
        elif self.length:
            length = self.length
        else:
            length = random.randint(self.length_min, self.length_max)

        # Return `length` models
        models = []
        for n in range(length):
            models.append(adapter.python_values_for_class(model_field_type))

        return models
