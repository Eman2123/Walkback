import { setSoundOn } from "../lib/sound.js";
import { useSoundOn } from "../lib/useSound.js";

// Master switch for the sound effects. Off by default, so nothing plays until a visitor asks for it.
export default function SoundToggle() {
  const on = useSoundOn();
  return (
    <button
      type="button"
      data-silent
      aria-pressed={on}
      aria-label={on ? "Sound effects on. Press to mute." : "Sound effects off. Press to turn on."}
      onClick={() => setSoundOn(!on)}
      className="px-toggle"
    >
      <svg width="16" height="16" viewBox="0 0 8 8" shapeRendering="crispEdges" aria-hidden="true">
        <path d="M0 3h2l2-2v6L2 5H0z" fill="currentColor" />
        {on ? (
          <path d="M5 2h1v4H5zM6 1h1v1H6zM6 6h1v1H6z" fill="currentColor" />
        ) : (
          <path d="M5 2h1v1H5zM6 3h1v1H6zM5 4h1v1H5zM6 5h1v1H6z" fill="currentColor" />
        )}
      </svg>
      Sound {on ? "on" : "off"}
    </button>
  );
}
