import React, { useRef, useEffect, useState } from 'react';
import * as THREE from 'three';
import { ForceGraph3D } from 'react-force-graph-3d';

const NeuralNetwork = ({ userData, clusterData, externalResonance }) => {
    const containerRef = useRef();
    const [graphData, setGraphData] = useState({ nodes: [], links: [] });
    const [selectedNode, setSelectedNode] = useState(null);

    useEffect(() => {
        // Generar datos del grafo basado en resonancia
        const neuralData = generateNeuralData(userData, clusterData, externalResonance);
        setGraphData(neuralData);
    }, [userData, clusterData, externalResonance]);

    const generateNeuralData = (user, cluster, resonance) => {
        const nodes = [];
        const links = [];

        // Nodo central del usuario
        nodes.push({
            id: 'user_center',
            name: 'Nodo Central',
            type: 'center',
            size: 20,
            color: '#ff6b6b',
            resonance: user.coherence || 0.5,
            metadata: user
        });

        // Nodos de clúster
        if (cluster.members) {
            cluster.members.forEach((member, index) => {
                const nodeId = `cluster_${index}`;
                nodes.push({
                    id: nodeId,
                    name: `Nodo ${index + 1}`,
                    type: 'cluster',
                    size: 8 + (member.resonance * 12),
                    color: getNodeColor(member.resonance),
                    resonance: member.resonance,
                    metadata: member
                });

                // Conectar con nodo central
                links.push({
                    source: 'user_center',
                    target: nodeId,
                    strength: member.resonance,
                    color: getLinkColor(member.resonance)
                });
            });
        }

        // Nodos de resonancia externa
        if (resonance.emerging_patterns) {
            resonance.emerging_patterns.forEach((pattern, index) => {
                const nodeId = `ext_${index}`;
                nodes.push({
                    id: nodeId,
                    name: pattern,
                    type: 'external',
                    size: 6,
                    color: '#74b9ff',
                    resonance: 0.7,
                    metadata: { pattern, source: 'external' }
                });

                links.push({
                    source: 'user_center',
                    target: nodeId,
                    strength: 0.3,
                    color: '#74b9ff'
                });
            });
        }

        // Conexiones entre nodos de clúster
        for (let i = 0; i < Math.min(5, nodes.length); i++) {
            for (let j = i + 1; j < Math.min(5, nodes.length); j++) {
                if (nodes[i].type === 'cluster' && nodes[j].type === 'cluster') {
                    const strength = Math.random() * 0.5;
                    links.push({
                        source: nodes[i].id,
                        target: nodes[j].id,
                        strength,
                        color: getLinkColor(strength)
                    });
                }
            }
        }

        return { nodes, links };
    };

    const getNodeColor = (resonance) => {
        const hue = resonance * 120; // 0 (rojo) to 120 (verde)
        return `hsl(${hue}, 70%, 50%)`;
    };

    const getLinkColor = (strength) => {
        const opacity = strength;
        return `rgba(255, 255, 255, ${opacity})`;
    };

    return (
        <div className="neural-network-container" ref={containerRef}>
            <h3>Mapa Neural de Resonancia</h3>
            
            <ForceGraph3D
                graphData={graphData}
                nodeLabel="name"
                nodeColor="color"
                nodeRelSize={6}
                linkColor="color"
                linkWidth={2}
                linkDirectionalParticles={2}
                linkDirectionalParticleSpeed={0.005}
                onNodeClick={setSelectedNode}
                nodeThreeObject={({ size, color, resonance }) => {
                    const geometry = new THREE.SphereGeometry(size / 10, 32, 32);
                    const material = new THREE.MeshPhongMaterial({ 
                        color,
                        transparent: true,
                        opacity: 0.8 + (resonance * 0.2)
                    });
                    const mesh = new THREE.Mesh(geometry, material);
                    
                    // Añadir glow effect para alta resonancia
                    if (resonance > 0.8) {
                        const glowGeometry = new THREE.SphereGeometry(size / 8, 32, 32);
                        const glowMaterial = new THREE.MeshBasicMaterial({
                            color,
                            transparent: true,
                            opacity: 0.3
                        });
                        const glowMesh = new THREE.Mesh(glowGeometry, glowMaterial);
                        mesh.add(glowMesh);
                    }
                    
                    return mesh;
                }}
                linkThreeObject={({ strength, color }) => {
                    const geometry = new THREE.CylinderGeometry(0.1, 0.1, 1, 8);
                    const material = new THREE.MeshBasicMaterial({ 
                        color,
                        transparent: true,
                        opacity: strength
                    });
                    return new THREE.Mesh(geometry, material);
                }}
            />

            {/* Panel de información del nodo seleccionado */}
            {selectedNode && (
                <div className="node-info-panel">
                    <h4>{selectedNode.name}</h4>
                    <p>Tipo: {selectedNode.type}</p>
                    <p>Resonancia: {(selectedNode.resonance * 100).toFixed(1)}%</p>
                    {selectedNode.metadata && (
                        <div className="node-metadata">
                            <pre>{JSON.stringify(selectedNode.metadata, null, 2)}</pre>
                        </div>
                    )}
                </div>
            )}

            {/* Leyenda del mapa */}
            <div className="neural-legend">
                <div className="legend-item">
                    <div className="color-box" style={{backgroundColor: '#ff6b6b'}}></div>
                    <span>Nodo Central (Usuario)</span>
                </div>
                <div className="legend-item">
                    <div className="color-box" style={{backgroundColor: '#a29bfe'}}></div>
                    <span>Nodos de Clúster</span>
                </div>
                <div className="legend-item">
                    <div className="color-box" style={{backgroundColor: '#74b9ff'}}></div>
                    <span>Resonancia Externa</span>
                </div>
            </div>
        </div>
    );
};

export default NeuralNetwork;