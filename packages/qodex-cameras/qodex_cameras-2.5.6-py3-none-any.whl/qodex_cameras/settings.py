from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent       # /whikoperator
CUR_DIR = os.path.dirname(os.path.abspath(__file__))    # /whikoperator/whikoperator
CONFIGS_DIR = os.path.join(CUR_DIR, 'configs')

PICS_DIR_NAME = 'photos'
DEF_PICS_DIR = os.path.join(CUR_DIR, PICS_DIR_NAME)
TEST_PHOTO = os.path.join(DEF_PICS_DIR, 'Test.png')

