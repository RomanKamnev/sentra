package config;

import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.sink.KafkaRecordSerializationSchema;
import org.apache.flink.connector.kafka.sink.KafkaSink;

public class KafkaSinkFactory {

    public static KafkaSink<String> createAlertSink() {
        return KafkaSink.<String>builder()
                .setBootstrapServers(KafkaConfig.BOOTSTRAP_SERVERS)
                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                        .setTopic(KafkaConfig.ALERTS_TOPIC)
                        .setValueSerializationSchema(new SimpleStringSchema())
                        .build())
                .setKafkaProducerConfig(KafkaConfig.PRODUCER_PROPERTIES)
                .setTransactionalIdPrefix("alert-sentra-")
                .build();
    }

    public static KafkaSink<String> createLogSink() {
        return KafkaSink.<String>builder()
                .setBootstrapServers(KafkaConfig.BOOTSTRAP_SERVERS)
                .setRecordSerializer(KafkaRecordSerializationSchema.builder()
                        .setTopic(KafkaConfig.LOGGING_TOPIC)
                        .setValueSerializationSchema(new SimpleStringSchema())
                        .build())
                .setKafkaProducerConfig(KafkaConfig.PRODUCER_PROPERTIES)
                .setTransactionalIdPrefix("log-sentra-")
                .build();
    }
}

