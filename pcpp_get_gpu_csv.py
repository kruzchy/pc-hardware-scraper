from pcpartpicker import API
import pandas as pd
import numpy as np

api = API(multithreading=False)
api.set_region('in')
df = api.retrieve('video-card')['video-card']

new = []
for obj in df:

    new.append({'brand': obj.brand if obj.brand else np.nan,
                'model': obj.model if obj.model else np.nan,
                'chipset': obj.chipset if obj.chipset else np.nan,
                'vram': obj.vram.total if obj.vram else np.nan,
                'core_clock': obj.core_clock.cycles if obj.core_clock else np.nan,
                'boost_clock': obj.boost_clock.cycles if obj.boost_clock else np.nan,
                'interface': obj.interface if obj.interface else np.nan,
                'color': obj.color if obj.color else np.nan})

new_df = pd.DataFrame(new)
new_df.to_csv('pcpp-gpu.csv', index=False)
