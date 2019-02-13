package org.kpmp.rabbitmq.rabbitMQ;

import org.springframework.stereotype.Component;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;

@Component
public class Receiver {

	public void receive(String queueName) throws Exception {

		// We don't do a try-with-resources because we want this to continue waiting for
		// messages to arrive
		ConnectionFactory factory = new ConnectionFactory();
		factory.setHost("rabbitmq");
		factory.setUsername("user");
		factory.setPassword("pass");
		Connection connection = factory.newConnection();
		Channel channel = connection.createChannel();

		channel.queueDeclare(queueName, false, false, false, null);
		System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

		DeliverCallback deliverCallback = (consumerTag, delivery) -> {
			String message = new String(delivery.getBody(), "UTF-8");
			System.out.println(" [x] Received '" + message + "'");
		};
		channel.basicConsume(queueName, true, deliverCallback, consumerTag -> {
		});
	}
}
