function fetchLiveScores() {
    fetch('/api/live-scores')
        .then(response => response.json())
        .then(data => {
            const scoresDiv = document.getElementById('live-scores');
            if (Array.isArray(data)) {
                const scoreHtml = data.map(match => `
                    <div class="match">
                        <h2>${match['team-1']} vs ${match['team-2']}</h2>
                        <p>Score: ${match.score}</p>
                        <p>Type: ${match.type}</p>
                        <p>Status: ${match.status}</p>
                    </div>
                `).join('');
                scoresDiv.innerHTML = scoreHtml;
            } else {
                scoresDiv.innerHTML = `<p>${data}</p>`;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            document.getElementById('live-scores').innerHTML = '<p>Error fetching live scores</p>';
        });
}

// Fetch scores immediately and then every 60 seconds
fetchLiveScores();
setInterval(fetchLiveScores, 60000);


