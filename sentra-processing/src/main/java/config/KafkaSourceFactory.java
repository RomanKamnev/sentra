package config;

import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.connector.kafka.source.enumerator.initializer.OffsetsInitializer;

public class KafkaSourceFactory {

    public static KafkaSource<String> createLogsSource() {
        return KafkaSource.<String>builder()
                .setBootstrapServers(KafkaConfig.BOOTSTRAP_SERVERS)
                .setTopics(KafkaConfig.LOGS_TOPIC)
                .setGroupId(KafkaConfig.GROUP_ID)
                .setStartingOffsets(OffsetsInitializer.earliest())
                .setValueOnlyDeserializer(new SimpleStringSchema())
                .build();
    }
}
