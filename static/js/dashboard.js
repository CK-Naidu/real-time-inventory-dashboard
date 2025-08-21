document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch('/api/kpi/weather-impact');
        const data = await response.json();
        const labels = data.map(item => item.weathercondition);   // lowercase keys from JSON
        const values = data.map(item => item.avgunitsold);

        new Chart(document.getElementById('weatherImpactChart'), {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Average Units Sold',
                    data: values,
                    backgroundColor: 'rgba(75, 192, 192, 0.6)',
                    borderColor: 'rgba(75,192,192,1)',
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (error) {
        console.error('Failed to load chart data:', error);
    }
});
