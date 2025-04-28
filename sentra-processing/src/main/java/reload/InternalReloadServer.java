package reload;

import com.sun.net.httpserver.HttpServer;
import flink.RuleEngine;

import java.io.OutputStream;
import java.net.InetSocketAddress;

public class InternalReloadServer {

    private static HttpServer server;

    public static void start(int port) throws Exception {
        server = HttpServer.create(new InetSocketAddress(port), 0);
        server.createContext("/internal/reload", exchange -> {
            if ("POST".equals(exchange.getRequestMethod())) {
                RuleEngine.reloadRules();
                String response = "Rules reloaded successfully";
                exchange.sendResponseHeaders(200, response.getBytes().length);
                OutputStream os = exchange.getResponseBody();
                os.write(response.getBytes());
                os.close();
            } else {
                exchange.sendResponseHeaders(405, -1); // Method Not Allowed
            }
        });
        server.setExecutor(null);
        server.start();
        System.out.println("[RELOAD SERVER] Started on port " + port);
    }

    public static void stop() {
        if (server != null) {
            server.stop(0);
            System.out.println("[RELOAD SERVER] Stopped.");
        }
    }
}

