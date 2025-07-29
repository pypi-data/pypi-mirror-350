from dotenv import load_dotenv
from os import getenv as env

load_dotenv()

DSN = f"postgres://{env('POSTGRES_USER')}:{env('POSTGRES_PASSWORD')}@{env('POSTGRES_HOST', 'xyncdbs')}:{env('POSTGRES_PORT', 5432)}/{env('POSTGRES_DB', env('POSTGRES_USER'))}"
HT = env("HT")
BKEY = env("BKEY")
BSEC = env("BSEC")
OKXKEY = env("OKXKEY")
OKXSEC = env("OKXSEC")
OKXPSF = env("OKXPSF")
BYT = env("BYT")
BYKEY = env("BYKEY")
BYSEC = env("BYSEC")
KUKEY = env("KUKEY")
KUSEC = env("KUSEC")
CMXK = env("CMXK")
CMXS = env("CMXS")
