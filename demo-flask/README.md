# Description

Standard web form created using python flask framework ( http://flask.pocoo.org ) . Software reads value entered to the input field and pushes value to the redis list. 

# Configuration parameters (environment variables)

| Name        | Description           | Default value  |
| ------------- |:-------------:| -----:|
| WAIT_QUEUE      | Name of the list inside Redis | demo_wait_q_0 |
| REDIS_HOST      | Redis host      |   |
| REDIS_PORT | Redis port     |     |
| REDIS_DB | Redis database | 0 |
| REDIS_PASSWORD | Redis password | |
| REDIS_SSL | Use redis with SSL | true | 
