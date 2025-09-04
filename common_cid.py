import datetime

# basic
# db_conn='mysql://root:@localhost:3307/abom'
db_conn = 'mysql://root:@127.0.0.1:3307/abom'

# project dockerise but db localhost
# db_conn = 'mysql://root:@host.docker.internal/abom'

# for docker my-mysql image
# db_conn = 'mysql+pymysql://root:123@host.docker.internal:3306/abom'




# db = DAL('mysql://mytranscom01:superSecret1@mytranscom01.mysql.database.azure.com/mytranscom', decode_credentials=True)
date_fixed=datetime.datetime.now() #+datetime.timedelta(hours=6)