package org.kpmp.rabbitmq.rabbitMQ;

import org.kpmp.rabbitmq.rabbitMQ.publishSubscribe.ReceiveLogs;
import org.kpmp.rabbitmq.rabbitMQ.routing.ReceiveLogsDirect;
import org.kpmp.rabbitmq.rabbitMQ.topic.ReceiveLogsTopic;
import org.kpmp.rabbitmq.rabbitMQ.workQueue.FailingWorker;
import org.kpmp.rabbitmq.rabbitMQ.workQueue.Worker;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class DemoApplication {

	private final static String QUEUE_NAME = "hello";

	public static void main(String[] args) {
		SpringApplication.run(DemoApplication.class, args);
	}

	@Autowired
	public DemoApplication(Receiver receiver, ReceiveLogsTopic receiveLogs, Worker worker, FailingWorker failingWorker,
			ReceiveLogs pubSubReceieveLogs, ReceiveLogsDirect routingReceiveLogs) throws Exception {
		receiver.receive(QUEUE_NAME);
		receiveLogs.receive("*.critical");
		worker.doWork();
		failingWorker.doWork();
		pubSubReceieveLogs.receive();
		routingReceiveLogs.receive("info");
		new ReceiveLogsDirect().receive("error");
	}
}
