document.addEventListener('DOMContentLoaded', async () => {
  try {
    // Weather Impact Chart
    const weatherRes = await fetch('/api/kpi/weather-impact');
    const weatherData = await weatherRes.json();
    const weatherLabels = weatherData.map(item => item.WeatherCondition);
    const weatherValues = weatherData.map(item => item.AvgUnitsSold);

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

    // Sales by Region Chart
    const regionRes = await fetch('/api/kpi/sales-by-region');
    const regionData = await regionRes.json();
    const regionLabels = regionData.map(item => item.Region);
    const regionValues = regionData.map(item => item.TotalUnitsSold);

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

    // Sales by Category Chart
    const categoryRes = await fetch('/api/kpi/sales-by-category');
    const categoryData = await categoryRes.json();
    const categoryLabels = categoryData.map(item => item.Category);
    const categoryValues = categoryData.map(item => item.TotalUnitsSold);

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

    // Sales Trend Chart
    const trendRes = await fetch('/api/kpi/sales-trend');
    const trendData = await trendRes.json();
    const trendLabels = trendData.map(item => item.SaleDate);
    const trendValues = trendData.map(item => item.TotalUnitsSold);

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
