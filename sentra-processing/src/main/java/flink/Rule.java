package flink;

public class Rule {
    public String eventType;
    public int minFailures;
    public int timeWindowSeconds;
    public String severity;
    public String action;

    public Rule(String eventType, int minFailures, int timeWindowSeconds, String severity, String action) {
        this.eventType = eventType;
        this.minFailures = minFailures;
        this.timeWindowSeconds = timeWindowSeconds;
        this.severity = severity;
        this.action = action;
    }

    @Override
    public String toString() {
        return "Rule{" +
                "eventType='" + eventType + '\'' +
                ", minFailures=" + minFailures +
                ", timeWindowSeconds=" + timeWindowSeconds +
                ", severity='" + severity + '\'' +
                ", action='" + action + '\'' +
                '}';
    }
}

