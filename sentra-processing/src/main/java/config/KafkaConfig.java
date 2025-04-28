package config;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class KafkaConfig {

    public static final String BOOTSTRAP_SERVERS;
    public static final String LOGS_TOPIC;
    public static final String ALERTS_TOPIC;
    public static final String LOGGING_TOPIC;
    public static final String GROUP_ID;

    public static final Properties PRODUCER_PROPERTIES = new Properties();

    static {
        Properties props = new Properties();
        try (InputStream input = KafkaConfig.class.getClassLoader().getResourceAsStream("sentra-config.properties")) {
            if (input == null) {
                throw new IllegalArgumentException("sentra-config.properties not found");
            }
            props.load(input);

            BOOTSTRAP_SERVERS = props.getProperty("kafka.bootstrap.servers", "localhost:9092");
            LOGS_TOPIC = props.getProperty("kafka.topic.logs", "logs");
            ALERTS_TOPIC = props.getProperty("kafka.topic.alerts", "alerts");
            LOGGING_TOPIC = props.getProperty("kafka.topic.logs_events", "logs-events");
            GROUP_ID = props.getProperty("kafka.group.id", "sentra-flink");

            PRODUCER_PROPERTIES.setProperty("transaction.timeout.ms", props.getProperty("kafka.producer.transaction.timeout.ms", "900000"));
            PRODUCER_PROPERTIES.setProperty("acks", props.getProperty("kafka.producer.acks", "all"));
            PRODUCER_PROPERTIES.setProperty("enable.idempotence", props.getProperty("kafka.producer.enable.idempotence", "true"));

            System.out.println("[CONFIG] Loaded Kafka settings successfully");
        } catch (IOException e) {
            throw new ExceptionInInitializerError("Failed to load Kafka config: " + e.getMessage());
        }
    }
}
