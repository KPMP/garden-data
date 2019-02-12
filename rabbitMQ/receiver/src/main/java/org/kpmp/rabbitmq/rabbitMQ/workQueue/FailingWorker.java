package org.kpmp.rabbitmq.rabbitMQ.workQueue;

import org.springframework.stereotype.Component;

import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.DeliverCallback;

@Component
public class FailingWorker {

	private static final String TASK_QUEUE_NAME = "task_queue";

	public void doWork() throws Exception {
		ConnectionFactory factory = new ConnectionFactory();
		factory.setHost("rabbitmq");
		factory.setUsername("user");
		factory.setPassword("pass");
		final Connection connection = factory.newConnection();
		final Channel channel = connection.createChannel();

		channel.queueDeclare(TASK_QUEUE_NAME, true, false, false, null);
		System.out.println(" [*] Waiting for messages. To exit press CTRL+C");

		channel.basicQos(1);

		DeliverCallback deliverCallback = (consumerTag, delivery) -> {
			String message = new String(delivery.getBody(), "UTF-8");

			System.out.println(" [x] Received with failing worker'" + message + "'");
			try {
				doWork(message);
				System.out.println(" [x] Done with failing worker");
				channel.basicAck(delivery.getEnvelope().getDeliveryTag(), false);
			} catch (Exception e) {
				System.out.println("Failing worker failed");
				channel.abort();
			}
		};
		channel.basicConsume(TASK_QUEUE_NAME, false, deliverCallback, consumerTag -> {
		});
	}

	private static void doWork(String task) throws Exception {
		for (char ch : task.toCharArray()) {
			if (ch == '.') {
				try {
					Thread.sleep(1000);
					throw new Exception("I failed");
				} catch (InterruptedException _ignored) {
					Thread.currentThread().interrupt();
				}
			}
		}
	}
}
