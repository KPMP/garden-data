package org.kpmp.rabbitmq.rabbitMQ.publishSubscribe;

import org.springframework.stereotype.Component;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;

@Component
public class EmitLog {

	private static final String EXCHANGE_NAME = "logs";

	public void emitLog(String... argv) throws Exception {
		ConnectionFactory factory = new ConnectionFactory();
		factory.setHost("rabbitmq");
		factory.setUsername("user");
		factory.setPassword("pass");
		try (Connection connection = factory.newConnection(); Channel channel = connection.createChannel()) {
			channel.exchangeDeclare(EXCHANGE_NAME, "fanout");

			String message = argv.length < 1 ? "info: Hello World!" : String.join(" ", argv);

			channel.basicPublish(EXCHANGE_NAME, "", null, message.getBytes("UTF-8"));
			System.out.println(" [x] Sent '" + message + "'");
		}
	}

}
