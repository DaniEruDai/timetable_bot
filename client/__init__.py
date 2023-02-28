import sys,os
sys.path.append(os.path.join(sys.path[0],'..'))

from dotenv import load_dotenv,find_dotenv
load_dotenv(find_dotenv('.env'))