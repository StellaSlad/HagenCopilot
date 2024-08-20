/**
 * personas.ts
 *
 * This module defines the personas used in the application, including the assistant and user personas.
 * Each persona includes a name, avatar, and optional tagline.
 *
 */

import { PersonaOptions } from "@nlux/react";
import assistantAvatar from "./assets/hagencopilot_avatar_light.png";
import userAvatar from "./assets/user_avatar.svg";

/**
 * The personas used in the application.
 *
 * @type {PersonaOptions}
 */
export const personas: PersonaOptions = {
  assistant: {
    name: "HagenCopilot",
    avatar: assistantAvatar,
    tagline: "Dein virtueller Assistent für das Fernstudium",
  },
  user: {
    name: "User",
    avatar: userAvatar,
  },
};
