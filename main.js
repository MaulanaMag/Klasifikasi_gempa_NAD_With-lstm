// Auto-fill koordinat kota
document.getElementById('citySelect').addEventListener('change', function() {
    const city = this.value;
    if (city) {
        fetch(`/get_city_coords?city=${city}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('latInput').value = data.lat;
                document.getElementById('lonInput').value = data.lon;
            });
    }
});

// Prediksi
document.getElementById('quakeForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    const data = {
        lat: document.getElementById('latInput').value,
        lon: document.getElementById('lonInput').value,
        depth: document.getElementById('depthInput').value,
        magnitude: document.getElementById('magInput').value
    };
    
    fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(result => {
        const resultDiv = document.getElementById('result');
        resultDiv.textContent = `Prediksi: ${result.prediction}`;
        resultDiv.style.display = 'block';
    });
});