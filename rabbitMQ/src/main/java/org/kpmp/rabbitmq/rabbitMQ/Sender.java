package org.kpmp.rabbitmq.rabbitMQ;

import java.util.Map;

import org.springframework.stereotype.Component;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

@Component
public class Sender {

	public void send(String queueName) throws Exception {
		ConnectionFactory factory = new ConnectionFactory();
		factory.setHost("localhost");

		// Using a try-with-resources statement so I don't have to worry about closing
		// connections
		try (Connection connection = factory.newConnection(); Channel channel = connection.createChannel()) {
			boolean queueSurviveRestart = false;
			boolean isRestrictedToThisConnection = false;
			boolean serverAutoDelete = false;
			Map<String, Object> additionalArguments = null;
			channel.queueDeclare(queueName, queueSurviveRestart, isRestrictedToThisConnection, serverAutoDelete,
					additionalArguments);
			String message = "Hello World!";
			channel.basicPublish("", queueName, null, message.getBytes());
			System.out.println(" [x] Sent '" + message + "'");
		}
	}

}
