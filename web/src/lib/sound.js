// 8-bit sound effects (Web Audio) and a read-aloud voice (Web Speech API).
// No audio files and no network: the beeps are generated, the voice is the browser's own.
// Sound is OFF by default. The toggle is remembered per browser; storage may be unavailable, so every access is guarded.

const KEY = "walkback-sound";
let enabled = false;
try {
  enabled = localStorage.getItem(KEY) === "on";
} catch {
  /* storage blocked: stay off */
}

const listeners = new Set();
const emit = () => listeners.forEach((f) => f());

export const subscribe = (f) => {
  listeners.add(f);
  return () => listeners.delete(f);
};
export const isSoundOn = () => enabled;

export function setSoundOn(on) {
  enabled = Boolean(on);
  try {
    localStorage.setItem(KEY, enabled ? "on" : "off");
  } catch {
    /* ignore */
  }
  if (!enabled) stopSpeaking();
  emit();
  if (enabled) sfx("on"); // also unlocks audio inside the click that turned it on
}

// ---------- beeps ----------
let ctx = null;
function audio() {
  if (ctx) return ctx;
  const AC = typeof window !== "undefined" && (window.AudioContext || window.webkitAudioContext);
  if (!AC) return null;
  try {
    ctx = new AC();
  } catch {
    ctx = null;
  }
  return ctx;
}

function beep(freq, start, dur, { type = "square", vol = 0.04, slideTo = null } = {}) {
  const c = audio();
  if (!c) return;
  if (c.state === "suspended") c.resume().catch(() => {});
  const t0 = c.currentTime + start;
  const osc = c.createOscillator();
  const gain = c.createGain();
  osc.type = type;
  osc.frequency.setValueAtTime(freq, t0);
  if (slideTo) osc.frequency.linearRampToValueAtTime(slideTo, t0 + dur);
  gain.gain.setValueAtTime(vol, t0);
  gain.gain.exponentialRampToValueAtTime(0.0001, t0 + dur); // short fade, so no click at the end
  osc.connect(gain).connect(c.destination);
  osc.start(t0);
  osc.stop(t0 + dur + 0.02);
}

const SFX = {
  click: () => { beep(660, 0, 0.04); beep(880, 0.04, 0.05); },
  on: () => { beep(523, 0, 0.07); beep(659, 0.07, 0.07); beep(784, 0.14, 0.1); },
  place: () => { beep(392, 0, 0.06); beep(587, 0.06, 0.09); },
  done: () => { beep(523, 0, 0.07); beep(784, 0.08, 0.11); },
  // A result that misses the 95 % target must not sound like a win.
  shortfall: () => { beep(392, 0, 0.12, { type: "triangle", vol: 0.06 }); beep(294, 0.13, 0.2, { type: "triangle", vol: 0.06 }); },
  speak: () => { beep(988, 0, 0.05); beep(1319, 0.05, 0.07); },
  error: () => beep(160, 0, 0.22, { type: "sawtooth", vol: 0.05, slideTo: 90 }),
};

export function sfx(name) {
  if (!enabled) return;
  try {
    SFX[name]?.();
  } catch {
    /* sound must never break the app */
  }
}

let lastTick = 0;
export function tick(fraction) {
  if (!enabled) return;
  const now = performance.now();
  if (now - lastTick < 45) return; // a drag fires many events
  lastTick = now;
  try {
    beep(300 + Math.max(0, Math.min(1, fraction)) * 700, 0, 0.03, { vol: 0.03 });
  } catch {
    /* ignore */
  }
}

// ---------- voice ----------
export const speechSupported =
  typeof window !== "undefined" && "speechSynthesis" in window && "SpeechSynthesisUtterance" in window;

let speaking = false;
const speechListeners = new Set();
export const subscribeSpeech = (f) => {
  speechListeners.add(f);
  return () => speechListeners.delete(f);
};
export const isSpeaking = () => speaking;
const setSpeaking = (v) => {
  speaking = v;
  speechListeners.forEach((f) => f());
};

function pickVoice() {
  const voices = window.speechSynthesis.getVoices();
  return voices.find((v) => /^en[-_]US/i.test(v.lang)) || voices.find((v) => /^en/i.test(v.lang)) || null;
}

// Chrome stops long utterances after about 15 s, so read one sentence at a time.
function sentences(text) {
  return (text.match(/[^.!?]+[.!?]+(\s|$)|[^.!?]+$/g) || [text]).map((s) => s.trim()).filter(Boolean);
}

export function speak(text) {
  if (!speechSupported || !text) return;
  stopSpeaking();
  const parts = sentences(text);
  const voice = pickVoice();
  setSpeaking(true);
  parts.forEach((part, i) => {
    const u = new SpeechSynthesisUtterance(part);
    u.lang = "en-US";
    u.rate = 0.95;
    u.pitch = 0.8; // a little lower, to suit the console look
    if (voice) u.voice = voice;
    if (i === parts.length - 1) {
      u.onend = () => setSpeaking(false);
      u.onerror = () => setSpeaking(false);
    }
    window.speechSynthesis.speak(u);
  });
}

export function stopSpeaking() {
  if (!speechSupported) return;
  try {
    window.speechSynthesis.cancel();
  } catch {
    /* ignore */
  }
  if (speaking) setSpeaking(false);
}

if (typeof window !== "undefined") window.addEventListener("beforeunload", stopSpeaking);
