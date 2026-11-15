import { useSyncExternalStore } from "react";
import { isSoundOn, isSpeaking, subscribe, subscribeSpeech } from "./sound.js";

export const useSoundOn = () => useSyncExternalStore(subscribe, isSoundOn, () => false);
export const useSpeaking = () => useSyncExternalStore(subscribeSpeech, isSpeaking, () => false);
