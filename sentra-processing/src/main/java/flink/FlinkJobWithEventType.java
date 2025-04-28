package flink;

import config.KafkaSinkFactory;
import config.KafkaSourceFactory;
import config.MappingConfig;
import org.apache.flink.api.common.eventtime.WatermarkStrategy;
import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.java.tuple.Tuple5;
import org.apache.flink.connector.kafka.sink.KafkaSink;
import org.apache.flink.connector.kafka.source.KafkaSource;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.windowing.assigners.TumblingEventTimeWindows;
import org.apache.flink.streaming.api.windowing.time.Time;
import util.FlexibleLoginParser;

import java.util.Objects;

public class FlinkJobWithEventType {

    public static void main(String[] args) throws Exception {
        StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        env.enableCheckpointing(5000);

        KafkaSource<String> source = KafkaSourceFactory.createLogsSource();

        DataStream<String> stream = env.fromSource(
                source,
                WatermarkStrategy.noWatermarks(),
                "KafkaSource"
        );

        DataStream<Tuple5<String, Integer, Long, String, String>> parsed = stream
                .map(new MapFunction<String, Tuple5<String, Integer, Long, String, String>>() {
                    private transient FlexibleLoginParser localParser;

                    @Override
                    public Tuple5<String, Integer, Long, String, String> map(String value) {
                        if (localParser == null) {
                            MappingConfig mappingConfig = new MappingConfig("mapping-config.json");
                            localParser = new FlexibleLoginParser(mappingConfig);
                        }
                        return localParser.parse(value);
                    }
                })
                .filter(tuple -> !"invalid".equals(tuple.f0));

        SingleOutputStreamOperator<String> loginAlerts = parsed
                .keyBy(tuple -> tuple.f0)
                .window(TumblingEventTimeWindows.of(Time.minutes(1)))
                .reduce((v1, v2) -> Tuple5.of(v1.f0, v1.f1 + v2.f1, v1.f2, v1.f3, v1.f4))
                .map(tuple -> {
                    String eventType = tuple.f3;
                    int failures = tuple.f1;
                    if (RuleEngine.shouldTriggerAlert(eventType, failures)) {
                        return "[ALERT][" + RuleEngine.getSeverity(eventType).toUpperCase() + "] " + eventType + " | IP: " + tuple.f0 + " had " + failures + " failures";
                    } else if (RuleEngine.shouldLogOnly(eventType, failures)) {
                        return "[LOG][" + RuleEngine.getSeverity(eventType).toUpperCase() + "] " + eventType + " | IP: " + tuple.f0 + " had " + failures + " failures";
                    } else {
                        return null;
                    }
                })
                .filter(Objects::nonNull);

        SingleOutputStreamOperator<String> credentialStuffingAlerts = parsed
                .keyBy(tuple -> tuple.f0)
                .window(org.apache.flink.streaming.api.windowing.assigners.TumblingProcessingTimeWindows.of(Time.minutes(1)))
                .process(new UniqueUsernameCounter());

        KafkaSink<String> alertSink = KafkaSinkFactory.createAlertSink();
        KafkaSink<String> logSink = KafkaSinkFactory.createLogSink();

        loginAlerts
                .filter(msg -> msg.startsWith("[ALERT]"))
                .sinkTo(alertSink);

        loginAlerts
                .filter(msg -> msg.startsWith("[LOG]"))
                .sinkTo(logSink);

        credentialStuffingAlerts.sinkTo(alertSink);

        env.execute("Sentra Flink Job with Flexible Login Parsing and Credential Stuffing Detection");
    }
}
