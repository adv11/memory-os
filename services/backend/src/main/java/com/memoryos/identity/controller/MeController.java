package com.memoryos.identity.controller;

import static com.memoryos.common.api.ApiPaths.API_V1;

import com.memoryos.identity.dto.CurrentUserResponse;
import com.memoryos.identity.entity.AppUser;
import com.memoryos.identity.service.AuthenticatedUserService;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping(API_V1)
public class MeController {
    private final AuthenticatedUserService authenticatedUserService;

    public MeController(AuthenticatedUserService authenticatedUserService) {
        this.authenticatedUserService = authenticatedUserService;
    }

    @GetMapping("/me")
    public CurrentUserResponse me(Authentication authentication) {
        AppUser user = authenticatedUserService.requireCurrentUser(authentication);
        return new CurrentUserResponse(user.getId(), user.getEmail(), user.getName());
    }
}

