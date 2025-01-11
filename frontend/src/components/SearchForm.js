import React, { useState } from 'react';

function SearchForm({ onSearch }) {
    const [query, setQuery] = useState("");

    const handleSubmit = async (e) => {
        e.preventDefault();
        const response = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query }),
        });
        const data = await response.json();
        onSearch(data);
    };

    return (
        <form onSubmit={handleSubmit}>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Enter your query"
            />
            <button type="submit">Search</button>
        </form>
    );
}

export default SearchForm;
