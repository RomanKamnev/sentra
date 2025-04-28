package flink;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.File;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class RuleEngine {
    private static final Map<String, Rule> rulesMap = new HashMap<>();

    static {
        loadRules();
    }

    public static void reloadRules() {
        System.out.println("[RULE ENGINE] Reloading rules...");
        rulesMap.clear();
        loadRules();
    }

    private static void loadRules() {
        try {
            ObjectMapper mapper = new ObjectMapper();
            ClassLoader classLoader = RuleEngine.class.getClassLoader();
            URL resource = classLoader.getResource("rules.json");
            if (resource == null) {
                throw new IllegalArgumentException("rules.json not found in resources");
            }
            File file = new File(resource.toURI());
            JsonNode root = mapper.readTree(file);
            for (JsonNode node : root.path("rules")) {
                String eventType = node.path("event_type").asText();
                int minFailures = node.path("min_failures").asInt();
                int timeWindow = node.path("time_window_seconds").asInt();
                String severity = node.path("severity").asText("medium");
                String action = node.path("action").asText("alert");
                Rule rule = new Rule(eventType, minFailures, timeWindow, severity, action);
                rulesMap.put(eventType, rule);
            }
            System.out.println("[RULE ENGINE] Loaded rules: " + rulesMap);
        } catch (Exception e) {
            System.err.println("[RULE ENGINE] Failed to load rules: " + e.getMessage());
        }
    }

    public static boolean shouldTriggerAlert(String eventType, int failures) {
        Rule rule = rulesMap.get(eventType);
        if (rule == null) {
            return false;
        }
        return failures >= rule.minFailures && "alert".equalsIgnoreCase(rule.action);
    }

    public static boolean shouldLogOnly(String eventType, int failures) {
        Rule rule = rulesMap.get(eventType);
        if (rule == null) {
            return false;
        }
        return failures >= rule.minFailures && "log".equalsIgnoreCase(rule.action);
    }

    public static String getSeverity(String eventType) {
        Rule rule = rulesMap.get(eventType);
        if (rule == null) {
            return "unknown";
        }
        return rule.severity;
    }
}
