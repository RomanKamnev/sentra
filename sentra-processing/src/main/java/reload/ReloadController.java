package reload;

import flink.RuleEngine;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
class ReloadController {

    //TODO Consider cert auth ✅ Да (обязательно HTTPS + IP-ограничение + Auth)

    @PostMapping("/reload")
    public String reloadRules() {
        RuleEngine.reloadRules();
        return "Rules reloaded successfully";
    }
}
