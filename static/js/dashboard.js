document.addEventListener('DOMContentLoaded', async () => {
  try {
    // Fetch and render Weather Impact Chart
    const weatherRes = await fetch('/api/kpi/weather-impact');
    if (!weatherRes.ok) throw new Error(`Weather Impact API error: ${weatherRes.status}`);
    const weatherData = await weatherRes.json();
    if (!Array.isArray(weatherData)) throw new Error('Weather Impact data is not an array');
    const weatherLabels = weatherData.map(item => item.weathercondition);
    const weatherValues = weatherData.map(item => item.avgunitsold);
    
    new Chart(document.getElementById('weatherImpactChart'), {
      type: 'bar',
      data: {
        labels: weatherLabels,
        datasets: [{
          label: 'Average Units Sold',
          data: weatherValues,
          backgroundColor: 'rgba(75, 192, 192, 0.6)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      },
      options: {
        scales: { y: { beginAtZero: true } }
      }
    });
    // Fetch and render Sales by Region Chart
    const regionRes = await fetch('/api/kpi/sales-by-region');
    if (!regionRes.ok) throw new Error(`Sales by Region API error: ${regionRes.status}`);
    const regionData = await regionRes.json();
    if (!Array.isArray(regionData)) throw new Error('Sales by Region data is not an array');
    const regionLabels = regionData.map(item => item.region);         // Corrected
    const regionValues = regionData.map(item => item.totalunitssold); // Corrected

    new Chart(document.getElementById('salesByRegionChart'), {
      type: 'pie',
      data: {
        labels: regionLabels,
        datasets: [{
          label: 'Sales by Region',
          data: regionValues,
          backgroundColor: [
            'rgba(255, 99, 132, 0.6)',
            'rgba(54, 162, 235, 0.6)',
            'rgba(255, 206, 86, 0.6)',
            'rgba(75, 192, 192, 0.6)'
          ],
          borderColor: 'rgba(255, 255, 255, 1)',
          borderWidth: 1
        }]
      }
    });

    // Fetch and render Sales by Category Chart
    const categoryRes = await fetch('/api/kpi/sales-by-category');
    if (!categoryRes.ok) throw new Error(`Sales by Category API error: ${categoryRes.status}`);
    const categoryData = await categoryRes.json();
    if (!Array.isArray(categoryData)) throw new Error('Sales by Category data is not an array');
    const categoryLabels = categoryData.map(item => item.category);       // Corrected
    const categoryValues = categoryData.map(item => item.totalunitssold); // Corrected

    new Chart(document.getElementById('salesByCategoryChart'), {
      type: 'doughnut',
      data: {
        labels: categoryLabels,
        datasets: [{
          label: 'Sales by Category',
          data: categoryValues,
          backgroundColor: [
            'rgba(153, 102, 255, 0.6)',
            'rgba(255, 159, 64, 0.6)',
            'rgba(255, 205, 86, 0.6)',
            'rgba(201, 203, 207, 0.6)'
          ],
          borderColor: 'rgba(255, 255, 255, 1)',
          borderWidth: 1
        }]
      }
    });

    // Fetch and render Sales Trend Chart
    const trendRes = await fetch('/api/kpi/sales-trend');
    if (!trendRes.ok) throw new Error(`Sales Trend API error: ${trendRes.status}`);
    const trendData = await trendRes.json();
    if (!Array.isArray(trendData)) throw new Error('Sales Trend data is not an array');
    const trendLabels = trendData.map(item => item.saledate);       // Corrected
    const trendValues = trendData.map(item => item.totalunitssold); // Corrected

    new Chart(document.getElementById('salesTrendChart'), {
      type: 'line',
      data: {
        labels: trendLabels,
        datasets: [{
          label: 'Sales Trend Over Time',
          data: trendValues,
          fill: false,
          borderColor: 'rgba(54, 162, 235, 1)',
          tension: 0.1
        }]
      }
    });

  } catch (error) {
    console.error('Failed to load chart data:', error);
  }
});
