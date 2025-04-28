package flink;

import org.apache.flink.streaming.api.functions.windowing.ProcessWindowFunction;
import org.apache.flink.util.Collector;
import org.apache.flink.api.java.tuple.Tuple5;

import java.util.HashSet;
import java.util.Set;

public class UniqueUsernameCounter extends ProcessWindowFunction<Tuple5<String, Integer, Long, String, String>, String, String, org.apache.flink.streaming.api.windowing.windows.TimeWindow> {

    @Override
    public void process(String key, Context context, Iterable<Tuple5<String, Integer, Long, String, String>> elements, Collector<String> out) {
        Set<String> uniqueUsernames = new HashSet<>();

        for (Tuple5<String, Integer, Long, String, String> element : elements) {
            if (!"invalid".equals(element.f4)) {
                uniqueUsernames.add(element.f4);
            }
        }

        if (uniqueUsernames.size() >= 10) {
            out.collect("[ALERT][CREDENTIAL_STUFFING] IP: " + key + " attempted " + uniqueUsernames.size() + " usernames in 1 min window.");
        }
    }
}
