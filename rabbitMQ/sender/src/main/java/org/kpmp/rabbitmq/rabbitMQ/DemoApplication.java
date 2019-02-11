package org.kpmp.rabbitmq.rabbitMQ;

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
	public DemoApplication(Sender sender, EmitLogTopic logEmitter) throws Exception {
		sender.send(QUEUE_NAME);
		logEmitter.emit("log.critical", "Terrible thing happened");
		logEmitter.emit("log.info", "Info message that will not be picked up");
	}
}
