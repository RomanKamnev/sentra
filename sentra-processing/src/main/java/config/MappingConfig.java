package config;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;

import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

public class MappingConfig {

    private final Map<String, String> fieldMappings = new HashMap<>();

    public MappingConfig(String configFileName) {
        try (InputStream input = MappingConfig.class.getClassLoader().getResourceAsStream(configFileName)) {
            if (input == null) {
                throw new IllegalArgumentException("Mapping config not found: " + configFileName);
            }
            ObjectMapper mapper = new ObjectMapper();
            JsonNode root = mapper.readTree(input);

            JsonNode fieldsNode = root.path("fields");
            fieldsNode.fieldNames().forEachRemaining(field -> {
                fieldMappings.put(field, fieldsNode.path(field).asText(field));
            });
        } catch (Exception e) {
            throw new RuntimeException("Failed to load mapping config", e);
        }
    }

    public String getField(String standardName) {
        return fieldMappings.getOrDefault(standardName, standardName);
    }
}
