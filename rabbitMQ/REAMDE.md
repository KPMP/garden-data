# RabbitMQ
I have created a docker-compose script to encapsulate this spike.

There are 3 containers, 1 for rabbitmq and the management plugin, 1 for a sender, and one for a receiver.

If you want to log into rabbitmq management console after you bring up the docker containers, you can navigate to localhost:8080 and user username/password: user/pass

The sender currently sends a single message and then dies.  The receiver continues to live and watch the queue for additional messages.  Because of this, you can go to the management console and add more messages to the queue and see them printed out if you follow the logs of the docker containers.

