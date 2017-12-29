from settings import *
import server
import sub_server

newThread(server.main)
extend_one_second()
sub_server.main(local_IP())