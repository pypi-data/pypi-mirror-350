import numpy as np

from glue.core.data import Data

from glue.core.component import CategoricalComponent

__all__ = ["create_phase_data"]


def create_phase_data(df, **kwargs):
    data = Data()
    data.meta["is_phase_data"] = True
    data.style.color = "#ff0000"

    phases = np.asarray(df.index.values)
    categories = [phase for phase in phases]
    phase_name = CategoricalComponent(phases, categories)
    #data.add_component(df.index.values, "phase")
    for c in df.columns:
        data.add_component(df[c], str(c))

    return data