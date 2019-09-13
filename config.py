import configparser

parser = configparser.ConfigParser()
parser.read("config.ini")

addr = parser["server"]["addr"]
port = int(parser["server"]["port"])

username = parser["client"]["username"]
password = parser["client"]["password"]
