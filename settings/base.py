import os
DATABASE_CONFIG={
                "Catalog":{
                    "name":"postgres",
                    "user":"postgres",
                    "password":os.environ["DATABASE_PASSWORD"],
                    "host":"localhost",
                    "port":"5432"
                }
            }