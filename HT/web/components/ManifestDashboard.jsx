import React, { useState, useEffect, useRef } from 'react';
import NeuralNetwork from './NeuralNetwork';
import { BinauralEngine } from './BinauralEngine';
import ManifestDashboard from './ManifestDashboard';

const EnhancedDashboard = () => {
    const [externalResonance, setExternalResonance] = useState({});
    const [neuralData, setNeuralData] = useState({});
    const [audioData, setAudioData] = useState({});
    const [isAudioActive, setIsAudioActive] = useState(false);
    
    const binauralEngine = useRef();
    const resonanceInterval = useRef();

    useEffect(() => {
        // Inicializar motores
        initializeEngines();
        
        // Configurar actualización periódica de resonancia
        resonanceInterval.current = setInterval(fetchExternalResonance, 30000); // Cada 30 segundos
        
        return () => {
            cleanupEngines();
        };
    }, []);

    const initializeEngines = async () => {
        // Inicializar motor binaural
        binauralEngine.current = new BinauralEngine();
        await binauralEngine.current.init();
        
        // Cargar resonancia inicial
        await fetchExternalResonance();
    };

    const fetchExternalResonance = async () => {
        try {
            const response = await fetch('/api/resonance/external');
            const data = await response.json();
            
            setExternalResonance(data);
            
            // Actualizar audio basado en nueva resonancia
            if (binauralEngine.current) {
                binauralEngine.current.updateFromResonance(data);
            }
            
            // Actualizar datos neurales
            updateNeuralData(data);
            
        } catch (error) {
            console.error('Error fetching external resonance:', error);
        }
    };

    const updateNeuralData = (resonanceData) => {
        const simulate = process.env.REACT_APP_SIMULATE === 'true';
        if (!simulate) {
            // En modo real, intentar llamar a API de nodos (no implementado)
            setNeuralData({members: [], collectiveMetrics:{}});
            return;
        }

        // Deterministic simulated data when REACT_APP_SIMULATE=true
        const seed = (resonanceData.temporal_marker || '') + (resonanceData.resonance_frequency || '0');
        let hash = 0;
        for (let i = 0; i < seed.length; i++) {
            const ch = seed.charCodeAt(i);
            hash = ((hash << 5) - hash) + ch;
            hash |= 0;
        }

        const members = Array.from({length: 15}, (_, i) => {
            const localSeed = Math.abs(hash + i * 997) % 1000;
            const resonance = (localSeed % 50) / 100 + 0.3; // 0.3 - 0.8
            const coherence = ((localSeed + 30) % 40) / 100 + 0.4; // 0.4 - 0.8
            return {
                id: i,
                resonance,
                coherence,
                cluster: ['AETHOS', 'VÍNCULO', 'TRANSFORMACIÓN'][i % 3]
            };
        });

        const collectiveMetrics = {
            overallResonance: resonanceData.resonance_frequency || 0.5,
            emotionalCoherence: resonanceData.collective_emotions 
                ? Object.values(resonanceData.collective_emotions).reduce((a, b) => a + b, 0) / Object.values(resonanceData.collective_emotions).length
                : 0.5
        };

        setNeuralData({members, collectiveMetrics});
    };

    const toggleAudio = () => {
        if (isAudioActive) {
            binauralEngine.current.stop();
        } else {
            binauralEngine.current.init();
        }
        setIsAudioActive(!isAudioActive);
    };

    const cleanupEngines = () => {
        if (binauralEngine.current) {
            binauralEngine.current.stop();
        }
        if (resonanceInterval.current) {
            clearInterval(resonanceInterval.current);
        }
    };

    return (
        <div className="enhanced-dashboard">
            {/* Header con controles de audio */}
            <div className="dashboard-header">
                <h1>ECOSISTEMA AETHOS - RESONANCIA ACTIVA</h1>
                <div className="audio-controls">
                    <button 
                        onClick={toggleAudio}
                        className={`audio-btn ${isAudioActive ? 'active' : ''}`}
                    >
                        {isAudioActive ? '🔊 Audio On' : '🔇 Audio Off'}
                    </button>
                    <span className="resonance-info">
                        Frecuencia: {externalResonance.resonance_frequency?.toFixed(1) || '--'} Hz
                    </span>
                </div>
            </div>

            {/* Layout de tres columnas */}
            <div className="dashboard-layout">
                {/* Columna izquierda: Mapa Neural */}
                <div className="panel neural-panel">
                    <h2>Mapa de Resonancia Neural</h2>
                    <NeuralNetwork 
                        userData={neuralData}
                        clusterData={neuralData}
                        externalResonance={externalResonance}
                    />
                </div>

                {/* Columna central: Manifestación */}
                <div className="panel manifestation-panel">
                    <ManifestDashboard />
                </div>

                {/* Columna derecha: Datos de Resonancia Externa */}
                <div className="panel resonance-panel">
                    <h2>Resonancia Externa</h2>
                    <div className="resonance-data">
                        <div className="resonance-item">
                            <h4>Estado Colectivo</h4>
                            <p>Emoción dominante: {externalResonance.collective_emotions?.dominant_emotion || '--'}</p>
                            <p>Coherencia social: {((externalResonance.collective_emotions?.social_coherence || 0) * 100).toFixed(1)}%</p>
                        </div>
                        
                        <div className="resonance-item">
                            <h4>Patrones Emergentes</h4>
                            <ul>
                                {(externalResonance.emerging_patterns || []).map((pattern, index) => (
                                    <li key={index}>{pattern}</li>
                                ))}
                            </ul>
                        </div>
                        
                        <div className="resonance-item">
                            <h4>Datos Cósmicos</h4>
                            <p>Actividad solar: {((externalResonance.cosmic_data?.solar_activity || 0) * 100).toFixed(1)}%</p>
                            <p>Fase lunar: {((externalResonance.cosmic_data?.moon_phase || 0) * 100).toFixed(1)}%</p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Barra de estado inferior */}
            <div className="status-bar">
                <div className="status-item">
                    <span>Estado Audio: </span>
                    <strong>{isAudioActive ? 'ACTIVO' : 'INACTIVO'}</strong>
                </div>
                <div className="status-item">
                    <span>Resonancia Global: </span>
                    <strong>{((externalResonance.resonance_frequency || 0) * 100).toFixed(1)}%</strong>
                </div>
                <div className="status-item">
                    <span>Nodos Activos: </span>
                    <strong>{neuralData.members?.length || 0}</strong>
                </div>
                <div className="status-item">
                    <span>Última Actualización: </span>
                    <strong>{new Date().toLocaleTimeString()}</strong>
                </div>
            </div>
        </div>
    );
};

export default EnhancedDashboard;