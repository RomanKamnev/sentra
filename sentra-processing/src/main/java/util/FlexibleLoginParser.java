package util;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import config.MappingConfig;
import org.apache.flink.api.java.tuple.Tuple5;

public class FlexibleLoginParser {

    private static final ObjectMapper objectMapper = new ObjectMapper();
    private final MappingConfig mapping;

    public FlexibleLoginParser(MappingConfig mapping) {
        this.mapping = mapping;
    }

    public Tuple5<String, Integer, Long, String, String> parse(String line) {
        try {
            JsonNode root = getJsonNode(line);

            String ip = root.path(mapping.getField("ip")).asText("unknown");
            int failures = root.path(mapping.getField("failures")).asInt(0);
            long timestamp = root.path(mapping.getField("timestamp")).asLong(System.currentTimeMillis());
            String eventType = root.path(mapping.getField("event_type")).asText("unknown");
            String username = root.path(mapping.getField("username")).asText("unknown");

            return Tuple5.of(ip, failures, timestamp, eventType, username);
        } catch (Exception e) {
            System.err.println("Error parsing JSON: " + e.getMessage());
            e.printStackTrace();
            return Tuple5.of("invalid", 0, 0L, "invalid", "invalid");
        }
    }

    private static JsonNode getJsonNode(String line) throws JsonProcessingException {
        JsonNode root;
        // Check if the string is double-quoted
        if (line.startsWith("\"") && line.endsWith("\"") && line.length() > 2) {
            // Remove outer quotes
            String unquotedLine = line.substring(1, line.length() - 1);

            // Handle escaped JSON strings
            if (unquotedLine.startsWith("{") && unquotedLine.endsWith("}")) {
                // Direct parse of unquoted JSON
                root = objectMapper.readTree(unquotedLine);
            } else if (unquotedLine.startsWith("\\\"") && unquotedLine.endsWith("\\\"")) {
                // Handle double escaped JSON
                String cleanedLine = objectMapper.readValue(line, String.class);
                root = objectMapper.readTree(cleanedLine);
            } else {
                // Try to parse as is
                root = objectMapper.readTree(unquotedLine);
            }
        } else if (line.startsWith("\"{") && line.endsWith("}\"")) {
            // Original logic for escaped JSON strings
            String cleanedLine = objectMapper.readValue(line, String.class);
            root = objectMapper.readTree(cleanedLine);
        } else {
            // Original logic for direct JSON
            root = objectMapper.readTree(line);
        }
        return root;
    }
}
