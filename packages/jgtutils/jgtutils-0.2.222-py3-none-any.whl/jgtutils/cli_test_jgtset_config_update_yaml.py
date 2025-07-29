#%%
from io import StringIO
import ruamel.yaml
yaml = ruamel.yaml.YAML()

book_config_file="_config.yml"

import jgtset as jset
jgtset_included_keys = "_jgtset_included.json"

updated_yaml_data=jset.update_jgt_on_existing_yaml_file(custom_path=jgtset_included_keys, target_filepath=book_config_file)
# %%
stream = StringIO()
yaml.dump(updated_yaml_data, stream)
print(stream.getvalue())



