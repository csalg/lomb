import time

from services.etl import etl_from_scratch
from slices.caching import ensure_datapoints_have_frequency_and_languages
from slices.remove_ignored_datapoints import remove_ignored_datapoints

if __name__ == '__main__':
    print('Starting ETL from scratch.')
    timestamp = int(time.time())
    etl_from_scratch()
    print(f'Done with ETL. Took {int(time.time()) - timestamp} seconds.')
    timestamp = int(time.time())
    print('Will remove ignored datapoints.')
    remove_ignored_datapoints()
    print(f'Done removing ignored datapoints. Took {int(time.time()) - timestamp} seconds.')
    timestamp = int(time.time())
    print('Will ensure datapoints have frequency and languages.')
    ensure_datapoints_have_frequency_and_languages()
    print(f'Done ensuring frequency and language metadata. Took {int(time.time()) - timestamp} seconds.')
