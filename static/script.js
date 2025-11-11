document.addEventListener('DOMContentLoaded', function () {
    const k1Slider = document.getElementById('k1');
    const k2Slider = document.getElementById('k2');
    const k1ValueSpan = document.getElementById('k1-value');
    const k2ValueSpan = document.getElementById('k2-value');
    const metricK1 = document.getElementById('metric-k1');
    const metricK2 = document.getElementById('metric-k2');
    const metricRatio = document.getElementById('metric-ratio');
    const plotDiv = document.getElementById('plot');

    function updatePlot() {
        const k1 = parseFloat(k1Slider.value);
        const k2 = parseFloat(k2Slider.value);

        k1ValueSpan.textContent = k1.toFixed(3);
        k2ValueSpan.textContent = k2.toFixed(3);
        metricK1.textContent = `${k1.toFixed(3)} min⁻¹`;
        metricK2.textContent = `${k2.toFixed(3)} min⁻¹`;
        metricRatio.textContent = (k2 / k1).toFixed(2);

        fetch('/data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ k1: k1, k2: k2 })
        })
        .then(response => {
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return response.json();
        })
        .then(data => {
            // Render Plotly chart
            Plotly.react(plotDiv, data.data, data.layout, {
                responsive: true,
                displayModeBar: true,
                modeBarButtonsToRemove: ['select2d', 'lasso2d', 'autoScale2d'],
                displaylogo: false
            });
        })
        .catch(err => {
            console.error('Failed to update plot:', err);
            plotDiv.innerText = 'Error loading plot. See console for details.';
        });
    }

    k1Slider.addEventListener('input', updatePlot);
    k2Slider.addEventListener('input', updatePlot);

    // Initial plot
    updatePlot();
});
