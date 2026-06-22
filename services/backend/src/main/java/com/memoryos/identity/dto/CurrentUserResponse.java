package com.memoryos.identity.dto;

import java.util.UUID;

public record CurrentUserResponse(
        UUID id,
        String email,
        String name
) {
}

