import os
LOG_FILE_PATH=r"C:\Users\jrayala\home\product-catalog__logs"
DATABASE_CONFIG={
                "Catalog":{
                    "name":"postgres",
                    "user":"postgres",
                    "password":os.environ["DATABASE_PASSWORD"],
                    "host":"localhost",
                    "port":"5432"
                }
            }