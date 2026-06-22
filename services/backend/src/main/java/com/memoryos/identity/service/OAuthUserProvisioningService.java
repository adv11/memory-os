package com.memoryos.identity.service;

import com.memoryos.identity.entity.AppUser;
import com.memoryos.identity.repository.AppUserRepository;
import java.util.UUID;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

@Service
public class OAuthUserProvisioningService {
    private final AppUserRepository appUserRepository;

    public OAuthUserProvisioningService(AppUserRepository appUserRepository) {
        this.appUserRepository = appUserRepository;
    }

    @Transactional
    public AppUser provision(Authentication authentication) {
        AuthenticatedUserService.OAuthProfile profile = AuthenticatedUserService.OAuthProfile.from(authentication);
        return appUserRepository.findByGoogleId(profile.googleId())
                .map(user -> {
                    user.updateProfile(profile.email(), profile.name());
                    return user;
                })
                .orElseGet(() -> appUserRepository.save(
                        new AppUser(UUID.randomUUID(), profile.googleId(), profile.email(), profile.name())
                ));
    }
}

