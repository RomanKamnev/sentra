package util;

import config.MappingConfig;
import org.apache.flink.api.java.tuple.Tuple5;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;


public class FlexibleLoginParserTest {

    @Test
    public void testParseValidSSHEvent() {
        MappingConfig mappingConfig = new MappingConfig("default-mapping-config.json"); // <-- укажи свой конфиг
        FlexibleLoginParser parser = new FlexibleLoginParser(mappingConfig);

        String json = "{\"event_type\":\"ssh\",\"ip\":\"192.168.1.1\",\"failures\":3,\"timestamp\":1745678000,\"username\":\"admin\"}";

        Tuple5<String, Integer, Long, String, String> result = parser.parse(json);

        assertEquals("192.168.1.1", result.f0);
        assertEquals(3, result.f1);
        assertEquals(1745678000L, result.f2);
        assertEquals("ssh", result.f3);
        assertEquals("admin", result.f4);
    }

    @Test
    public void testParseInvalidEvent() {
        MappingConfig mappingConfig = new MappingConfig("default-mapping-config.json");
        FlexibleLoginParser parser = new FlexibleLoginParser(mappingConfig);

        String json = "{}";

        Tuple5<String, Integer, Long, String, String> result = parser.parse(json);

        assertEquals("unknown", result.f0);
        assertEquals(0, result.f1);
//        assertEquals(1745758654518L, result.f2);
        assertEquals("unknown", result.f3);
        assertEquals("unknown", result.f4);
    }
}
