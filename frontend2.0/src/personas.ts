import { PersonaOptions } from "@nlux/react";
import assistantAvatar from "./assets/hagencopilot_small.png";

import userAvatar from "./assets/user_avatar.svg";

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
