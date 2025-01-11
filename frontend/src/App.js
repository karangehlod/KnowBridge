import React, { useState } from 'react';
import axios from 'axios';
import Graph from 'react-graph-vis';

function App() {
    const [query, setQuery] = useState('');
    const [response, setResponse] = useState(null);

    const handleQuery = async () => {
        const result = await axios.post('http://localhost:8000/query', { user_query: query });
        setResponse(result.data);
    };

    return (
        <div>
            <input 
                type="text" 
                value={query} 
                onChange={(e) => setQuery(e.target.value)} 
                placeholder="Enter your query" 
            />
            <button onClick={handleQuery}>Submit</button>
            {response && (
                <div>
                    <h3>Summary:</h3>
                    <p>{response.summary}</p>
                    <h3>Graph Visualization:</h3>
                    <Graph
                        graph={response.graph_response}
                        options={{ layout: { hierarchical: true }, edges: { color: "#000000" } }}
                    />
                </div>
            )}
        </div>
    );
}

export default App;
