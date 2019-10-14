from pcpartpicker import API
import pandas as pd
import numpy as np

api = API(multithreading=False)
api.set_region('in')
df = api.retrieve('cpu')['cpu']

new = []
for obj in df:
    new.append({'brand': obj.brand if obj.brand else np.nan,
                'model': obj.model if obj.model else np.nan,
                'cores': obj.cores if obj.cores else np.nan,
                'base_clock': obj.base_clock.cycles if obj.base_clock else np.nan,
                'boost_clock': obj.base_clock.cycles if obj.boost_clock else np.nan,
                'tdp': obj.tdp if obj.tdp else np.nan,
                'integrated_graphics':  np.nan if obj.integrated_graphics is None else obj.integrated_graphics,
                'multithreading': np.nan if obj.multithreading is None else obj.multithreading})

new_df = pd.DataFrame(new)
new_df.to_csv('pcpp-cpu.csv', index=False)
