from consumer.kafka_consumer import create_consumer
from parser.alert_parser import parse_alert
from prompt.prompt_builder import build_prompt
from llm.client import MockLLMClient
from observability.logger import logger
from observability.metrics import metrics
import time

def main():
    consumer = create_consumer()
    llm_client = MockLLMClient()

    logger.info("🟢 Sentra LLM Agent is running...")

    for message in consumer:
        alert_text = message.value
        logger.info(f"Received alert: {alert_text}")

        alert_data = parse_alert(alert_text)
        if not alert_data:
            logger.warning("Could not parse alert.")
            metrics.record_failure()
            continue

        prompt = build_prompt(alert_data)
        logger.info(f"Generated prompt:\n{prompt}")

        start_time = time.time()
        try:
            llm_response = llm_client.query(prompt)
            latency = time.time() - start_time
            metrics.record_latency(latency)
            metrics.record_success()

            logger.info(f"LLM Response: {llm_response}")
            logger.info(f"Latency: {latency:.2f} seconds")

        except Exception as e:
            latency = time.time() - start_time
            metrics.record_latency(latency)
            metrics.record_failure()
            logger.error(f"Error during LLM inference: {e}")

if __name__ == "__main__":
    main()
