import os
os.environ['ISX'] = '0'

from dewan_manual_curation import manual_curation

if __name__ == '__main__':
    manual_curation.launch_gui()
