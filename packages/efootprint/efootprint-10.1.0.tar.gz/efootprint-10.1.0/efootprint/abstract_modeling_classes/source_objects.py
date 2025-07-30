import pandas as pd
from pint import Quantity

from efootprint.abstract_modeling_classes.explainable_object_base_class import ExplainableObject, Source
from efootprint.abstract_modeling_classes.explainable_objects import ExplainableQuantity, ExplainableHourlyQuantities
from efootprint.constants.sources import Sources


SOURCE_VALUE_DEFAULT_NAME = "unnamed source"


class SourceObject(ExplainableObject):
    def __init__(self, value: object, source: Source = Sources.HYPOTHESIS, label: str = SOURCE_VALUE_DEFAULT_NAME):
        super().__init__(value, label=label, source=source)


class SourceValue(ExplainableQuantity):
    def __init__(self, value: Quantity, source: Source = Sources.HYPOTHESIS, label: str = SOURCE_VALUE_DEFAULT_NAME):
        super().__init__(value, label=label, source=source)


class SourceHourlyValues(ExplainableHourlyQuantities):
    def __init__(self, value: pd.DataFrame, source: Source = Sources.HYPOTHESIS, label: str = SOURCE_VALUE_DEFAULT_NAME):
        super().__init__(value, label=label, source=source)
