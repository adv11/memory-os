package com.memoryos.identity.service;

import static org.assertj.core.api.Assertions.assertThat;

import com.memoryos.identity.entity.AppUser;
import com.memoryos.identity.repository.AppUserRepository;
import java.util.Map;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.orm.jpa.DataJpaTest;
import org.springframework.context.annotation.Import;
import org.springframework.security.authentication.TestingAuthenticationToken;
import org.springframework.security.oauth2.core.user.DefaultOAuth2User;
import org.springframework.security.oauth2.core.user.OAuth2User;
import org.springframework.test.context.ActiveProfiles;

@DataJpaTest
@ActiveProfiles("test")
@Import({OAuthUserProvisioningService.class})
class OAuthUserProvisioningServiceTest {

    @Autowired
    private OAuthUserProvisioningService service;

    @Autowired
    private AppUserRepository repository;

    @Test
    void createsUserFromGoogleProfile() {
        AppUser user = service.provision(authentication("google-123", "ava@example.com", "Ava"));

        assertThat(user.getId()).isNotNull();
        assertThat(user.getGoogleId()).isEqualTo("google-123");
        assertThat(user.getEmail()).isEqualTo("ava@example.com");
        assertThat(user.getName()).isEqualTo("Ava");
        assertThat(repository.findByGoogleId("google-123")).isPresent();
    }

    @Test
    void updatesExistingUserProfile() {
        service.provision(authentication("google-123", "old@example.com", "Old Name"));

        AppUser updated = service.provision(authentication("google-123", "new@example.com", "New Name"));

        assertThat(updated.getEmail()).isEqualTo("new@example.com");
        assertThat(updated.getName()).isEqualTo("New Name");
        assertThat(repository.findAll()).hasSize(1);
    }

    private TestingAuthenticationToken authentication(String googleId, String email, String name) {
        OAuth2User principal = new DefaultOAuth2User(
                java.util.List.of(),
                Map.of("sub", googleId, "email", email, "name", name),
                "sub"
        );
        return new TestingAuthenticationToken(principal, null);
    }
}

