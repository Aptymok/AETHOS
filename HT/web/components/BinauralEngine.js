export class BinauralEngine {
    constructor() {
        this.audioContext = null;
        this.oscillators = new Map();
        this.filters = new Map();
        this.panners = new Map();
        this.isActive = false;
        this.baseFrequencies = {
            alpha: 432,    // Hz base para estado alpha
            theta: 396,    // Hz base para estado theta
            delta: 285,    // Hz base para estado delta
            gamma: 528     // Hz base para estado gamma
        };
        this.currentState = 'alpha';
    }

    async init() {
        if (this.audioContext) return;

        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();
            
            // Crear osciladores base
            await this.createBaseOscillators();
            
            // Configurar nodos de procesamiento
            this.setupAudioGraph();
            
            this.isActive = true;
            console.log('Binaural Engine initialized');
            
        } catch (error) {
            console.error('Error initializing Binaural Engine:', error);
        }
    }

    async createBaseOscillators() {
        // Oscilador para oído izquierdo
        const leftOsc = this.audioContext.createOscillator();
        leftOsc.type = 'sine';
        leftOsc.frequency.value = this.baseFrequencies[this.currentState];
        
        // Oscilador para oído derecho (frecuencia ligeramente diferente para efecto binaural)
        const rightOsc = this.audioContext.createOscillator();
        rightOsc.type = 'sine';
        rightOsc.frequency.value = this.baseFrequencies[this.currentState] + 10; // Diferencia binaural
        
        // Guardar osciladores
        this.oscillators.set('left', leftOsc);
        this.oscillators.set('right', rightOsc);
        
        // Crear panners estéreo
        const leftPanner = this.audioContext.createStereoPanner();
        leftPanner.pan.value = -1; // Completamente izquierdo
        
        const rightPanner = this.audioContext.createStereoPanner();
        rightPanner.pan.value = 1; // Completamente derecho
        
        this.panners.set('left', leftPanner);
        this.panners.set('right', rightPanner);
        
        // Crear filtros para suavizar el sonido
        const leftFilter = this.audioContext.createBiquadFilter();
        leftFilter.type = 'lowpass';
        leftFilter.frequency.value = 1000;
        
        const rightFilter = this.audioContext.createBiquadFilter();
        rightFilter.type = 'lowpass';
        rightFilter.frequency.value = 1000;
        
        this.filters.set('left', leftFilter);
        this.filters.set('right', rightFilter);
    }

    setupAudioGraph() {
        const leftOsc = this.oscillators.get('left');
        const rightOsc = this.oscillators.get('right');
        const leftPanner = this.panners.get('left');
        const rightPanner = this.panners.get('right');
        const leftFilter = this.filters.get('left');
        const rightFilter = this.filters.get('right');
        
        // Conectar: Osc → Filter → Panner → Destination
        leftOsc.connect(leftFilter);
        leftFilter.connect(leftPanner);
        leftPanner.connect(this.audioContext.destination);
        
        rightOsc.connect(rightFilter);
        rightFilter.connect(rightPanner);
        rightPanner.connect(this.audioContext.destination);
        
        // Iniciar osciladores
        leftOsc.start();
        rightOsc.start();
    }

    setBrainwaveState(state, intensity = 0.5) {
        this.currentState = state;
        const baseFreq = this.baseFrequencies[state];
        
        // Aplicar efecto binaural basado en el estado cerebral
        const binauralBeat = this.calculateBinauralBeat(state, intensity);
        
        const leftOsc = this.oscillators.get('left');
        const rightOsc = this.oscillators.get('right');
        
        if (leftOsc && rightOsc) {
            leftOsc.frequency.setValueAtTime(baseFreq, this.audioContext.currentTime);
            rightOsc.frequency.setValueAtTime(baseFreq + binauralBeat, this.audioContext.currentTime);
        }
        
        console.log(`Brainwave state changed to: ${state}, intensity: ${intensity}`);
    }

    calculateBinauralBeat(state, intensity) {
        // Diferentes frecuencias binaurales para diferentes estados
        const beatFrequencies = {
            delta: 0.5,    // 0.5-4 Hz - Sueño profundo
            theta: 5,      // 4-8 Hz - Meditación, creatividad
            alpha: 10,     // 8-12 Hz - Relajación alerta
            gamma: 40      // 30-100 Hz - Cognición alta
        };
        
        return beatFrequencies[state] * intensity;
    }

    updateFromResonance(resonanceData) {
        if (!this.isActive) return;
        
        // Mapear resonancia a estados cerebrales
        const resonance = resonanceData.resonance_frequency || 0.5;
        const collectiveMood = resonanceData.collective_emotions || {};
        
        // Determinar estado basado en resonancia externa
        let targetState = 'alpha';
        let intensity = 0.5;
        
        if (resonance > 0.7) {
            targetState = 'gamma'; // Alta resonancia → estado gamma
            intensity = 0.8;
        } else if (resonance < 0.3) {
            targetState = 'theta'; // Baja resonancia → estado theta
            intensity = 0.6;
        }
        
        // Ajustar basado en emociones colectivas
        if (collectiveMood.joy > 0.7) {
            targetState = 'gamma';
            intensity = collectiveMood.joy;
        } else if (collectiveMood.fear > 0.6) {
            targetState = 'delta';
            intensity = collectiveMood.fear * 0.5;
        }
        
        this.setBrainwaveState(targetState, intensity);
        
        // Aplicar modulaciones basadas en patrones emergentes
        this.applyPatternModulation(resonanceData.emerging_patterns);
    }

    applyPatternModulation(patterns) {
        if (!patterns || !this.audioContext) return;
        
        patterns.forEach(pattern => {
            switch(pattern) {
                case 'colectivo_expansivo':
                    this.modulateFrequency(5, 0.3); // Modulación suave ascendente
                    break;
                case 'resonancia_alta':
                    this.modulateFrequency(10, 0.5); // Modulación más intensa
                    break;
                case 'tension_colectiva':
                    this.modulateFrequency(-8, 0.4); // Modulación descendente
                    break;
            }
        });
    }

    modulateFrequency(delta, duration = 1.0) {
        const leftOsc = this.oscillators.get('left');
        const rightOsc = this.oscillators.get('right');
        
        if (leftOsc && rightOsc) {
            const currentTime = this.audioContext.currentTime;
            
            leftOsc.frequency.exponentialRampToValueAtTime(
                leftOsc.frequency.value + delta,
                currentTime + duration
            );
            
            rightOsc.frequency.exponentialRampToValueAtTime(
                rightOsc.frequency.value + delta,
                currentTime + duration
            );
        }
    }

    setSpatialPosition(x, y, z) {
        // En un sistema avanzado, usaría Web Audio API's PannerNode para posicionamiento 3D
        const leftPanner = this.panners.get('left');
        const rightPanner = this.panners.get('right');
        
        if (leftPanner && rightPanner) {
            // Simular posicionamiento espacial básico
            leftPanner.pan.value = Math.max(-1, Math.min(1, -x));
            rightPanner.pan.value = Math.max(-1, Math.min(1, x));
        }
    }

    stop() {
        if (this.audioContext) {
            this.oscillators.forEach(osc => osc.stop());
            this.audioContext.close();
            this.audioContext = null;
            this.isActive = false;
        }
    }

    // Método para sincronizar con visualizaciones
    getCurrentAudioData() {
        return {
            state: this.currentState,
            leftFrequency: this.oscillators.get('left')?.frequency.value || 0,
            rightFrequency: this.oscillators.get('right')?.frequency.value || 0,
            isActive: this.isActive
        };
    }
}