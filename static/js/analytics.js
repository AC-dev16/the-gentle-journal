// Analytics Page JavaScript
class AnalyticsManager {
    constructor() {
        this.chart = null;
        this.currentPeriod = 30;
        this.visibleDatasets = {
            pain: true,
            mood: true,
            sleep: true
        };
        this.chartData = null;
        
        this.initialize();
    }

    initialize() {
        // Only run on analytics page
        if (!document.getElementById('analyticsChart')) {
            return;
        }

        this.setupEventListeners();
        this.loadChartData();
    }

    setupEventListeners() {
        // Period selection buttons
        document.querySelectorAll('.period-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                // Update active button
                document.querySelectorAll('.period-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                
                // Update period and reload data
                this.currentPeriod = parseInt(e.target.dataset.days);
                this.loadChartData();
            });
        });

        // Data toggle buttons
        document.querySelectorAll('.data-toggle-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const dataset = e.target.dataset.dataset;
                const isActive = e.target.classList.contains('active');
                
                // Toggle button state
                if (isActive) {
                    e.target.classList.remove('active');
                    e.target.classList.add('btn-outline-secondary');
                    this.visibleDatasets[dataset] = false;
                } else {
                    e.target.classList.add('active');
                    e.target.classList.remove('btn-outline-secondary');
                    this.visibleDatasets[dataset] = true;
                    
                    // Restore original color
                    if (dataset === 'pain') e.target.classList.add('btn-danger');
                    if (dataset === 'mood') e.target.classList.add('btn-success');
                    if (dataset === 'sleep') e.target.classList.add('btn-info');
                }
                
                this.updateChartVisibility();
            });
        });
    }

    async loadChartData() {
        try {
            const response = await fetch(`/api/analytics-data/?days=${this.currentPeriod}`);
            this.chartData = await response.json();
            
            this.createChart();
            this.updateChartInfo();
            this.generateInsights();
            
        } catch (error) {
            console.error('Error loading chart data:', error);
            this.showError('Failed to load chart data');
        }
    }

    createChart() {
        const ctx = document.getElementById('analyticsChart').getContext('2d');
        
        // Destroy existing chart
        if (this.chart) {
            this.chart.destroy();
        }

        // Prepare datasets
        const datasets = [];
        
        if (this.visibleDatasets.pain) {
            datasets.push({
                label: 'Pain Level',
                data: this.chartData.pain_data,
                borderColor: '#dc3545',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                tension: 0.3,
                fill: false,
                yAxisID: 'y'
            });
        }
        
        if (this.visibleDatasets.mood) {
            datasets.push({
                label: 'Mood Level',
                data: this.chartData.mood_data,
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                tension: 0.3,
                fill: false,
                yAxisID: 'y'
            });
        }
        
        if (this.visibleDatasets.sleep) {
            datasets.push({
                label: 'Sleep Hours',
                data: this.chartData.sleep_data,
                borderColor: '#17a2b8',
                backgroundColor: 'rgba(23, 162, 184, 0.1)',
                tension: 0.3,
                fill: false,
                yAxisID: 'y1'
            });
        }

        // Create chart
        this.chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: this.chartData.labels,
                datasets: datasets
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                interaction: {
                    mode: 'index',
                    intersect: false
                },
                plugins: {
                    title: {
                        display: true,
                        text: `Wellness Tracking - Last ${this.currentPeriod} Days`,
                        font: { size: 16, weight: 'bold' }
                    },
                    legend: {
                        position: 'top'
                    },
                    tooltip: {
                        callbacks: {
                            afterLabel: function(context) {
                                if (context.dataset.label === 'Pain Level' || context.dataset.label === 'Mood Level') {
                                    return '/10';
                                } else if (context.dataset.label === 'Sleep Hours') {
                                    return 'hours';
                                }
                                return '';
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        display: true,
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: {
                        type: 'linear',
                        display: true,
                        position: 'left',
                        beginAtZero: true,
                        max: 10,
                        title: {
                            display: true,
                            text: 'Pain/Mood Level (0-10)'
                        },
                        grid: {
                            drawOnChartArea: this.visibleDatasets.sleep ? false : true
                        }
                    },
                    y1: {
                        type: 'linear',
                        display: this.visibleDatasets.sleep,
                        position: 'right',
                        beginAtZero: true,
                        max: 24,
                        title: {
                            display: true,
                            text: 'Sleep Hours'
                        },
                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        });
    }

    updateChartVisibility() {
        if (!this.chart) return;
        
        this.createChart(); // Recreate chart with new visibility settings
    }

    updateChartInfo() {
        const info = document.getElementById('chartInfo');
        const entryCount = this.chartData.entry_count;
        const period = this.currentPeriod;
        
        let periodText = '';
        if (period === 7) periodText = '7 days';
        else if (period === 30) periodText = '1 month';
        else if (period === 90) periodText = '3 months';
        else if (period === 365) periodText = '1 year';
        
        info.textContent = `Showing ${entryCount} entries from the last ${periodText}`;
    }

    generateInsights() {
        const container = document.getElementById('insightsContainer');
        
        if (this.chartData.entry_count === 0) {
            container.innerHTML = '<p class="text-muted">No data available for the selected period. Try selecting a longer time range or add more entries.</p>';
            return;
        }

        const insights = this.calculateInsights();
        this.displayInsights(insights, container);
    }

    calculateInsights() {
        const { pain_data, mood_data, sleep_data } = this.chartData;
        const insights = [];

        // Calculate averages
        const avgPain = pain_data.reduce((a, b) => a + b, 0) / pain_data.length;
        const avgMood = mood_data.reduce((a, b) => a + b, 0) / mood_data.length;
        const avgSleep = sleep_data.reduce((a, b) => a + b, 0) / sleep_data.length;

        // Pain insights
        if (avgPain <= 3) {
            insights.push({
                icon: 'bi-check-circle-fill text-success',
                title: 'Great Pain Management!',
                message: `Your average pain level (${avgPain.toFixed(1)}/10) is in the low range. Keep up your current management strategies.`
            });
        } else if (avgPain >= 7) {
            insights.push({
                icon: 'bi-exclamation-triangle-fill text-warning',
                title: 'High Pain Levels',
                message: `Your average pain level (${avgPain.toFixed(1)}/10) is high. Consider discussing pain management options with your healthcare provider.`
            });
        }

        // Mood insights
        if (avgMood >= 7) {
            insights.push({
                icon: 'bi-emoji-smile-fill text-success',
                title: 'Positive Mood Trend',
                message: `Your average mood (${avgMood.toFixed(1)}/10) shows consistent positivity. This supports overall wellbeing.`
            });
        } else if (avgMood <= 4) {
            insights.push({
                icon: 'bi-heart-fill text-primary',
                title: 'Mood Support',
                message: `Your average mood (${avgMood.toFixed(1)}/10) suggests you might benefit from additional support or stress management techniques.`
            });
        }

        // Sleep insights
        if (avgSleep < 6) {
            insights.push({
                icon: 'bi-moon-fill text-info',
                title: 'Sleep Improvement Needed',
                message: `You're averaging ${avgSleep.toFixed(1)} hours of sleep. Aim for 7-9 hours for optimal health and pain management.`
            });
        } else if (avgSleep >= 7 && avgSleep <= 9) {
            insights.push({
                icon: 'bi-check-circle-fill text-success',
                title: 'Excellent Sleep Habits!',
                message: `Your average sleep (${avgSleep.toFixed(1)} hours) is in the healthy range, supporting overall wellbeing.`
            });
        }

        // Trend insights
        const painTrend = this.calculateTrend(pain_data);
        const moodTrend = this.calculateTrend(mood_data);

        if (painTrend < -0.1) {
            insights.push({
                icon: 'bi-arrow-down-circle-fill text-success',
                title: 'Pain Trending Down',
                message: 'Your pain levels show a decreasing trend over this period. Great progress!'
            });
        } else if (painTrend > 0.1) {
            insights.push({
                icon: 'bi-arrow-up-circle-fill text-warning',
                title: 'Pain Trending Up',
                message: 'Your pain levels show an increasing trend. Consider reviewing your management strategies.'
            });
        }

        if (moodTrend > 0.1) {
            insights.push({
                icon: 'bi-arrow-up-circle-fill text-success',
                title: 'Mood Improving',
                message: 'Your mood shows an upward trend over this period. Keep up the positive momentum!'
            });
        }

        return insights;
    }

    calculateTrend(data) {
        if (data.length < 2) return 0;
        
        const n = data.length;
        const sumX = (n * (n + 1)) / 2;
        const sumY = data.reduce((a, b) => a + b, 0);
        const sumXY = data.reduce((sum, y, x) => sum + (x + 1) * y, 0);
        const sumXX = (n * (n + 1) * (2 * n + 1)) / 6;
        
        return (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
    }

    displayInsights(insights, container) {
        if (insights.length === 0) {
            container.innerHTML = '<p class="text-muted">Keep tracking to see personalized insights based on your data patterns.</p>';
            return;
        }

        container.innerHTML = insights.map(insight => `
            <div class="insight-item mb-3 p-3 border rounded">
                <div class="d-flex align-items-center mb-2">
                    <i class="${insight.icon} me-2" style="font-size: 1.2rem;"></i>
                    <h6 class="mb-0">${insight.title}</h6>
                </div>
                <p class="mb-0 text-muted small">${insight.message}</p>
            </div>
        `).join('');
    }

    showError(message) {
        const container = document.getElementById('insightsContainer');
        container.innerHTML = `
            <div class="alert alert-danger" role="alert">
                <i class="bi bi-exclamation-triangle me-2"></i>
                ${message}
            </div>
        `;
    }
}

// Initialize analytics when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    new AnalyticsManager();
});