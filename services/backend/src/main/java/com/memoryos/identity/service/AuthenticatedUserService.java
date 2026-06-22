package com.memoryos.identity.service;

import com.memoryos.identity.entity.AppUser;
import com.memoryos.identity.repository.AppUserRepository;
import java.util.Map;
import org.springframework.security.core.Authentication;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class AuthenticatedUserService {
    private final AppUserRepository appUserRepository;

    public AuthenticatedUserService(AppUserRepository appUserRepository) {
        this.appUserRepository = appUserRepository;
    }

    @Transactional(readOnly = true)
    public AppUser requireCurrentUser(Authentication authentication) {
        OAuthProfile profile = OAuthProfile.from(authentication);
        return appUserRepository.findByGoogleId(profile.googleId())
                .orElseThrow(() -> new IllegalStateException("Authenticated user was not provisioned"));
    }

    record OAuthProfile(String googleId, String email, String name) {
        static OAuthProfile from(Authentication authentication) {
            if (authentication == null || !(authentication.getPrincipal() instanceof OAuth2User user)) {
                throw new IllegalStateException("OAuth user principal is required");
            }

            Map<String, Object> attributes = user.getAttributes();
            String googleId = requiredAttribute(attributes, "sub");
            String email = requiredAttribute(attributes, "email");
            String name = attributes.getOrDefault("name", email).toString();
            return new OAuthProfile(googleId, email, name);
        }

        private static String requiredAttribute(Map<String, Object> attributes, String key) {
            Object value = attributes.get(key);
            if (value == null || value.toString().isBlank()) {
                throw new IllegalStateException("Missing OAuth attribute: " + key);
            }
            return value.toString();
        }
    }
}

