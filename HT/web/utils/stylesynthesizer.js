// web/utils/styleSynthesizer.js
export class StyleSynthesizer {
  static generateCSSFromMetrics(metrics, baseTheme = "dark") {
    // metrics: {coherence, entropy, alignment, cluster}
    const hue = metrics.coherence * 120; // 0-120 (rojo-verde)
    const saturation = 50 + (metrics.alignment * 50);
    const intensity = metrics.entropy * 100;
    
    return `
      :root {
        --primary-hue: ${hue};
        --saturation: ${saturation}%;
        --intensity: ${intensity}%;
        --bg-color: hsl(${hue}, ${saturation}%, ${10 + intensity/10}%);
        --text-glow: 0 0 10px hsl(${hue}, ${saturation}%, 80%);
      }
      body { 
        background: var(--bg-color);
        transition: all 0.5s ease;
      }
    `;
  }
}