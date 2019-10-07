package userRolesService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.client.RestTemplate;

/*
 * This would live in the authorization service rather than in each project that needed to communicate with the User Portal
 * We would likely then send in the X-API-TOKEN from the calling app rather than having one for all the apps, or hardcoding it in some way
 */

@Controller
public class UserRoleController {

	private final Logger log = LoggerFactory.getLogger(this.getClass());

	@RequestMapping(value = "/v1/user/info/{shibId}", method = RequestMethod.GET)
	public @ResponseBody String getUserInfo(@PathVariable("shibId") String shibId) {

		HttpHeaders headers = new HttpHeaders();
		// We will need to create a token for each application
		headers.set("X-API-TOKEN", "1ef4ecb8-2c2a-48af-889b-3ceb9ca9d102");
		HttpEntity<String> entity = new HttpEntity<>("body", headers);

		RestTemplate restTemplate = new RestTemplate();
		try {
			ResponseEntity<String> result = restTemplate.exchange("https://testuserportal.kpmp.org/api/user/" + shibId,
					HttpMethod.GET, entity, String.class);
			log.info(result.getStatusCode().toString());
			String resultString = result.getBody();

			log.info(resultString);

			return resultString;
		} catch (Exception e) {
			log.error(e.getMessage());
			return null;
		}
	}

	@RequestMapping(value = "/v1/testSessions", method = RequestMethod.GET)
	public @ResponseBody String validUser() {
		return "You are verified";
	}

}
