package org.kpmp.rabbitmq.rabbitMQ.topic;

import org.springframework.stereotype.Component;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;

@Component
public class ReceiveLogsTopic {

	private static final String EXCHANGE_NAME = "topic_logs";

	public void receive(String... argv) throws Exception {
		ConnectionFactory factory = new ConnectionFactory();
		factory.setHost("rabbitmq");
		factory.setUsername("user");
		factory.setPassword("pass");
		Connection connection = factory.newConnection();
		Channel channel = connection.createChannel();

		channel.exchangeDeclare(EXCHANGE_NAME, "topic");
		String queueName = channel.queueDeclare().getQueue();

		if (argv.length < 1) {
			System.err.println("Usage: ReceiveLogsTopic [binding_key]...");
			System.exit(1);
		}

		for (String bindingKey : argv) {
			channel.queueBind(queueName, EXCHANGE_NAME, bindingKey);
		}

		System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

		DeliverCallback deliverCallback = (consumerTag, delivery) -> {
			String message = new String(delivery.getBody(), "UTF-8");
			System.out.println(" [x] Received '" + delivery.getEnvelope().getRoutingKey() + "':'" + message + "'");
		};
		channel.basicConsume(queueName, true, deliverCallback, consumerTag -> {
		});
	}
}
