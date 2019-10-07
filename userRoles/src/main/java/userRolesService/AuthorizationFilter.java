package userRolesService;

import java.io.IOException;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.stereotype.Component;

import com.fasterxml.jackson.databind.ObjectMapper;

@Component
public class AuthorizationFilter implements Filter {

	private final Logger log = LoggerFactory.getLogger(this.getClass());
	private UTF8Encoder encoder;
	private UserRoleController userRoleController;

	public AuthorizationFilter(UTF8Encoder encoder, UserRoleController userRoleController) {
		this.encoder = encoder;
		this.userRoleController = userRoleController;
	}

	@Override
	public void init(FilterConfig filterConfig) throws ServletException {
		// TODO Auto-generated method stub

	}

	@Override
	public void doFilter(ServletRequest incomingRequest, ServletResponse incominResponse, FilterChain chain)
			throws IOException, ServletException {
		HttpServletRequest request = (HttpServletRequest) incomingRequest;
		HttpServletResponse response = (HttpServletResponse) incominResponse;

		HttpSession existingSession = request.getSession(false);
		Cookie[] cookies = request.getCookies();
		String value = handleNull(request.getHeader("eppn"));
		String shibId = encoder.convertFromLatin1(value);

		if (existingSession != null) {
			log.info("have an existing session");
			for (Cookie cookie : cookies) {
				log.info("had a cookie");
				if (cookie.getName().equals("shibid")) {
					log.info("found a cookie");
					if (cookie.getValue().equals(shibId)) {
						log.info("cookie is goood");
						chain.doFilter(incomingRequest, response);
					} else {
						log.error("wrong user");
						existingSession.invalidate();
					}
				} else {
					log.info("no existing session...now looking up user");
					// do the call
				}
			}

		} else {
			log.info("no existing session...now looking up user");

			// This would actually be a request to the auth service that could handle
			// communication to UserPortal
			// For simplicities sake, I kept all the code in one project for this example
			String userInfo = userRoleController.getUserInfo(shibId);
			if (userInfo != null) {
				ObjectMapper mapper = new ObjectMapper();
				User user = mapper.readValue(userInfo, User.class);

				if (user.getGroups().contains("uw_rit_kpmp_role_developer")) {
					log.info("Creating a new session");
					HttpSession session = request.getSession(true);
					// setting session timeout to 5 minutes...we'll probably want something
					// different for realsies
					session.setMaxInactiveInterval(5 * 60);
					Cookie message = new Cookie("shibid", user.getShibId());
					session.setAttribute("roles", user.getGroups());
					response.addCookie(message);
					chain.doFilter(incomingRequest, response);
				} else {
					log.error("User " + user.getShibId() + " does not have permission to use this app.");
					response.sendRedirect("http://welcome.kpmp.org/shibds");
				}
			} else {
				log.error("We were unable to find user information for shib id: " + shibId);
				response.sendRedirect("http://welcome.kpmp.org/shibds");
			}

		}

	}

	@Override
	public void destroy() {
		// TODO Auto-generated method stub

	}

	private String handleNull(String value) {
		if (value == null) {
			return "";
		}
		return value;
	}

}
