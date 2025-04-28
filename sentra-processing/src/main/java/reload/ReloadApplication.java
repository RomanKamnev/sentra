package reload;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.web.SecurityFilterChain;

@SpringBootApplication
public class ReloadApplication {

    public static void main(String[] args) {
        SpringApplication.run(ReloadApplication.class, args);
    }

    @EnableWebSecurity
    public static class SecurityConfig {

        @Bean
        public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
            http
                    .authorizeHttpRequests(auth -> auth
                            .anyRequest().authenticated()
                    )
                    .securityContext(context -> context
                            .requireExplicitSave(false)
                    )
                    .httpBasic(customizer -> {})
                    .csrf(csrf -> csrf.disable());
            return http.build();
        }
    }
}
