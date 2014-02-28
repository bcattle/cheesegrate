import uuid
import datetime
import random


class FactoryField(object):
    pass


class RandomGuidField(FactoryField):
    def __call__(self):
        return str(uuid.uuid4())

class DateNowUTCField(FactoryField):
    def __call__(self):
        return datetime.datetime.utcnow().isoformat("T") + "Z"

class RandomBooleanField(FactoryField):
    def __init__(self, prob_true=0.5):
        self.prob_true = prob_true

    def __call__(self):
        return random.random() < self.prob_true


class RandomIntField(FactoryField):
    def __init__(self, min=0, max=100):
        self.min = min
        self.max = max

    def __call__(self):
        return random.randint(self.min, self.max)


class RandomFloatField(FactoryField):
    def __init__(self, min=0.0, max=1.0):
        self.min = min
        self.max = max

    def __call__(self):
        return random.uniform(self.min, self.max)



class ChoiceField(FactoryField):
    def __init__(self, choices):
        self.choices = choices

    def __call__(self):
        return random.choice(self.choices)


class IndexedChoiceField(FactoryField):
    def __init__(self, sequence, seq_index):
        self.sequence = sequence
        self.seq_index = seq_index

    def __call__(self, index):
        return self.sequence[index][self.seq_index]


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

    def __call__(self):
        if self.length:
            length = self.length
        else:
            length = random.randint(self.length_min, self.length_max)
        # Return `length` models
        pass
