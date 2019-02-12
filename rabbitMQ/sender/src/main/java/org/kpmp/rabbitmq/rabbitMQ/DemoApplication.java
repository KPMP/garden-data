package org.kpmp.rabbitmq.rabbitMQ;

import org.kpmp.rabbitmq.rabbitMQ.publishSubscribe.EmitLog;
import org.kpmp.rabbitmq.rabbitMQ.routing.EmitLogDirect;
import org.kpmp.rabbitmq.rabbitMQ.topic.EmitLogTopic;
import org.kpmp.rabbitmq.rabbitMQ.workQueue.TaskProducer;
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
	public DemoApplication(Sender sender, EmitLogTopic logEmitter, TaskProducer producer, EmitLog pubSubEmitLog,
			EmitLogDirect routingEmitLog) throws Exception {
		sender.send(QUEUE_NAME);
		logEmitter.emit("log.critical", "Terrible thing happened");
		logEmitter.emit("log.info", "Info message that will not be picked up");
		producer.produce("Initial message...");
		pubSubEmitLog.emitLog();
		routingEmitLog.emitLog("info", "stuff happened");
		routingEmitLog.emitLog("error", "bad stuff happened");
		routingEmitLog.emitLog("warning", "message will be lost, no receiver");
	}
}
