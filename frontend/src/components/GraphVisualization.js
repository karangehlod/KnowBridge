import React from 'react';
import CytoscapeComponent from 'react-cytoscapejs';

function GraphVisualization({ graphData }) {
    const elements = graphData.map((node) => ({
        data: { id: node.id, label: node.label },
    }));

    return (
        <CytoscapeComponent
            elements={elements}
            style={{ width: '600px', height: '600px' }}
        />
    );
}

export default GraphVisualization;
