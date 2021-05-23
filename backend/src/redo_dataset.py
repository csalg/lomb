from services.etl import etl_from_scratch
from slices.caching import ensure_datapoints_have_frequency_and_languages
from slices.remove_ignored_datapoints import remove_ignored_datapoints

if __name__ == '__main__':
    etl_from_scratch()
    remove_ignored_datapoints()
    ensure_datapoints_have_frequency_and_languages()
