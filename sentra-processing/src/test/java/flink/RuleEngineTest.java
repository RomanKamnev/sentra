package flink;


import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class RuleEngineTest {

    @Test
    public void testTriggerAlertSSH() {
        boolean result = RuleEngine.shouldTriggerAlert("ssh", 6);
        assertTrue(result);
    }

    @Test
    public void testNoTriggerAlertSSH() {
        boolean result = RuleEngine.shouldTriggerAlert("ssh", 2);
        assertFalse(result);
    }

    @Test
    public void testGetSeverity() {
        String severity = RuleEngine.getSeverity("ssh");
        assertNotNull(severity);
    }
}
